#!/usr/bin/env python3
"""Compare two lightweight style fingerprints."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from style_utils import load_json, write_json


def overlap(a, b):
    sa, sb = set(a or []), set(b or [])
    if not sa and not sb:
        return {"score": None, "matched": [], "missing": []}
    matched = sorted(sa & sb)
    return {"score": round(len(matched) / max(1, len(sa | sb)), 3), "matched": matched, "missing": sorted(sa - sb)}


def main(argv):
    parser = argparse.ArgumentParser(description="Compare generated style fingerprint against a reference fingerprint.")
    parser.add_argument("reference")
    parser.add_argument("generated")
    parser.add_argument("--out-json", default="style_similarity_report.json")
    args = parser.parse_args(argv)

    ref = load_json(Path(args.reference))
    gen = load_json(Path(args.generated))
    report = {
        "reference": ref.get("source", args.reference),
        "generated": gen.get("source", args.generated),
        "matched_traits": {},
        "drifted_traits": [],
        "likely_acceptable_differences": [],
        "needs_manual_review": [],
    }
    for key in ("dominant_colors", "font_tokens", "layout_archetypes"):
        report["matched_traits"][key] = overlap(ref.get(key), gen.get(key))
        if report["matched_traits"][key]["score"] is not None and report["matched_traits"][key]["score"] < 0.35:
            report["drifted_traits"].append(key)
    for key in ("visual_density", "canvas"):
        if ref.get(key) == gen.get(key):
            report["matched_traits"][key] = ref.get(key)
        else:
            report["needs_manual_review"].append({"trait": key, "reference": ref.get(key), "generated": gen.get(key)})
    report["summary"] = "Style fingerprints are lightweight; use screenshots/manual review for final style judgment."
    out = Path(args.out_json).resolve()
    write_json(out, report)
    print(json.dumps({"status": "ok", "report": str(out), "drifted_traits": report["drifted_traits"]}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
