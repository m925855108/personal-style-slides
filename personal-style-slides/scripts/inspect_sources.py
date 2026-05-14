#!/usr/bin/env python3
"""Inspect research slide sources and templates.

The script is intentionally stdlib-first. Optional PDF libraries are used only
when already installed. It emits JSON by default and can also write a concise
Markdown memory file after the user approves saving one.
"""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def sha256_short(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def file_record(path: Path) -> dict:
    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "suffix": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "sha256_16": sha256_short(path),
    }


class HtmlSummaryParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images = []
        self.links = []
        self.sections = 0
        self.classes = {}
        self.style_blocks = []
        self._in_style = False
        self._style_buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and attrs.get("src"):
            self.images.append({"src": attrs.get("src"), "alt": attrs.get("alt", "")})
        if tag == "link" and attrs.get("href"):
            self.links.append({"href": attrs.get("href"), "rel": attrs.get("rel", "")})
        if tag == "section":
            self.sections += 1
        if attrs.get("class"):
            for cls in attrs["class"].split():
                self.classes[cls] = self.classes.get(cls, 0) + 1
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


def inspect_html(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = HtmlSummaryParser()
    parser.feed(text)
    css = "\n".join(parser.style_blocks)
    colors = sorted(set(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]+\)|hsla?\([^)]+\)", css)))[:80]
    font_sizes = sorted(set(re.findall(r"font-size\s*:\s*[^;}{]+", css)))[:80]
    variables = sorted(set(re.findall(r"--[-\w]+\s*:\s*[^;}{]+", css)))[:120]
    top_classes = sorted(parser.classes.items(), key=lambda kv: (-kv[1], kv[0]))[:50]
    compact_images = []
    for img in parser.images[:200]:
        src = img.get("src", "")
        if src.startswith("data:"):
            compact_images.append({"src_preview": src[:96] + "...", "data_uri": True, "chars": len(src), "alt": img.get("alt", "")[:200]})
        else:
            compact_images.append({"src": src[:500], "alt": img.get("alt", "")[:200]})
    return {
        "kind": "html",
        "file": file_record(path),
        "slide_like_sections": parser.sections,
        "images": compact_images,
        "links": parser.links[:100],
        "top_classes": top_classes,
        "style_tokens": {"colors": colors, "font_sizes": font_sizes, "css_variables": variables},
    }


