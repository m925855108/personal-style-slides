#!/usr/bin/env python3
"""Extract a compact style profile from a template, old deck, PDF, or screenshots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import inspect_sources
from style_utils import IMAGE_SUFFIXES, classify_layout, extract_css_px_values, guess_density, markdown_list, top_items, write_json


def image_dimensions(path: Path):
    try:
        data = path.read_bytes()
        if path.suffix.lower() == ".png" and data[:8] == b"\x89PNG\r\n\x1a\n":
            return {"width": int.from_bytes(data[16:20], "big"), "height": int.from_bytes(data[20:24], "big")}
        if path.suffix.lower() in (".jpg", ".jpeg"):
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                size = int.from_bytes(data[i + 2 : i + 4], "big")
                if marker in (0xC0, 0xC2):
                    return {"height": int.from_bytes(data[i + 5 : i + 7], "big"), "width": int.from_bytes(data[i + 7 : i + 9], "big")}
                i += 2 + size
    except Exception:
        return None
    return None


def inspect_input(path: Path, extract_dir: Path | None, render_dir: Path | None):
    if path.is_dir():
        images = []
        for item in sorted(path.rglob("*")):
            if item.suffix.lower() in IMAGE_SUFFIXES:
                images.append({"path": str(item), "dimensions": image_dimensions(item)})
        return {"kind": "screenshot-directory", "file": {"path": str(path), "name": path.name}, "images": images[:300]}
    return inspect_sources.inspect_path(path, extract_dir, render_dir)


def build_profile(items):
    colors = []
    font_sizes = []
    css_vars = []
    classes = []
    slide_count = 0
    image_count = 0
    text_preview = ""
    canvas = None
    source_names = []
    warnings = []

    for item in items:
        source_names.append(item.get("file", {}).get("name", "unknown"))
        warnings.extend(item.get("warnings", []))
        kind = item.get("kind")
        if kind == "html":
            slide_count += item.get("slide_like_sections") or 0
            image_count += len(item.get("images", []))
            tokens = item.get("style_tokens", {})
            colors += tokens.get("colors", [])
            font_sizes += tokens.get("font_sizes", [])
            css_vars += tokens.get("css_variables", [])
            classes += [name for name, _ in item.get("top_classes", [])]
        elif kind == "pptx":
            slide_count += len(item.get("slides", []))
            image_count += len(item.get("media", []))
            colors += item.get("theme_colors", [])
            canvas = item.get("slide_size") or canvas
            classes += [layout.get("layout_name") or layout.get("name") for layout in item.get("layouts", [])]
            text_preview += " ".join(s.get("text_preview", "") for s in item.get("slides", [])[:12])
        elif kind == "latex":
            slide_count += len(item.get("frames", []))
            image_count += len(item.get("graphics", []))
            classes += item.get("themes", [])
            text_preview += " ".join(item.get("frames", [])[:20])
        elif kind == "pdf":
            slide_count += item.get("pages") or 0
            image_count += len(item.get("images", [])) + len(item.get("page_renders", []))
            text_preview += item.get("text_preview", "")
        elif kind == "docx":
            image_count += len(item.get("media", []))
            text_preview += " ".join(p.get("text", "") for p in item.get("paragraphs", [])[:40])
        elif kind == "screenshot-directory":
            image_count += len(item.get("images", []))
            classes.append("screenshot-reference")

    top_colors = top_items(colors, 18)
    top_fonts = top_items(font_sizes, 16)
    layouts = classify_layout(classes, slide_count, image_count)
    profile = {
        "profile_kind": "auto_style_profile",
        "sources": source_names,
        "canvas": canvas,
        "slide_count": slide_count,
        "image_count": image_count,
        "visual_density": guess_density(slide_count, text_preview, image_count),
        "dominant_colors": top_colors,
        "font_size_tokens": top_fonts,
        "font_px_values": extract_css_px_values(font_sizes),
        "css_variables": top_items(css_vars, 30),
        "layout_archetypes": layouts,
        "style_contract": {
            "imitate": [
                "canvas ratio and slide shell",
                "title/footer/page-number placement",
                "dominant colors and accent usage",
                "layout archetypes and figure/text rhythm",
                "figure and caption treatment visible in the seed",
            ],
            "adapt": [
                "slide count",
                "figure scale",
                "text density",
                "multi-figure layouts",
                "scientific diagrams required by new content",
            ],
        },
        "warnings": warnings,
    }
    return profile


def to_markdown(profile):
    lines = [
        "# Auto Style Summary",
        "",
        "This file is an automatically extracted style seed. Treat it as a compact guide, not a perfect visual model.",
        "",
        f"- Sources: {markdown_list(profile.get('sources', []))}",
        f"- Canvas: {profile.get('canvas') or 'not detected'}",
        f"- Slide/page count: {profile.get('slide_count')}",
        f"- Image/media count: {profile.get('image_count')}",
        f"- Visual density: {profile.get('visual_density')}",
        f"- Dominant colors: {markdown_list(profile.get('dominant_colors', []))}",
        f"- Font size tokens: {markdown_list(profile.get('font_size_tokens', []))}",
        f"- Layout archetypes: {markdown_list(profile.get('layout_archetypes', []))}",
        "",
        "## Imitate",
    ]
    lines += [f"- {x}" for x in profile["style_contract"]["imitate"]]
    lines += ["", "## Adapt For New Content"]
    lines += [f"- {x}" for x in profile["style_contract"]["adapt"]]
    if profile.get("warnings"):
        lines += ["", "## Warnings"]
        lines += [f"- {w}" for w in profile["warnings"]]
    return "\n".join(lines) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(description="Extract a compact style profile from templates, old decks, PDFs, HTML, or screenshots.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out-dir", default="style_profile_output")
    parser.add_argument("--extract-dir")
    parser.add_argument("--render-dir")
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    extract_dir = Path(args.extract_dir).resolve() if args.extract_dir else out_dir / "extracted_assets"
    render_dir = Path(args.render_dir).resolve() if args.render_dir else out_dir / "rendered_pages"
    items = []
    for raw in args.paths:
        path = Path(raw).resolve()
        if path.exists():
            items.append(inspect_input(path, extract_dir, render_dir))
        else:
            items.append({"kind": "missing", "file": {"path": str(path), "name": path.name}, "warnings": ["Path does not exist."]})
    profile = build_profile(items)
    profile["raw_inspection"] = {"items": items}
    json_path = out_dir / "style_profile.auto.json"
    md_path = out_dir / "style_summary.auto.md"
    write_json(json_path, profile)
    md_path.write_text(to_markdown(profile), encoding="utf-8")
    print(json.dumps({"style_profile": str(json_path), "style_summary": str(md_path), "status": "ok"}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
