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

If you use a skill installer that accepts GitHub URLs, use the skill subfolder URL, not the repository root URL:

```text
https://github.com/m925855108/personal-style-slides/tree/main/personal-style-slides
```

For example, Codex's installer script needs the path explicitly:

```bash
python install-skill-from-github.py --repo m925855108/personal-style-slides --path personal-style-slides --dest D:/CodexSkills
```

Using only the repository root URL `https://github.com/m925855108/personal-style-slides` may fail because the installer cannot know which subfolder is the actual skill.

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

If the client does not detect the new skill immediately, restart Codex/Claude. After installation, verify with:

```text
Check whether the personal-style-slides skill is available and summarize what it is for.
```

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

## Included Helper Scripts

These scripts are not a rigid checklist that you must run by hand every time. They are helper tools for Codex/Claude when the skill is active, and you can also run them manually when you want to diagnose the environment, inspect output, or reuse a style. Most scripts are designed to degrade gently: if an optional dependency is missing, they should report the limitation instead of pretending that full verification was completed.

| Script | Purpose | Typical use |
| --- | --- | --- |
| `doctor.py` | Checks Python, browser, LibreOffice, PyMuPDF, Playwright, and related environment capabilities. | After installation, when scripts fail, or when browser verification is unavailable. |
| `inspect_sources.py` | Inspects PPTX, DOCX, PDF, HTML, LaTeX, or screenshot folders and summarizes text, images, pages, and template metadata. | When source documents, templates, or asset folders are available. |
| `extract_style_profile.py` | Extracts a compact style seed from a template, old deck, PDF, HTML deck, or screenshots. | Before generating or substantially revising a deck, so the agent can understand your style first. |
| `check_html_deck.py` | Performs static checks for slide sections, image paths, repeated images, and risky CSS patterns. | After generating HTML, as a basic sanity check. |
| `verify_rendered_deck.py` | Uses Playwright or a local browser for rendered checks, screenshots, and DOM box inspection. | When a browser or Playwright is available and rendered layout risk matters. |
| `extract_style_fingerprint.py` | Extracts a lightweight style fingerprint from a style profile. | Before comparing a generated deck against a template style. |
| `compare_style_fingerprint.py` | Compares two style fingerprints and reports matched or drifted traits. | To check whether colors, density, and layout habits roughly stayed close to the template. |
| `update_style_memory.py` | Lists, appends, or removes local style memory entries. | Only when you explicitly want a preference remembered long term. |
| `style_utils.py` | Internal helper functions shared by the other scripts. | Usually not run directly. |

## What Runs Automatically

When you ask Codex/Claude to use the `personal-style-slides` skill, the skill guides the agent to choose the right steps for the task. It should not run the full workflow for every small edit.

- If a template, old deck, PDF, HTML deck, or screenshot is available, the agent should inspect it first and use `inspect_sources.py` or `extract_style_profile.py` when useful.
- After generating or revising an HTML deck, the agent should usually run `check_html_deck.py` for static checks.
- If Playwright or a local browser is available, the agent may run `verify_rendered_deck.py` for rendered verification. If not available, it should clearly state the downgrade to static checks or screenshot-only evidence.
- When style similarity matters, the agent may use `extract_style_fingerprint.py` and `compare_style_fingerprint.py`, but these reports are advisory and do not replace screenshots or human review.
- `update_style_memory.py` should not write long-term memory automatically. The agent should update style memory only when you explicitly approve it or say something like "remember this style", "use this from now on", or "avoid this in the future".
- `doctor.py` is usually a manual diagnostic tool. The agent may suggest it when the environment is unclear, a browser cannot be found, or PPTX/PDF rendering support needs to be checked.

Small tasks should use a light path. For example, a one-slide edit, image replacement, or font-size adjustment should not trigger a full style-learning pass. Formal builds or major redesigns are better candidates for style extraction, content review, static checks, and browser-render verification.

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