def xml_text(blob: bytes) -> str:
    text = blob.decode("utf-8", errors="ignore")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def render_pptx_with_libreoffice(path: Path, render_dir: Path) -> dict:
    result = {"page_renders": [], "warnings": []}
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        result["warnings"].append("LibreOffice not found; PPTX rendering fallback unavailable.")
        return result
    render_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(render_dir), str(path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
    except Exception as exc:
        result["warnings"].append(f"LibreOffice PPTX to PDF conversion failed: {exc}")
        return result
    pdf = render_dir / f"{path.stem}.pdf"
    if not pdf.exists():
        result["warnings"].append("LibreOffice conversion did not produce the expected PDF.")
        return result
    page_dir = render_dir / f"{path.stem}_rendered_pages"
    pdf_report = inspect_pdf(pdf, None, page_dir)
    result["page_renders"] = pdf_report.get("page_renders", [])
    result["warnings"].extend(pdf_report.get("warnings", []))
    if not result["page_renders"]:
        result["warnings"].append("PPTX converted to PDF, but page image rendering needs PyMuPDF.")
    return result


def inspect_pptx(path: Path, render_dir: Path | None = None) -> dict:
    out = {"kind": "pptx", "file": file_record(path), "slide_size": None, "slides": [], "media": [], "layouts": [], "masters": [], "theme_colors": []}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for name in names:
            if name.startswith("ppt/media/"):
                info = z.getinfo(name)
                out["media"].append({"name": name, "size_bytes": info.file_size})
        if "ppt/presentation.xml" in names:
            root = ET.fromstring(z.read("ppt/presentation.xml"))
            for el in root.iter():
                if el.tag.endswith("sldSz"):
                    out["slide_size"] = {"cx": el.attrib.get("cx"), "cy": el.attrib.get("cy")}
                    break
        for name in sorted(n for n in names if n.startswith("ppt/slideLayouts/slideLayout") and n.endswith(".xml")):
            root = ET.fromstring(z.read(name))
            shape_count = sum(1 for el in root.iter() if el.tag.endswith("sp"))
            pic_count = sum(1 for el in root.iter() if el.tag.endswith("pic"))
            title = ""
            for el in root.iter():
                if el.tag.endswith("cSld"):
                    title = el.attrib.get("name", "")
                    break
            out["layouts"].append({"name": name, "layout_name": title, "shape_count": shape_count, "picture_count": pic_count})
        for name in sorted(n for n in names if n.startswith("ppt/slideMasters/slideMaster") and n.endswith(".xml")):
            root = ET.fromstring(z.read(name))
            out["masters"].append({
                "name": name,
                "shape_count": sum(1 for el in root.iter() if el.tag.endswith("sp")),
                "picture_count": sum(1 for el in root.iter() if el.tag.endswith("pic")),
            })
        for name in sorted(n for n in names if n.startswith("ppt/theme/theme") and n.endswith(".xml")):
            root = ET.fromstring(z.read(name))
            for el in root.iter():
                if el.tag.endswith("srgbClr") and el.attrib.get("val"):
                    out["theme_colors"].append("#" + el.attrib["val"])
            out["theme_colors"] = sorted(set(out["theme_colors"]))[:80]
        slide_names = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.findall(r"\d+", n)[-1]),
        )
        for slide_name in slide_names:
            idx = int(re.findall(r"\d+", slide_name)[-1])
            text = xml_text(z.read(slide_name))
            rels_name = f"ppt/slides/_rels/slide{idx}.xml.rels"
            images = []
            if rels_name in names:
                rel_root = ET.fromstring(z.read(rels_name))
                for rel in rel_root:
                    target = rel.attrib.get("Target", "")
                    rtype = rel.attrib.get("Type", "")
                    if "image" in rtype or target.startswith("../media/"):
                        images.append(target)
            root = ET.fromstring(z.read(slide_name))
            out["slides"].append({
                "number": idx,
                "text_preview": text[:800],
                "images": images,
                "shape_count": sum(1 for el in root.iter() if el.tag.endswith("sp")),
                "picture_count": sum(1 for el in root.iter() if el.tag.endswith("pic")),
                "graphic_frame_count": sum(1 for el in root.iter() if el.tag.endswith("graphicFrame")),
            })
    if render_dir:
        rendered = render_pptx_with_libreoffice(path, render_dir)
        out["page_renders"] = rendered.get("page_renders", [])
        out.setdefault("warnings", []).extend(rendered.get("warnings", []))
    return out


def inspect_docx(path: Path, extract_dir: Path | None = None) -> dict:
    out = {"kind": "docx", "file": file_record(path), "paragraphs": [], "media": [], "relationships": [], "warnings": []}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for name in names:
            if name.startswith("word/media/"):
                info = z.getinfo(name)
                rec = {"name": name, "size_bytes": info.file_size}
                if extract_dir:
                    extract_dir.mkdir(parents=True, exist_ok=True)
                    dest = extract_dir / f"{path.stem}_{Path(name).name}"
                    dest.write_bytes(z.read(name))
                    rec["path"] = str(dest)
                out["media"].append(rec)
        if "word/document.xml" in names:
            xml = z.read("word/document.xml").decode("utf-8", errors="ignore")
            paras = re.findall(r"<w:p[\s\S]*?</w:p>", xml)
            for para in paras[:300]:
                texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", para)
                text = re.sub(r"\s+", " ", " ".join(texts)).strip()
                if not text:
                    continue
                style = ""
                m = re.search(r"<w:pStyle[^>]+w:val=\"([^\"]+)\"", para)
                if m:
                    style = m.group(1)
                out["paragraphs"].append({"style": style, "text": text[:1000]})
        if "word/_rels/document.xml.rels" in names:
            root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
            for rel in root:
                target = rel.attrib.get("Target", "")
                rtype = rel.attrib.get("Type", "")
                if target or rtype:
                    out["relationships"].append({"target": target, "type": rtype})
    return out


