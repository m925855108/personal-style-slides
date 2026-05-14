# Personal Style Slides / 个性化 HTML 演示 Skill

## English

This repository contains an installable Codex/Claude-style skill:

```text
personal-style-slides/
```

It is not a universal slide-design system. It is a template-seeded, feedback-refined workflow for creating personalized HTML slide decks. Users provide an approved template, old deck, HTML deck, PPTX, PDF, or screenshot as the style seed. The skill extracts a compact style profile, generates or revises a personalized deck, and can update local style memory only after user approval.

The skill is optimized for research and academic presentations, but the core ability is broader: preserving a user's established slide aesthetics, rhythm, typography, density, layout habits, and figure treatment.

### Install

Copy the installable skill folder into your Codex/Claude skills directory:

```text
personal-style-slides/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

Do not install the repository root as the skill. Install only the `personal-style-slides/` subfolder.

### Typical Use

1. Put an approved local template, old deck, or screenshot folder under `personal-style-slides/assets/templates/`, or provide the file path in conversation.
2. Ask your agent to use the installed `personal-style-slides` skill. For example: "Use the personal-style-slides skill to create this deck based on this template."
3. The skill treats the provided template/deck/screenshot as the style seed.
4. It generates or modifies a personalized HTML slide deck, with stronger source-traceability safeguards for research tasks.
5. Reusable feedback is written to style memory only with user approval.

### Quick Start

Optional dependencies improve PDF/PPTX extraction and browser verification:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

Check the local environment:

```bash
python personal-style-slides/scripts/doctor.py
```

Extract a compact style profile from a local template or old deck:

```bash
python personal-style-slides/scripts/extract_style_profile.py \
  personal-style-slides/assets/templates/my_template.pptx \
  --out-dir style_profile_output
```

After generating a deck, run static checks:

```bash
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
```

Run optional browser-render verification:

```bash
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

PPTX visual rendering requires LibreOffice for PPTX-to-PDF conversion plus PyMuPDF for PDF-to-PNG page rendering. Without both, PPTX inspection falls back to OOXML metadata only.

### Demo

See `examples_demo/demo_template_seed/` for a synthetic template-seed example. The demo shows the expected local workflow:

```text
template/old deck -> style_profile.auto.json + style_summary.auto.md -> personalized deck generation
```

The demo is synthetic and safe to publish. Do not place private templates or unpublished figures in `examples_demo/`.

### Privacy

Keep private materials local. Do not commit:

- real templates or old decks
- unpublished figures or confidential project images
- institutional logos
- advisor/client comments
- personal style memory
- commercial or system font files

The repository is meant to publish the skill framework, not private user content.

### Limitations

- Style extraction is a compact style seed, not a complete visual reconstruction.
- Fingerprint comparison is advisory and cannot prove visual similarity.
- Static HTML checks cannot prove rendered non-overlap.
- Browser-render verification depends on Playwright or a local browser.

---

## 中文

这个仓库包含一个可直接安装的 Codex/Claude 风格 skill：

```text
personal-style-slides/
```

它不是通用 PPT 美化工具，而是一个“模板作为风格种子、对话反馈逐步优化”的个性化 HTML 演示文稿工作流。用户提供认可的模板、旧 deck、HTML deck、PPTX、PDF 或截图作为风格种子；skill 会提取紧凑的风格画像，生成或修改个性化演示文稿，并且只在用户批准后把可复用反馈写入本地 style memory。

这个 skill 主要为科研和学术演示优化，但核心能力更宽：保留使用者既有的审美、页面节奏、字体层级、内容密度、布局习惯和图片处理方式。

### 安装方式

把下面这个可安装 skill 文件夹复制到 Codex/Claude 的 skills 目录：

```text
personal-style-slides/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

不要把整个仓库根目录作为 skill 安装。应该只安装 `personal-style-slides/` 这个子目录。

### 典型用法

1. 将认可的本地模板、旧 deck 或截图文件夹放入 `personal-style-slides/assets/templates/`，也可以在对话中直接提供文件路径。
2. 请求模型使用已安装的 `personal-style-slides` skill。例如：“使用 personal-style-slides skill，根据这个模板制作演示文稿。”
3. skill 会把当前模板、旧 deck 或截图作为风格种子。
4. skill 会生成或修改个性化 HTML 演示文稿；如果任务是科研场景，会启用更强的来源追溯和科学准确性保护。
5. 只有在用户明确允许后，skill 才会把可复用的审美反馈写入本地 style memory。

### 快速开始

可选依赖可以增强 PDF/PPTX 提取和浏览器验证能力：

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

检查本地环境：

```bash
python personal-style-slides/scripts/doctor.py
```

从本地模板或旧 deck 提取紧凑风格画像：

```bash
python personal-style-slides/scripts/extract_style_profile.py \
  personal-style-slides/assets/templates/my_template.pptx \
  --out-dir style_profile_output
```

生成 deck 后运行静态检查：

```bash
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
```

运行可选浏览器渲染验证：

```bash
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

PPTX 视觉渲染需要 LibreOffice 完成 PPTX 到 PDF 的转换，并需要 PyMuPDF 将 PDF 页面渲染为 PNG。如果缺少这些工具，PPTX 检查会降级为 OOXML 元数据提取。

### Demo

见 `examples_demo/demo_template_seed/`。这是一个合成的模板种子示例，用来展示基本流程：

```text
模板/旧 deck -> style_profile.auto.json + style_summary.auto.md -> 个性化 deck 生成
```

demo 是合成材料，可以公开。不要把私人模板或未发表图片放入 `examples_demo/`。

### 隐私说明

请把私人材料留在本地，不要提交到公开仓库，包括：

- 真实模板或旧演示文稿
- 未发表结果图或保密项目图片
- 机构 logo
- 导师或客户批注
- 个人 style memory
- 商业字体或系统字体文件

这个仓库用于发布 skill 框架，而不是发布个人内容。

### 局限

- 风格提取只是紧凑的风格种子，不是完整视觉重建。
- 风格指纹比较只是辅助提示，不能证明视觉相似。
- 静态 HTML 检查不能证明浏览器渲染后没有重叠。
- 浏览器渲染验证依赖 Playwright 或本地浏览器。
