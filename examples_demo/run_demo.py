#!/usr/bin/env python3
"""Run the bundled synthetic demo for Personal Style Slides.

This is a smoke test for the public repository, not a full slide generator.
It checks that helper scripts can inspect a template seed, produce a style
profile, create a style fingerprint, and audit the demo HTML deck.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_step(name: str, cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        "name": name,
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "status": "ok" if proc.returncode == 0 else "error",
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    scripts = repo_root / "personal-style-slides" / "scripts"
    demo = repo_root / "examples_demo" / "demo_template_seed"
    html = demo / "input" / "demo_template.html"
    out_dir = demo / "run_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    steps = [
        run_step("doctor", [sys.executable, str(scripts / "doctor.py")]),
        run_step(
            "extract_style_profile",
            [sys.executable, str(scripts / "extract_style_profile.py"), str(html), "--out-dir", str(out_dir / "style_profile")],
        ),
        run_step(
            "extract_style_fingerprint",
            [sys.executable, str(scripts / "extract_style_fingerprint.py"), str(html), "--out-json", str(out_dir / "style_fingerprint.json")],
        ),
        run_step(
            "check_html_deck",
            [sys.executable, str(scripts / "check_html_deck.py"), str(html), "--out-json", str(out_dir / "deck_check.json")],
        ),
    ]

    report = {
        "demo": "demo_template_seed",
        "html": str(html),
        "output_dir": str(out_dir),
        "steps": steps,
        "status": "ok" if all(step["returncode"] == 0 for step in steps if step["name"] != "doctor") else "error",
        "notes": [
            "doctor.py may report missing optional dependencies; that is acceptable for this synthetic demo.",
            "This demo proves the helper scripts run on a small HTML seed. It does not prove high-fidelity PPTX template reconstruction.",
        ],
    }
    report_path = out_dir / "run_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(report_path)}, ensure_ascii=True, indent=2))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
