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
Static checks + optional browser verification
        |
        v
User feedback
        |
        v
Update local style memory only with approval
```

## Key Features

- Learns from your approved PPTX, HTML deck, PDF, or screenshots instead of generic themes.
- Preserves your slide rhythm, title habits, typography hierarchy, density, figure/text ratio, and caption style.
- Supports traceable claims, figures, and source references for research and academic materials.
- Generates browser-ready HTML slides with print/PDF-oriented checks.
- Provides static checks, browser-render verification, lightweight style fingerprint comparison, and style memory update scripts.
- Keeps private templates, unpublished figures, logos, comments, and style memory local by default.

## Install

This repository has two layers:

```text
repo root/
  README.md
  README_EN.md
  requirements.txt
  examples_demo/

  personal-style-slides/   # install only this folder as the skill
    SKILL.md
    agents/
    assets/
    references/
    scripts/
```

Do not install the repository root as a skill. Install only the `personal-style-slides/` subfolder.

### Install for Codex

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

Windows PowerShell example:

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\personal-style-slides"
```

### Install for Claude

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.claude/skills/
```

Windows PowerShell example:

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.claude\skills\personal-style-slides"
```

If your client uses a different skills directory, replace the target path with the actual one.

### ZIP Install

Download the repository ZIP, unzip it, then copy the inner `personal-style-slides/` folder into your Codex or Claude skills directory.

## Optional Dependencies

The skill itself can be installed directly. These dependencies are only for local helper scripts:

```bash
pip install -r requirements.txt
python -m playwright install chromium
python personal-style-slides/scripts/doctor.py
```

PPTX visual rendering fallback requires:

```text
LibreOffice: PPTX -> PDF
PyMuPDF: PDF -> PNG
```

If these tools are unavailable, the skill falls back to lightweight metadata checks and should not claim complete visual template parsing.

## Quick Start

1. Put an approved template, old deck, or screenshot into the local skill's `assets/templates/`.
2. Ask Codex/Claude to use the installed `personal-style-slides` skill.
3. After generation, run optional helper checks.

```bash
python personal-style-slides/scripts/extract_style_profile.py personal-style-slides/assets/templates/my_template.pptx
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

`extract_style_profile.py` produces a compact style seed, not a complete visual reconstruction. Final style judgment still requires screenshots and manual review.

## Example Prompts

```text
Use the personal-style-slides skill.
Learn the style from assets/templates/my_template.pptx, then create an 8-minute thesis proposal HTML deck from proposal.docx.
```

```text
Use the personal-style-slides skill.
This old deck is the style reference. Please revise the new content to match its layout rhythm, figure/text ratio, and caption style.
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

## Credits

Created by @MV with Codex.

## License

MIT