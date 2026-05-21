#!/usr/bin/env python3
"""Browser-rendered validation for research HTML slide decks.

Uses Playwright when installed for DOM/bounding-box checks. Without Playwright,
it can still capture a screenshot with a local Chrome/Edge executable. The
fallback is useful evidence, but it cannot prove non-overlap.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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

MAX_TEXT_CHARS_PER_SLIDE = 950
MAX_BULLETS_PER_SLIDE = 7
MAX_VISIBLE_ITEMS_PER_SLIDE = 90
MIN_CONTENT_VERTICAL_USE_RATIO = 0.42


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


def vertical_range(items: list[dict]) -> tuple[float, float] | None:
    if not items:
        return None
    top = min(item["y"] for item in items)
    bottom = max(item["y"] + item["height"] for item in items)
    return top, bottom


def overlaps_any(items_a: list[dict], items_b: list[dict]) -> list[dict]:
    warnings = []
    for a in items_a:
        for b in items_b:
            if rect_overlap(a, b):
                warnings.append({"a": a, "b": b})
                break
    return warnings


async def wait_for_reveal_or_stable_page(page) -> list[str]:
    warnings = []
    try:
        await page.wait_for_function(
            """() => {
              if (!window.Reveal) return true;
              if (typeof Reveal.isReady === 'function') return Reveal.isReady();
              return true;
            }""",
            timeout=3000,
        )
    except Exception:
        warnings.append("Reveal.js readiness was not confirmed within 3s; continuing with rendered DOM as-is.")
    try:
        await page.wait_for_load_state("networkidle", timeout=3000)
    except Exception:
        warnings.append("Network-idle state was not reached within 3s; continuing after a short stabilization wait.")
    await page.wait_for_timeout(250)
    return warnings


def slide_selector(generic_mode: bool) -> str:
    if generic_mode:
        return "[data-slide], .slide, section.slide, .reveal .slides section, main section, body > section, section"
    return ".reveal .slides section, section.slide, [data-slide], main section, body > section, section"


async def playwright_check(html: Path, out_dir: Path, width: int, height: int, max_slides: int | None, generic_mode: bool) -> dict:
    from playwright.async_api import async_playwright  # type: ignore

    out_dir.mkdir(parents=True, exist_ok=True)
    selector = slide_selector(generic_mode)
    report = {
        "mode": "playwright-generic" if generic_mode else "playwright",
        "viewport": {"width": width, "height": height},
        "slide_selector": selector,
        "slides": [],
        "errors": [],
        "warnings": [],
    }
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        await page.goto(file_url(html))
        report["warnings"].extend(await wait_for_reveal_or_stable_page(page))
        count = await page.evaluate(
            """(selector) => {
              const unique = [];
              const seen = new Set();
              for (const el of document.querySelectorAll(selector)) {
                if (!seen.has(el)) {
                  seen.add(el);
                  unique.push(el);
                }
              }
              return unique.length || 1;
            }""",
            selector,
        )
        if max_slides:
            count = min(count, max_slides)
        for idx in range(count):
            await page.evaluate(
                """({idx, selector, genericMode}) => {
                  const unique = [];
                  const seen = new Set();
                  for (const el of document.querySelectorAll(selector)) {
                    if (!seen.has(el)) {
                      seen.add(el);
                      unique.push(el);
                    }
                  }
                  document.querySelectorAll('[data-verify-active="true"]').forEach(el => {
                    el.removeAttribute('data-verify-active');
                  });
                  if (!genericMode && window.Reveal && Reveal.slide) {
                    Reveal.slide(idx);
                    const active = Array.from(document.querySelectorAll('.reveal .slides section.present, .reveal .slides section.active'))[0];
                    if (active) active.setAttribute('data-verify-active', 'true');
                  } else {
                    unique.forEach((s, i) => {
                      s.style.display = i === idx ? '' : 'none';
                      s.classList.toggle('active', i === idx);
                      s.classList.toggle('present', i === idx);
                      if (i === idx) {
                        s.setAttribute('data-verify-active', 'true');
                      }
                    });
                  }
                }""",
                {"idx": idx, "selector": selector, "genericMode": generic_mode},
            )
            await page.wait_for_timeout(250)
            shot = out_dir / f"slide_{idx + 1:03d}.png"
            await page.screenshot(path=str(shot), full_page=True)
            data = await page.evaluate(
                """(selector) => {
                  const visible = (el) => {
                    const s = getComputedStyle(el);
                    const r = el.getBoundingClientRect();
                    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 1 && r.height > 1;
                  };
                  const active = document.querySelector('[data-verify-active="true"]');
                  const root = (active && visible(active))
                    ? active
                    : (Array.from(document.querySelectorAll('.active, .present, [data-slide], .slide, section'))
                        .find(visible) || document.body);
                  const roleFor = (el) => {
                    const tag = el.tagName.toLowerCase();
                    const cls = String(el.className || '').toLowerCase();
                    if (tag === 'h1' || cls.includes('title') || cls.includes('headline')) return 'title';
                    if (tag === 'footer' || cls.includes('footer') || cls.includes('slide-no') || cls.includes('page-number')) return 'footer';
                    if (tag === 'img' || tag === 'svg' || tag === 'canvas') return 'figure';
                    if (cls.includes('caption') || tag === 'figcaption') return 'caption';
                    return 'content';
                  };
                  const nodes = Array.from(root.querySelectorAll('h1,h2,h3,p,li,blockquote,pre,code,img,svg,canvas,table,.title,.content,.footer,.caption,.slide-no'));
                  const items = nodes.filter(visible).slice(0, 250).map((el) => {
                    const r = el.getBoundingClientRect();
                    const cs = getComputedStyle(el);
                    return {
                      role: roleFor(el),
                      tag: el.tagName.toLowerCase(),
                      className: el.className ? String(el.className).slice(0,120) : '',
                      text: (el.innerText || el.alt || '').replace(/\\s+/g,' ').slice(0,120),
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
                  const textChars = items
                    .filter(item => ['title', 'content', 'caption'].includes(item.role))
                    .reduce((sum, item) => sum + (item.text || '').length, 0);
                  const bulletCount = items.filter(item => item.tag === 'li').length;
                  const figureCount = items.filter(item => item.role === 'figure').length;
                  return {items, brokenImages, textChars, bulletCount, figureCount};
                }""",
                selector,
            )
            warnings = []
            screenshot_bytes = shot.stat().st_size if shot.exists() else 0
            items = data["items"]
            if not items:
                warnings.append(
                    {
                        "rule": "verification-incomplete",
                        "message": "No visible text/image/table items were detected in the active slide DOM. Screenshot exists, but DOM overlap checks did not run for this slide.",
                        "screenshot_bytes": screenshot_bytes,
                    }
                )
            if screenshot_bytes < 10_000:
                warnings.append(
                    {
                        "rule": "screenshot-may-be-blank",
                        "message": "Screenshot file is very small; manually inspect whether the slide rendered correctly.",
                        "screenshot_bytes": screenshot_bytes,
                    }
                )
            title_items = [i for i in items if i.get("role") == "title"]
            footer_items = [i for i in items if i.get("role") == "footer"]
            content_items = [i for i in items if i.get("role") in ("content", "figure", "caption")]
            for item in items:
                if item["overflowX"] or item["overflowY"]:
                    warnings.append({"rule": "element-overflow", "item": item})
                if item["x"] < -2 or item["y"] < -2 or item["x"] + item["width"] > width + 2 or item["y"] + item["height"] > height + 2:
                    warnings.append({"rule": "element-outside-viewport", "item": item})
            for pair in overlaps_any(title_items, content_items):
                warnings.append({"rule": "title-content-overlap", **pair})
            for pair in overlaps_any(footer_items, content_items):
                warnings.append({"rule": "footer-content-overlap", **pair})
            content_range = vertical_range(content_items)
            if content_range:
                content_use = (content_range[1] - content_range[0]) / max(1, height)
                if content_use < MIN_CONTENT_VERTICAL_USE_RATIO and data["textChars"] > 220:
                    warnings.append(
                        {
                            "rule": "content-central-band-risk",
                            "vertical_use_ratio": round(content_use, 3),
                            "note": "Content occupies a narrow vertical band; consider spreading modules or splitting slides.",
                        }
                    )
            if data["textChars"] > MAX_TEXT_CHARS_PER_SLIDE:
                warnings.append({"rule": "dense-text-risk", "text_chars": data["textChars"], "limit": MAX_TEXT_CHARS_PER_SLIDE})
            if data["bulletCount"] > MAX_BULLETS_PER_SLIDE:
                warnings.append({"rule": "bullet-density-risk", "bullet_count": data["bulletCount"], "limit": MAX_BULLETS_PER_SLIDE})
            if len(items) > MAX_VISIBLE_ITEMS_PER_SLIDE:
                warnings.append({"rule": "many-visible-elements-risk", "item_count": len(items), "limit": MAX_VISIBLE_ITEMS_PER_SLIDE})
            if data["figureCount"] >= 3 and data["textChars"] > 360:
                warnings.append(
                    {
                        "rule": "multi-figure-density-risk",
                        "figure_count": data["figureCount"],
                        "text_chars": data["textChars"],
                        "note": "Multi-figure slides with substantial text often need split slides or zoom interaction.",
                    }
                )
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
            report["slides"].append(
                {
                    "number": idx + 1,
                    "screenshot": str(shot),
                    "warnings": warnings,
                    "item_count": len(items),
                    "text_chars": data["textChars"],
                    "bullet_count": data["bulletCount"],
                    "figure_count": data["figureCount"],
                    "screenshot_bytes": screenshot_bytes,
                }
            )
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
    parser.add_argument("--generic-mode", action="store_true", help="Prefer [data-slide]/.slide enumeration for custom HTML decks.")
    args = parser.parse_args(argv)

    html = Path(args.html).resolve()
    out_dir = Path(args.out_dir).resolve()
    try:
        import asyncio
        import playwright  # type: ignore  # noqa: F401

        report = asyncio.run(playwright_check(html, out_dir, args.width, args.height, args.max_slides, args.generic_mode))
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
