#!/usr/bin/env python3
"""Shared lightweight style helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def top_items(items, limit=12):
    counts = {}
    for item in items:
        if not item:
            continue
        counts[item] = counts.get(item, 0) + 1
    return [k for k, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def classify_layout(classes, slide_count=0, image_count=0):
    joined = " ".join(classes).lower()
    hits = []
    for name, patterns in {
        "two-column": ["two-col", "two_column", "split", "image-left", "text-left"],
        "card-modules": ["card", "module", "panel", "mini-card"],
        "workflow": ["flow", "workflow", "chain", "step"],
        "timeline": ["timeline", "track", "plan"],
        "section-divider": ["section", "divider", "cover"],
        "figure-first": ["image-card", "figure", "caption"],
        "left-navigation": ["sidebar", "side-nav", "left-nav"],
    }.items():
        if any(p in joined for p in patterns):
            hits.append(name)
    if image_count and slide_count and image_count >= slide_count * 0.6:
        hits.append("figure-heavy")
    return sorted(set(hits))


def guess_density(slide_count, text_preview="", image_count=0):
    text_len = len(text_preview or "")
    if slide_count and image_count >= slide_count and text_len < slide_count * 240:
        return "figure-forward"
    if slide_count and text_len > slide_count * 700:
        return "dense text"
    if slide_count and text_len < slide_count * 220:
        return "sparse"
    return "moderate"


def markdown_list(values):
    return ", ".join(str(v) for v in values) if values else "not detected"


def extract_css_px_values(values):
    out = []
    for value in values:
        out.extend(re.findall(r"([0-9]+(?:\.[0-9]+)?px)", str(value)))
    return top_items(out, 12)
