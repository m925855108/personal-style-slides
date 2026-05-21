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


def compare_scalar(ref, gen, key, report):
    if ref.get(key) == gen.get(key):
        report["matched_traits"][key] = ref.get(key)
    else:
        report["needs_manual_review"].append({"trait": key, "reference": ref.get(key), "generated": gen.get(key)})


def compare_image_ratio(ref_sig, gen_sig, report):
    ref_ratio = ref_sig.get("image_per_slide")
    gen_ratio = gen_sig.get("image_per_slide")
    if ref_ratio is None or gen_ratio is None:
        report["needs_manual_review"].append({"trait": "image_per_slide", "reference": ref_ratio, "generated": gen_ratio})
        return
    diff = abs(ref_ratio - gen_ratio)
    report["matched_traits"]["image_per_slide_delta"] = round(diff, 3)
    if diff > 0.45:
        report["drifted_traits"].append("image_per_slide")


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
    for key in ("dominant_colors", "font_tokens", "font_px_values", "font_families", "layout_archetypes"):
        report["matched_traits"][key] = overlap(ref.get(key), gen.get(key))
        if report["matched_traits"][key]["score"] is not None and report["matched_traits"][key]["score"] < 0.35:
            report["drifted_traits"].append(key)
    ref_sig = ref.get("layout_signature", {})
    gen_sig = gen.get("layout_signature", {})
    report["matched_traits"]["layout_motifs"] = overlap(ref_sig.get("layout_motifs"), gen_sig.get("layout_motifs"))
    if report["matched_traits"]["layout_motifs"]["score"] is not None and report["matched_traits"]["layout_motifs"]["score"] < 0.35:
        report["drifted_traits"].append("layout_motifs")
    compare_image_ratio(ref_sig, gen_sig, report)
    for key in ("visual_density", "canvas"):
        compare_scalar(ref, gen, key, report)
    for key in ("image_density", "geometry_available", "has_rendered_references"):
        compare_scalar(ref_sig, gen_sig, key, report)
    if not ref_sig.get("has_rendered_references"):
        report["likely_acceptable_differences"].append(
            "Reference fingerprint has no rendered slide screenshots; geometry similarity is approximate."
        )
    report["summary"] = (
        "Style fingerprints are lightweight and rule-based. They compare colors, type scale, font families, density, "
        "layout motifs, geometry availability, and image ratio, but screenshots/manual review remain necessary for final style judgment."
    )
    out = Path(args.out_json).resolve()
    write_json(out, report)
    print(json.dumps({"status": "ok", "report": str(out), "drifted_traits": report["drifted_traits"]}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
