#!/usr/bin/env python3
"""Browser-rendered validation for research HTML slide decks.

Uses Playwright when installed for DOM/bounding-box checks. Without Playwright,
it can still capture a screenshot with a local Chrome/Edge executable. The
fallback is useful evidence, but it cannot prove non-overlap.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


CHROMIUM_BROWSER_NAMES = ["google-chrome", "chromium", "chromium-browser", "msedge", "microsoft-edge"]
FIREFOX_BROWSER_NAMES = ["firefox"]
CHROMIUM_BROWSER_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    str(Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
FIREFOX_BROWSER_PATHS = [
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "/Applications/Firefox.app/Contents/MacOS/firefox",
]


def file_url(path: Path) -> str:
    return path.resolve().as_uri()


def safe_exists(path: str) -> bool:
    try:
        return Path(path).exists()
    except OSError:
        return False


def browser_candidates() -> list[tuple[str, str]]:
    found = []
    for name in CHROMIUM_BROWSER_NAMES:
        path = shutil.which(name)
        if path:
            found.append(("chromium", path))
    for path in CHROMIUM_BROWSER_PATHS:
        found.append(("chromium", path))
    for name in FIREFOX_BROWSER_NAMES:
        path = shutil.which(name)
        if path:
            found.append(("firefox", path))
    for path in FIREFOX_BROWSER_PATHS:
        found.append(("firefox", path))
    return found


def discover_browser(explicit: str | None = None) -> tuple[str, str] | None:
    if explicit and safe_exists(explicit):
        name = Path(explicit).name.lower()
        kind = "firefox" if "firefox" in name else "chromium"
        return kind, str(Path(explicit).resolve())
    for kind, candidate in browser_candidates():
        if safe_exists(candidate):
            return kind, candidate
    return None


def rect_overlap(a: dict, b: dict) -> bool:
    return not (
        a["x"] + a["width"] <= b["x"]
        or b["x"] + b["width"] <= a["x"]
        or a["y"] + a["height"] <= b["y"]
        or b["y"] + b["height"] <= a["y"]
    )


async def playwright_check(html: Path, out_dir: Path, width: int, height: int, max_slides: int | None) -> dict:
    from playwright.async_api import async_playwright  # type: ignore

    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"mode": "playwright", "viewport": {"width": width, "height": height}, "slides": [], "errors": [], "warnings": []}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        await page.goto(file_url(html))
        await page.wait_for_timeout(400)
        count = await page.evaluate(
            """() => {
              const sections = Array.from(document.querySelectorAll('.reveal .slides section, section.slide, main section, body > section, section'));
              return sections.length || 1;
            }"""
        )
        if max_slides:
            count = min(count, max_slides)
        for idx in range(count):
            await page.evaluate(
                """(idx) => {
                  if (window.Reveal && Reveal.slide) {
                    Reveal.slide(idx);
                  } else {
                    const sections = Array.from(document.querySelectorAll('.reveal .slides section, section.slide, main section, body > section, section'));
                    sections.forEach((s, i) => {
                      s.style.display = i === idx ? '' : 'none';
                      s.classList.toggle('active', i === idx);
                    });
                  }
                }""",
                idx,
            )
            await page.wait_for_timeout(250)
            shot = out_dir / f"slide_{idx + 1:03d}.png"
            await page.screenshot(path=str(shot), full_page=True)
            data = await page.evaluate(
                """() => {
                  const visible = (el) => {
                    const s = getComputedStyle(el);
                    const r = el.getBoundingClientRect();
                    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 1 && r.height > 1;
                  };
                  const root = Array.from(document.querySelectorAll('.active, .present, section.slide, section'))
                    .find(visible) || document.body;
                  const nodes = Array.from(root.querySelectorAll('h1,h2,h3,p,li,blockquote,pre,code,img,svg,canvas,table,.title,.content,.footer,.caption,.slide-no'));
                  const items = nodes.filter(visible).slice(0, 250).map((el) => {
                    const r = el.getBoundingClientRect();
                    const cs = getComputedStyle(el);
                    return {
                      tag: el.tagName.toLowerCase(),
                      className: el.className ? String(el.className).slice(0,120) : '',
                      text: (el.innerText || el.alt || '').replace(/\s+/g,' ').slice(0,120),
                      x: r.x, y: r.y, width: r.width, height: r.height,
                      fontSize: cs.fontSize,
                      overflowX: el.scrollWidth > el.clientWidth + 2,
                      overflowY: el.scrollHeight > el.clientHeight + 2,
                      naturalWidth: el.naturalWidth || null,
                      naturalHeight: el.naturalHeight || null
                    };
                  });
                  const brokenImages = Array.from(root.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0)
                    .map(img => img.src);
                  return {items, brokenImages};
                }"""
            )
            warnings = []
            items = data["items"]
            for item in items:
                if item["overflowX"] or item["overflowY"]:
                    warnings.append({"rule": "element-overflow", "item": item})
                if item["x"] < -2 or item["y"] < -2 or item["x"] + item["width"] > width + 2 or item["y"] + item["height"] > height + 2:
                    warnings.append({"rule": "element-outside-viewport", "item": item})
            key_items = [i for i in items if i["tag"] in ("h1", "h2", "h3", "p", "li", "img", "table", "svg", "canvas")]
            for a_i, a in enumerate(key_items):
                for b in key_items[a_i + 1 :]:
                    if rect_overlap(a, b):
                        overlap_area = min(a["x"] + a["width"], b["x"] + b["width"]) - max(a["x"], b["x"])
                        overlap_area *= min(a["y"] + a["height"], b["y"] + b["height"]) - max(a["y"], b["y"])
                        if overlap_area > 80:
                            warnings.append({"rule": "possible-overlap", "a": a, "b": b})
                            break
            for src in data["brokenImages"]:
                warnings.append({"rule": "broken-image-rendered", "src": src})
            report["slides"].append({"number": idx + 1, "screenshot": str(shot), "warnings": warnings, "item_count": len(items)})
        await browser.close()
    report["status"] = "warn" if any(s["warnings"] for s in report["slides"]) else "ok"
    return report


def screenshot_fallback(html: Path, out_dir: Path, width: int, height: int, browser: str | None) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    discovered = discover_browser(browser)
    report = {"mode": "browser-screenshot-fallback", "viewport": {"width": width, "height": height}, "errors": [], "warnings": []}
    if not discovered:
        report["errors"].append("No supported browser executable found. Provide --browser path.")
        report["status"] = "error"
        return report
    kind, exe = discovered
    shot = out_dir / "deck_first_view.png"
    if kind == "firefox":
        cmd = [exe, "--headless", "--screenshot", str(shot), "--window-size", f"{width},{height}", file_url(html)]
    else:
        cmd = [exe, "--headless=new", "--disable-gpu", f"--window-size={width},{height}", f"--screenshot={shot}", file_url(html)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
        report["screenshots"] = [str(shot)]
        report["browser"] = {"kind": kind, "path": exe}
        report["warnings"].append("Screenshot fallback cannot inspect DOM boxes or prove non-overlap.")
        report["status"] = "warn"
    except Exception as exc:
        report["errors"].append(str(exc))
        report["status"] = "error"
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render-check a local HTML slide deck.")
    parser.add_argument("html", help="HTML deck path.")
    parser.add_argument("--out-dir", default="render_check", help="Screenshot/report directory.")
    parser.add_argument("--out-json", help="Report JSON path.")
    parser.add_argument("--browser", help="Chrome/Edge executable for fallback screenshots.")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--max-slides", type=int)
    args = parser.parse_args(argv)

    html = Path(args.html).resolve()
    out_dir = Path(args.out_dir).resolve()
    try:
        import asyncio
        import playwright  # type: ignore  # noqa: F401

        report = asyncio.run(playwright_check(html, out_dir, args.width, args.height, args.max_slides))
    except Exception as exc:
        report = screenshot_fallback(html, out_dir, args.width, args.height, args.browser)
        report.setdefault("warnings", []).append(f"Playwright unavailable or failed: {exc}")
    data = json.dumps(report, ensure_ascii=False, indent=2)
    console = json.dumps(report, ensure_ascii=True, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(data, encoding="utf-8")
    print(console)
    return 1 if report.get("status") == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
