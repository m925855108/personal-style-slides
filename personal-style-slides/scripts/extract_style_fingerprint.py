#!/usr/bin/env python3
"""Extract a lightweight style fingerprint for comparison."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import extract_style_profile
from style_utils import write_json


FINGERPRINT_VERSION = "0.3"


def bucket_number(value: float | int | None, buckets: list[tuple[float, str]]) -> str | None:
    if value is None:
        return None
    for limit, label in buckets:
        if value <= limit:
            return label
    return buckets[-1][1] if buckets else None


def collect_raw_traits(profile: dict) -> dict:
    classes = []
    css_variables = []
    font_families = []
    font_typefaces = []
    geometry_hints = []
    theme_layouts = []
    page_renders = 0
    raw_items = profile.get("raw_inspection", {}).get("items", [])
    for item in raw_items:
        kind = item.get("kind")
        if kind == "html":
            classes.extend(name for name, _count in item.get("top_classes", []))
            css_variables.extend(item.get("style_tokens", {}).get("css_variables", []))
            font_families.extend(item.get("style_tokens", {}).get("font_families", []))
        elif kind == "pptx":
            theme_layouts.extend(
                (layout.get("layout_name") or layout.get("name") or "")
                for layout in item.get("layouts", [])
            )
            font_typefaces.extend(item.get("font_typefaces", []))
            if item.get("geometry_summary"):
                geometry_hints.append(item["geometry_summary"])
            for layout in item.get("layouts", []):
                if layout.get("geometry_summary"):
                    geometry_hints.append(layout["geometry_summary"])
            page_renders += len(item.get("page_renders", []))
        elif kind == "pdf":
            page_renders += len(item.get("page_renders", []))
    return {
        "top_classes": sorted(set(filter(None, classes)))[:24],
        "css_variables": sorted(set(filter(None, css_variables)))[:24],
        "font_families": sorted(set(filter(None, font_families + font_typefaces)))[:24],
        "template_layout_names": sorted(set(filter(None, theme_layouts)))[:24],
        "geometry_hints": geometry_hints[:12],
        "rendered_reference_pages": page_renders,
    }


def ratio_signature(slide_count: int | None, image_count: int | None) -> dict:
    if not slide_count:
        return {"image_per_slide": None, "image_density": None}
    ratio = round((image_count or 0) / max(1, slide_count), 3)
    return {
        "image_per_slide": ratio,
        "image_density": bucket_number(
            ratio,
            [
                (0.15, "text-forward"),
                (0.7, "balanced"),
                (1.3, "figure-forward"),
                (99, "multi-figure-heavy"),
            ],
        ),
    }


def derive_layout_signature(profile: dict, raw_traits: dict) -> dict:
    slide_count = profile.get("slide_count") or 0
    image_count = profile.get("image_count") or 0
    ratio = ratio_signature(slide_count, image_count)
    archetypes = profile.get("layout_archetypes", [])
    motifs = sorted(
        set(archetypes)
        | {
            name
            for name in raw_traits.get("top_classes", [])
            if any(token in name.lower() for token in ("card", "grid", "split", "sidebar", "caption", "figure", "timeline", "hero"))
        }
    )
    return {
        "visual_density": profile.get("visual_density"),
        "image_density": ratio["image_density"],
        "image_per_slide": ratio["image_per_slide"],
        "layout_archetypes": archetypes,
        "layout_motifs": motifs[:20],
        "geometry_available": bool(profile.get("geometry_summaries") or raw_traits.get("geometry_hints")),
        "has_rendered_references": bool(raw_traits.get("rendered_reference_pages")),
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Extract lightweight style fingerprint from a deck/template/screenshot directory.")
    parser.add_argument("path")
    parser.add_argument("--out-json", default="style_fingerprint.json")
    args = parser.parse_args(argv)

    path = Path(args.path).resolve()
    item = extract_style_profile.inspect_input(path, None, None)
    profile = extract_style_profile.build_profile([item])
    profile["raw_inspection"] = {"items": [item]}
    raw_traits = collect_raw_traits(profile)
    layout_signature = derive_layout_signature(profile, raw_traits)
    fp = {
        "fingerprint_version": FINGERPRINT_VERSION,
        "source": str(path),
        "canvas": profile.get("canvas"),
        "slide_count": profile.get("slide_count"),
        "image_count": profile.get("image_count"),
        "visual_density": profile.get("visual_density"),
        "dominant_colors": profile.get("dominant_colors", [])[:12],
        "font_tokens": profile.get("font_size_tokens", [])[:12],
        "font_px_values": profile.get("font_px_values", [])[:12],
        "font_families": profile.get("font_families", [])[:12],
        "layout_archetypes": profile.get("layout_archetypes", []),
        "geometry_summaries": profile.get("geometry_summaries", [])[:8],
        "layout_signature": layout_signature,
        "raw_trait_hints": raw_traits,
        "notes": [
            "This is a lightweight personal style fingerprint, not a trained model or visual proof.",
            "Use rendered screenshots and manual review for final style judgment.",
        ],
    }
    out = Path(args.out_json).resolve()
    write_json(out, fp)
    print(json.dumps({"status": "ok", "fingerprint": str(out)}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
