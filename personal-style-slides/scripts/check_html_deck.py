#!/usr/bin/env python3
"""Static resource/style audit for a generated research HTML slide deck.

This script does not prove that rendered slides are visually non-overlapping.
Use verify_rendered_deck.py for browser-level validation.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import sys
from collections import Counter
from pathlib import Path


class DeckParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images = []
        self.links = []
        self.sections = 0
        self.data_slides = 0
        self.slide_class_nodes = 0
        self.style_blocks = []
        self._in_style = False
        self._style_buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append({"src": attrs.get("src", ""), "alt": attrs.get("alt", ""), "class": attrs.get("class", "")})
        if tag == "link" and attrs.get("href"):
            self.links.append({"href": attrs.get("href", ""), "rel": attrs.get("rel", "")})
        if tag == "section":
            self.sections += 1
        if attrs.get("data-slide") is not None:
            self.data_slides += 1
        if "slide" in str(attrs.get("class", "")).split():
            self.slide_class_nodes += 1
        if tag == "style":
            self._in_style = True
            self._style_buf = []

    def handle_endtag(self, tag):
        if tag == "style" and self._in_style:
            self.style_blocks.append("".join(self._style_buf))
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)


def is_external(src: str) -> bool:
    return bool(re.match(r"^(https?:)?//|^data:", src))


def resolve_asset(base: Path, src: str) -> Path:
    src = src.split("#", 1)[0].split("?", 1)[0]
    return (base / src).resolve()


def risky_css(css: str) -> list[dict]:
    checks = [
        ("info", "negative-margin", r"margin(?:-[\w]+)?\s*:\s*-[^;]+"),
        ("warn", "absolute-position", r"position\s*:\s*absolute"),
        ("info", "viewport-font-scaling", r"font-size\s*:\s*[^;]*(?:vw|vh)"),
        ("info", "fixed-image-height", r"(?:height|max-height)\s*:\s*(?:calc\([^;]+|[0-9.]+(?:px|vh))"),
        ("warn", "overflow-hidden", r"overflow\s*:\s*hidden"),
    ]
    out = []
    for severity, name, pattern in checks:
        matches = re.findall(pattern, css, flags=re.I)
        if matches:
            out.append({"severity": severity, "rule": name, "count": len(matches), "examples": matches[:5]})
    return out


def css_number(value: str) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def font_size_audit(css: str, strict: bool = False) -> tuple[list[dict], list[dict], dict]:
    required_vars = ["--ts-title", "--ts-subtitle", "--ts-body", "--ts-caption", "--ts-footnote"]
    found_vars = {name for name in required_vars if re.search(rf"{re.escape(name)}\s*:", css)}
    missing_vars = [name for name in required_vars if name not in found_vars]
    px_values = [css_number(v) for v in re.findall(r"font-size\s*:\s*([0-9.]+)px", css, flags=re.I)]
    px_values = [v for v in px_values if v is not None]
    unique_px = sorted(set(round(v, 2) for v in px_values))
    errors = []
    warnings = []
    if missing_vars and strict:
        errors.append(
            {
                "severity": "error",
                "rule": "missing-type-scale-variables",
                "message": missing_vars,
            }
        )
    too_small = sorted(set(v for v in unique_px if v < 14))
    if too_small:
        target = errors if strict else warnings
        target.append(
            {
                "severity": "error" if strict else "warn",
                "rule": "minimum-font-size",
                "message": f"Font sizes below 14px detected: {too_small}",
            }
        )
    if len(unique_px) > 9:
        target = errors if strict else warnings
        target.append(
            {
                "severity": "error" if strict else "warn",
                "rule": "font-size-variance",
                "message": f"{len(unique_px)} unique raw px font sizes detected. Prefer unified type variables.",
                "values": unique_px[:30],
            }
        )
    elif len(unique_px) > 6:
        warnings.append(
            {
                "severity": "warn",
                "rule": "font-size-variance",
                "message": f"{len(unique_px)} unique raw px font sizes detected.",
                "values": unique_px[:30],
            }
        )
    return errors, warnings, {"required_variables": required_vars, "missing_variables": missing_vars, "unique_px_values": unique_px}


def image_size_audit(css: str, strict: bool = False) -> tuple[list[dict], list[dict], dict]:
    required_vars = ["--img-full", "--img-half", "--img-third"]
    found_vars = {name for name in required_vars if re.search(rf"{re.escape(name)}\s*:", css)}
    missing_vars = [name for name in required_vars if name not in found_vars]
    height_tokens = re.findall(r"(?:height|max-height)\s*:\s*([^;}{]+)", css, flags=re.I)
    normalized = sorted(set(re.sub(r"\s+", " ", token.strip()) for token in height_tokens if token.strip()))
    errors = []
    warnings = []
    if missing_vars and strict:
        errors.append(
            {
                "severity": "error",
                "rule": "missing-image-scale-variables",
                "message": missing_vars,
            }
        )
    ad_hoc = [token for token in normalized if not token.startswith("var(--img") and "100vh" not in token and "100dvh" not in token]
    if len(ad_hoc) > 6:
        target = errors if strict else warnings
        target.append(
            {
                "severity": "error" if strict else "warn",
                "rule": "image-height-variance",
                "message": f"{len(ad_hoc)} non-standard image/height tokens detected. Prefer unified image variables.",
                "values": ad_hoc[:30],
            }
        )
    elif len(ad_hoc) > 4:
        warnings.append(
            {
                "severity": "warn",
                "rule": "image-height-variance",
                "message": f"{len(ad_hoc)} non-standard image/height tokens detected.",
                "values": ad_hoc[:30],
            }
        )
    return errors, warnings, {"required_variables": required_vars, "missing_variables": missing_vars, "height_tokens": normalized[:50]}


def collect_manifest_images(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    found = set()

    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in ("src", "path", "name") and isinstance(value, str):
                    if re.search(r"\.(png|jpe?g|gif|webp|svg|tiff?)$", value, re.I):
                        found.add(Path(value).name.lower())
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return found


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check generated HTML deck for image and CSS risks.")
    parser.add_argument("html", help="Generated HTML deck path.")
    parser.add_argument("--manifest-json", help="Optional source inspection JSON to compare image use.")
    parser.add_argument("--out-json", help="Write check report JSON.")
    parser.add_argument("--strict-layout", action="store_true", help="Treat missing layout/type/image guardrails as errors.")
    args = parser.parse_args(argv)

    html_path = Path(args.html).resolve()
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    parser_obj = DeckParser()
    parser_obj.feed(text)
    base = html_path.parent

    errors = []
    warnings = []
    info = []
    missing = []
    local_images = []
    external_images = []
    large_data_uri_count = 0
    for img in parser_obj.images:
        src = img.get("src", "")
        if not src:
            warnings.append({"severity": "warn", "rule": "empty-image-src", "message": "An img tag has no src."})
            continue
        if src.startswith("data:") and len(src) > 1_000_000:
            large_data_uri_count += 1
        if is_external(src):
            if not src.startswith("data:"):
                external_images.append(src)
            continue
        local_images.append(src)
        resolved = resolve_asset(base, src)
        if not resolved.exists():
            missing.append(src)

    counts = Counter(local_images)
    repeated = [{"src": src, "count": count} for src, count in counts.items() if count > 1]
    manifest_images = collect_manifest_images(Path(args.manifest_json).resolve() if args.manifest_json else None)
    used_names = {Path(src).name.lower() for src in local_images}
    manifest_unused = sorted(manifest_images - used_names)[:100] if manifest_images else []
    css = "\n".join(parser_obj.style_blocks)
    slide_like_count = max(parser_obj.sections, parser_obj.data_slides, parser_obj.slide_class_nodes)
    if slide_like_count == 0:
        errors.append({"severity": "error", "rule": "zero-slide-sections", "message": "No section, data-slide, or .slide elements found."})
    elif parser_obj.sections == 0 and parser_obj.data_slides == 0:
        warnings.append({"severity": "warn", "rule": "custom-slide-unmarked", "message": "Slides appear to use custom HTML; add data-slide attributes for generic render verification."})
    for src in missing:
        errors.append({"severity": "error", "rule": "missing-local-image", "message": src})
    for item in repeated:
        warnings.append({"severity": "warn", "rule": "repeated-image", "message": item})
    for src in external_images:
        warnings.append({"severity": "warn", "rule": "external-image-dependency", "message": src})
    if large_data_uri_count:
        warnings.append({"severity": "warn", "rule": "large-data-uri-image", "message": f"{large_data_uri_count} data URI image(s) exceed 1MB."})
    for name in manifest_unused:
        warnings.append({"severity": "warn", "rule": "manifest-image-unused", "message": name})
    font_errors, font_warnings, font_report = font_size_audit(css, args.strict_layout)
    image_errors, image_warnings, image_report = image_size_audit(css, args.strict_layout)
    errors.extend(font_errors)
    errors.extend(image_errors)
    warnings.extend(font_warnings)
    warnings.extend(image_warnings)
    info.extend(risky_css(css))
    report = {
        "html": str(html_path),
        "sections": parser_obj.sections,
        "data_slide_count": parser_obj.data_slides,
        "slide_class_count": parser_obj.slide_class_nodes,
        "slide_like_count": slide_like_count,
        "image_count": len(parser_obj.images),
        "local_image_count": len(local_images),
        "missing_images": missing,
        "repeated_images": repeated,
        "manifest_unused_image_names": manifest_unused,
        "font_size_audit": font_report,
        "image_size_audit": image_report,
        "strict_layout": args.strict_layout,
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "status": "error" if errors else "warn" if warnings else "ok",
        "notes": [
            "Static checks cannot prove visual non-overlap; use browser screenshots or DOM bounding boxes before final delivery when possible."
        ],
    }
    data = json.dumps(report, ensure_ascii=False, indent=2)
    console_data = json.dumps(report, ensure_ascii=True, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(data, encoding="utf-8")
    print(console_data)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