def inspect_latex(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    frames = re.findall(r"\\begin\{frame\}(?:\[[^\]]*\])?(?:\{([^}]*)\})?", text)
    frame_titles = frames + re.findall(r"\\frametitle\{([^}]*)\}", text)
    graphics = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", text)
    sections = re.findall(r"\\(?:section|subsection)\*?\{([^}]*)\}", text)
    themes = re.findall(r"\\use(?:colortheme|fonttheme|innertheme|outertheme|theme)(?:\[[^\]]*\])?\{([^}]*)\}", text)
    colors = re.findall(r"\\definecolor\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", text)
    return {
        "kind": "latex",
        "file": file_record(path),
        "themes": themes,
        "sections": sections[:100],
        "frames": [t for t in frame_titles if t][:150],
        "graphics": graphics[:300],
        "defined_colors": colors[:80],
    }


def inspect_pdf(path: Path, extract_dir: Path | None = None, render_dir: Path | None = None) -> dict:
    out = {"kind": "pdf", "file": file_record(path), "pages": None, "text_preview": "", "images": [], "warnings": []}
    try:
        import fitz  # type: ignore

        doc = fitz.open(str(path))
        out["pages"] = len(doc)
        text_parts = []
        if extract_dir:
            extract_dir.mkdir(parents=True, exist_ok=True)
        if render_dir:
            render_dir.mkdir(parents=True, exist_ok=True)
        for page_i, page in enumerate(doc, start=1):
            if page_i <= 5:
                text_parts.append(page.get_text("text")[:2000])
            if render_dir:
                pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
                dest = render_dir / f"{path.stem}_page_{page_i:03d}.png"
                pix.save(str(dest))
                out.setdefault("page_renders", []).append(str(dest))
            for img_i, img in enumerate(page.get_images(full=True), start=1):
                rec = {"page": page_i, "index": img_i, "xref": img[0], "width": img[2], "height": img[3]}
                if extract_dir:
                    pix = doc.extract_image(img[0])
                    ext = pix.get("ext", "png")
                    name = f"{path.stem}_p{page_i:03d}_img{img_i:02d}.{ext}"
                    dest = extract_dir / name
                    dest.write_bytes(pix["image"])
                    rec["path"] = str(dest)
                out["images"].append(rec)
        out["text_preview"] = "\n".join(text_parts)[:6000]
        return out
    except Exception as exc:
        out["warnings"].append(f"PyMuPDF unavailable or failed: {exc}")
    for mod_name in ("pypdf", "PyPDF2"):
        try:
            mod = __import__(mod_name)
            reader = mod.PdfReader(str(path))
            out["pages"] = len(reader.pages)
            out["text_preview"] = "\n".join((p.extract_text() or "")[:1500] for p in reader.pages[:5])[:6000]
            out["warnings"].append("PDF image extraction unavailable without PyMuPDF; text-only fallback used.")
            return out
        except Exception as exc:
            out["warnings"].append(f"{mod_name} unavailable or failed: {exc}")
    raw = path.read_bytes()
    out["images_detected_by_raw_scan"] = len(re.findall(rb"/Subtype\s*/Image", raw))
    out["warnings"].append("No PDF parser library available; raw image-count fallback only.")
    return out


def inspect_path(path: Path, extract_dir: Path | None, render_dir: Path | None = None) -> dict:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        return inspect_html(path)
    if suffix == ".pptx":
        return inspect_pptx(path, render_dir)
    if suffix == ".docx":
        return inspect_docx(path, extract_dir)
    if suffix in (".tex", ".sty"):
        return inspect_latex(path)
    if suffix == ".pdf":
        return inspect_pdf(path, extract_dir, render_dir)
    return {"kind": "unknown", "file": file_record(path), "warnings": ["Unsupported file type; recorded metadata only."]}


def to_markdown(report: dict) -> str:
    lines = ["# Source Inspection Memory", ""]
    for item in report["items"]:
        file = item["file"]
        lines += [f"## {file['name']}", "", f"- Path: `{file['path']}`", f"- Type: {item['kind']}", f"- Size: {file['size_bytes']} bytes", f"- Hash: {file['sha256_16']}"]
        if item["kind"] == "html":
            lines += [f"- Slide-like sections: {item.get('slide_like_sections')}", f"- Images: {len(item.get('images', []))}"]
            if item.get("style_tokens", {}).get("colors"):
                lines += ["- Colors: " + ", ".join(item["style_tokens"]["colors"][:20])]
            if item.get("top_classes"):
                lines += ["- Frequent classes: " + ", ".join(k for k, _ in item["top_classes"][:20])]
        elif item["kind"] == "pptx":
            lines += [f"- Slides: {len(item.get('slides', []))}", f"- Media assets: {len(item.get('media', []))}", f"- Slide size: {item.get('slide_size')}"]
            if item.get("page_renders"):
                lines += [f"- Rendered slide images: {len(item.get('page_renders', []))}"]
            if item.get("theme_colors"):
                lines += ["- Theme colors: " + ", ".join(item["theme_colors"][:20])]
        elif item["kind"] == "docx":
            lines += [f"- Paragraphs: {len(item.get('paragraphs', []))}", f"- Media assets: {len(item.get('media', []))}"]
        elif item["kind"] == "latex":
            lines += ["- Themes: " + ", ".join(item.get("themes", [])[:20]), f"- Frames: {len(item.get('frames', []))}", f"- Graphics: {len(item.get('graphics', []))}"]
        elif item["kind"] == "pdf":
            lines += [f"- Pages: {item.get('pages')}", f"- Images listed: {len(item.get('images', []))}", f"- Text preview available: {bool(item.get('text_preview'))}"]
        for warning in item.get("warnings", []):
            lines.append(f"- Warning: {warning}")
        lines.append("")
    lines += [
        "## Reuse Notes",
        "",
        "- Use this file as a compact memory of the source/template after user approval.",
        "- Reinspect the original files if template CSS, figures, or scientific wording may have changed.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect PPTX, DOCX, HTML, LaTeX, and PDF sources for research HTML slides.")
    parser.add_argument("paths", nargs="+", help="Source/template paths to inspect.")
    parser.add_argument("--extract-dir", help="Directory for extracted PDF images when PyMuPDF is available.")
    parser.add_argument("--render-dir", help="Directory for PDF page-render fallback images when PyMuPDF is available.")
    parser.add_argument("--out-json", help="Write JSON report to this path.")
    parser.add_argument("--markdown-output", help="Write concise Markdown memory to this path after user approval.")
    args = parser.parse_args(argv)

    extract_dir = Path(args.extract_dir) if args.extract_dir else None
    render_dir = Path(args.render_dir) if args.render_dir else None
    report = {"items": []}
    for raw in args.paths:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            report["items"].append({"kind": "missing", "file": {"path": str(path), "name": path.name}, "warnings": ["Path does not exist."]})
            continue
        report["items"].append(inspect_path(path, extract_dir, render_dir))

    data = json.dumps(report, ensure_ascii=False, indent=2)
    console_data = json.dumps(report, ensure_ascii=True, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(data, encoding="utf-8")
    if args.markdown_output:
        Path(args.markdown_output).write_text(to_markdown(report), encoding="utf-8")
    print(console_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
