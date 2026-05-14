#!/usr/bin/env python3
"""Check optional local dependencies for the personal research slides skill."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path


def module_available(name):
    return importlib.util.find_spec(name) is not None


def safe_exists(path):
    try:
        return Path(path).exists()
    except OSError:
        return False


def first_existing(paths):
    for path in paths:
        if path and safe_exists(path):
            return path
    return None


def browser_candidates():
    names = ["google-chrome", "chromium", "chromium-browser", "msedge", "microsoft-edge", "firefox"]
    found = [shutil.which(name) for name in names]
    common_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        str(Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Firefox.app/Contents/MacOS/firefox",
    ]
    return [p for p in found + common_paths if p]


def main():
    report = {
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "modules": {
            "fitz_pymupdf": module_available("fitz"),
            "pypdf": module_available("pypdf"),
            "PyPDF2": module_available("PyPDF2"),
            "playwright": module_available("playwright"),
        },
        "executables": {
            "libreoffice": shutil.which("soffice") or shutil.which("libreoffice"),
            "browser": first_existing(browser_candidates()),
        },
        "notes": [
            "PyMuPDF improves PDF text/image/page rendering.",
            "Playwright enables DOM box verification.",
            "Chrome/Edge enables screenshot fallback.",
            "PPTX visual rendering requires LibreOffice for PPTX-to-PDF conversion plus PyMuPDF for PDF-to-PNG page rendering.",
            "Without LibreOffice and PyMuPDF, PPTX inspection falls back to OOXML metadata only.",
        ],
    }
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
