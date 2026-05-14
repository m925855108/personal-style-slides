# Personal Style Slides

Learn from your own slide templates. Generate HTML decks in your personal style.

[中文](README.md) | English

---

Personal Style Slides is an installable Codex/Claude-style skill. It is not a generic PPT beautifier. It learns from a PPTX, HTML deck, PDF, old deck, or screenshot you already like, then generates new HTML slides with the same slide rhythm, typography hierarchy, content density, figure/text ratio, and caption habits.

It is optimized for thesis proposals, defenses, group meetings, literature reports, simulation/result reports, and academic presentations. It can also be used for other personalized HTML slide work when matching a user's template style is the main requirement.

## Core Workflow

```text
Approved template / old deck / screenshot
        |
        v
Extract compact style seed
        |
        v
Generate personalized HTML slides
        |
        v
Static checks + optional browser-render verification
        |
        v
User feedback
        |
        v
Update local style memory only with approval
```

## Key Features

- Learns from your own approved PPTX, HTML, PDF, old decks, or screenshots instead of generic themes.
- Preserves slide rhythm, typography hierarchy, density, figure/text ratio, caption treatment, and footer style.
- Adds research safeguards for scientific wording, source figures, evidence traceability, and uncertainty notes.
- Outputs browser-ready HTML slides with print/PDF support.
- Includes helper scripts for source inspection, style profile extraction, static checks, browser-render verification, and style memory updates.
- Privacy-first: real templates, unpublished figures, institutional logos, advisor comments, commercial fonts, and personal style memory stay local.

## Installation

The repository root is not the installable skill. Install only the inner folder:

```text
personal-style-slides/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

### Install For Codex

Windows PowerShell:

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\"
```

macOS/Linux:

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

Replace the target path if your Codex skills directory is different.

### Install For Claude

macOS/Linux:

```bash
git clone https://github.com/m925855108/personal-style-slides.git
mkdir -p ~/.claude/skills
cp -r personal-style-slides/personal-style-slides ~/.claude/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.claude\skills\"
```

If your Claude client uses a different skills directory, copy the folder there instead.

### Install From ZIP

Download ZIP from GitHub, unzip it, and copy only the inner `personal-style-slides/` folder into your Codex or Claude skills directory. Do not copy the repository root as the skill.

## Quick Start

Install optional dependencies:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

Check the local environment:

```bash
python personal-style-slides/scripts/doctor.py
```

Put your approved template or old deck here:

```text
personal-style-slides/assets/templates/
```

Extract a style seed:

```bash
python personal-style-slides/scripts/extract_style_profile.py \
  personal-style-slides/assets/templates/my_template.pptx \
  --out-dir style_profile_output
```

After generating a deck, run checks:

```bash
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

PPTX visual rendering requires LibreOffice for PPTX-to-PDF conversion and PyMuPDF for PDF-to-PNG rendering. Without both, PPTX inspection falls back to OOXML metadata.

## Example Prompts

```text
Use the personal-style-slides skill.
Learn the style from assets/templates/my_template.pptx, then create an 8-minute thesis proposal HTML deck from proposal.docx.
```

```text
Use the personal-style-slides skill.
This old deck is my approved style reference. Revise the new deck to match its layout rhythm, figure/text ratio, and caption treatment.
```

```text
Use the personal-style-slides skill.
Generate a group-meeting report from these simulation results, keeping the style close to the template in assets/templates/.
```

## Demo

See `examples_demo/demo_template_seed/`:

```text
input/demo_template.html
input/research_notes.md
output/style_profile.auto.json
output/style_summary.auto.md
```

The demo shows the basic path:

```text
template seed -> style summary/profile -> personalized deck generation
```

The demo uses synthetic materials and contains no private data.

## Repository Structure

```text
personal-style-slides/          # install this folder as the skill
  SKILL.md
  agents/
  assets/
  references/
  scripts/

examples_demo/                  # synthetic public demo
README.md
README_EN.md
requirements.txt
THIRD_PARTY_NOTICES.md
LICENSE
```

## Privacy

Keep private materials local. Do not commit:

- real templates or old decks
- unpublished figures or confidential project images
- institutional logos
- advisor/client comments
- personal style memory
- commercial or system font files

This repository publishes the skill framework, not private user content.

## Limitations

- This is a skill package, not a standalone slide application, web app, or full CLI product.
- Style extraction is a compact style seed, not a complete visual reconstruction.
- Style fingerprint comparison is advisory and cannot prove visual similarity.
- Static HTML checks cannot prove rendered non-overlap.
- Browser-render verification depends on Playwright or a local browser.

## License

MIT
