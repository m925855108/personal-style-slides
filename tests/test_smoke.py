from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "personal-style-slides" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
DEMO_HTML = ROOT / "examples_demo" / "demo_template_seed" / "input" / "demo_template.html"


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class ScriptSmokeTests(unittest.TestCase):
    def test_check_html_deck_minimal_ok(self) -> None:
        result = run_script(str(SCRIPTS / "check_html_deck.py"), str(FIXTURES / "minimal_deck.html"))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["sections"], 1)

    def test_check_html_deck_missing_image_errors(self) -> None:
        result = run_script(str(SCRIPTS / "check_html_deck.py"), str(FIXTURES / "missing_image_deck.html"))
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["missing_images"], ["figures/not-found.png"])

    def test_extract_style_profile_demo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_script(str(SCRIPTS / "extract_style_profile.py"), str(DEMO_HTML), "--out-dir", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertTrue(Path(payload["style_profile"]).exists())
            self.assertTrue(Path(payload["style_summary"]).exists())

    def test_style_fingerprint_compare(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fp1 = tmp_path / "fp1.json"
            fp2 = tmp_path / "fp2.json"
            report = tmp_path / "style_similarity_report.json"
            first = run_script(str(SCRIPTS / "extract_style_fingerprint.py"), str(DEMO_HTML), "--out-json", str(fp1))
            second = run_script(str(SCRIPTS / "extract_style_fingerprint.py"), str(DEMO_HTML), "--out-json", str(fp2))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            compare = run_script(str(SCRIPTS / "compare_style_fingerprint.py"), str(fp1), str(fp2), "--out-json", str(report))
            self.assertEqual(compare.returncode, 0, compare.stderr)
            payload = json.loads(compare.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertTrue(report.exists())


if __name__ == "__main__":
    unittest.main()
