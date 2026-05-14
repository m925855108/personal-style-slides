#!/usr/bin/env python3
"""Extract a lightweight style fingerprint for comparison."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import extract_style_profile
from style_utils import write_json


def main(argv):
    parser = argparse.ArgumentParser(description="Extract lightweight style fingerprint from a deck/template/screenshot directory.")
    parser.add_argument("path")
    parser.add_argument("--out-json", default="style_fingerprint.json")
    args = parser.parse_args(argv)

    path = Path(args.path).resolve()
    item = extract_style_profile.inspect_input(path, None, None)
    profile = extract_style_profile.build_profile([item])
    fp = {
        "source": str(path),
        "canvas": profile.get("canvas"),
        "slide_count": profile.get("slide_count"),
        "image_count": profile.get("image_count"),
        "visual_density": profile.get("visual_density"),
        "dominant_colors": profile.get("dominant_colors", [])[:12],
        "font_tokens": profile.get("font_size_tokens", [])[:12],
        "layout_archetypes": profile.get("layout_archetypes", []),
    }
    out = Path(args.out_json).resolve()
    write_json(out, fp)
    print(json.dumps({"status": "ok", "fingerprint": str(out)}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
