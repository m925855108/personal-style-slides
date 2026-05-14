# Personal Style Slides

> Learn from your own slide templates. Generate HTML decks in your personal style.

Personal Style Slides is an installable Codex/Claude-style skill for personalized HTML slide decks. Instead of applying generic themes, it learns from a PPTX, HTML deck, PDF, old deck, or screenshot you already like. It extracts a compact style seed, generates or revises slides in that style, and updates local style memory only when you approve.

It is optimized for thesis proposals, group meetings, literature reports, simulation/result reports, and academic presentations where both style consistency and source traceability matter. It can also be used for non-research personalized slide work when template fidelity and HTML delivery are the main goals.

## Core Idea

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

- Learns from your own approved PPTX, HTML, PDF, old decks, or screenshots.
- Preserves slide rhythm, typography, density, layout habits, figure treatment, captions, and footer style.
- Adds research safeguards for claims, source figures, image provenance, and cautious wording.
- Generates browser-ready HTML decks with print/PDF support.
- Includes local helper scripts for source inspection, style extraction, static checks, render verification, and style memory updates.
- Keeps private templates, unpublished figures, advisor/client comments, fonts, and style memory local.

## Install

Install only the skill folder:

```text
personal-style-slides/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

Do not install the repository root as the skill.

### Option A: Clone And Copy

macOS/Linux:

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\"
```

Replace `~/.codex/skills/` or `%USERPROFILE%\.codex\skills\` with your actual Codex/Claude skills directory.

### Option B: Download ZIP

Download ZIP from GitHub, unzip it, then copy only the inner `personal-style-slides/` folder into your skills directory.

## Quick Start

Install optional local dependencies:

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

Extract a compact style seed:

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
This old deck is my approved style reference. Revise the new deck to match its layout rhythm, figure/text ratio, caption treatment, and footer style.
```

```text
Use the personal-style-slides skill.
Generate a group-meeting report from these simulation results, keeping the style close to the template in assets/templates/.
```

## Demo

See `examples_demo/demo_template_seed/` for a synthetic example:

```text
input/demo_template.html
input/research_notes.md
output/style_profile.auto.json
output/style_summary.auto.md
```

The demo shows the intended path:

```text
template seed -> style summary/profile -> personalized deck generation
```

The demo contains no private data.

## Repository Structure

```text
personal-style-slides/          # install this folder as the skill
  SKILL.md
  agents/
  assets/
  references/
  scripts/

examples_demo/                  # synthetic public demos
README.md
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

The repository publishes the skill framework, not private user content.

## Limitations

- This is a skill package, not a standalone slide application, web app, or CLI product.
- Style extraction is a compact style seed, not a complete visual reconstruction.
- Fingerprint comparison is advisory and cannot prove visual similarity.
- Static HTML checks cannot prove rendered non-overlap.
- Browser-render verification depends on Playwright or a local browser.

## 中文快速说明

> 让 Codex/Claude 学习你认可的模板，按你的审美生成个性化 HTML 演示文稿。

这个 skill 不是通用 PPT 美化工具。你提供一个认可的 PPTX、HTML deck、PDF、旧演示文稿或截图，它会提取“风格种子”，并在生成新 slides 时尽量保持你的页面节奏、字体层级、内容密度、图文比例、图注风格和页脚习惯。

适合：

- 博士开题、答辩、组会、文献汇报、模拟结果汇报；
- 已有模板或旧 deck，希望后续 slides 按同一审美生成；
- 需要 HTML slides、PDF/print 支持、本地检查和可追溯图片/内容来源的场景。

安装时只复制仓库里的内层目录：

```text
personal-style-slides/
```

不要把整个仓库根目录作为 skill 安装。

示例提示词：

```text
请使用 personal-style-slides skill。
以 assets/templates/my_template.pptx 作为风格模板，根据 proposal.docx 生成一份 8 分钟博士开题报告 HTML 演示文稿。
```

```text
请使用 personal-style-slides skill。
这个旧 deck 是我认可的风格，请把新内容改成类似的版式节奏、图文比例和图注风格。
```

隐私原则：真实模板、未发表图片、机构 logo、导师批注、个人 style memory、商业字体和系统字体都应保留在本地，不要提交到公开仓库。
