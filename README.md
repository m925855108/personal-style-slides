# Personal Style Slides

让 Codex/Claude 学习你认可的模板，按你的审美生成个性化 HTML 演示文稿。

中文 | [English](README_EN.md)

---

Personal Style Slides 是一个可直接安装的 Codex/Claude-style skill。它不是通用 PPT 美化工具，而是让模型从你认可的 PPTX、HTML deck、PDF、旧演示文稿或截图中学习风格，再按同样的页面节奏、字体层级、内容密度、图文比例和图注习惯生成新的 HTML slides。

它主要面向博士开题、答辩、组会、文献汇报、模拟结果汇报和学术演示；也可以用于其他“需要按个人模板风格生成 HTML slides”的场景。

## 核心流程

```text
认可模板 / 旧 deck / 截图
        |
        v
提取紧凑风格种子
        |
        v
生成个性化 HTML slides
        |
        v
静态检查 + 可选浏览器验证
        |
        v
用户反馈
        |
        v
经用户允许后写入本地风格记忆
```

## 主要功能

- 从用户认可的 PPTX、HTML deck、PDF 或截图中学习风格，而不是套用通用主题。
- 保持用户已有的版式节奏、标题习惯、字体层级、内容密度、图文比例和图注风格。
- 支持科研/学术材料中的图像、论点和来源追踪。
- 生成浏览器可打开的 HTML slides，并支持打印/PDF 导出方向的检查。
- 提供静态检查、浏览器渲染验证、轻量风格指纹比较和风格记忆更新脚本。
- 默认保护隐私：真实模板、未发表图、机构 logo、导师批注和个人风格记忆应留在本地。

## 安装

这个仓库有两层结构：

```text
repo root/
  README.md
  README_EN.md
  requirements.txt
  examples_demo/

  personal-style-slides/   # 只安装这个目录作为 skill
    SKILL.md
    agents/
    assets/
    references/
    scripts/
```

不要把整个仓库根目录安装为 skill。只安装 `personal-style-slides/` 子目录。

### 安装到 Codex

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

Windows PowerShell 示例：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\personal-style-slides"
```

### 安装到 Claude

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.claude/skills/
```

Windows PowerShell 示例：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.claude\skills\personal-style-slides"
```

如果你的客户端使用不同的 skills 目录，请把目标路径替换为实际路径。

### ZIP 安装

下载仓库 ZIP，解压后把里面的 `personal-style-slides/` 子目录复制到 Codex 或 Claude 的 skills 目录。

如果客户端没有立即识别新 skill，请重启 Codex/Claude。安装后可以用下面的提示词验证：

```text
请检查 personal-style-slides skill 是否可用，并概括它适合做什么。
```

## 可选依赖

skill 本体可以直接安装。下面这些依赖只用于本地辅助脚本：

```bash
pip install -r requirements.txt
python -m playwright install chromium
python personal-style-slides/scripts/doctor.py
```

PPTX 视觉渲染 fallback 需要：

```text
LibreOffice: PPTX -> PDF
PyMuPDF: PDF -> PNG
```

如果缺少这些工具，skill 会回退到轻量 metadata 检查，不应声称已经完成完整视觉模板解析。

## 快速开始

1. 把你认可的模板、旧 deck 或截图放入本地 skill 的 `assets/templates/`。
2. 让 Codex/Claude 使用已安装的 `personal-style-slides` skill。
3. 生成后运行可选检查脚本。

```bash
python personal-style-slides/scripts/extract_style_profile.py personal-style-slides/assets/templates/my_template.pptx
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

`extract_style_profile.py` 生成的是紧凑风格种子，不是完整视觉重建。最终风格判断仍需要结合截图和人工检查。

## 示例提示词

```text
请使用 personal-style-slides skill。
以 assets/templates/my_template.pptx 作为风格模板，根据 proposal.docx 生成一份 8 分钟博士开题报告 HTML 演示文稿。
```

```text
请使用 personal-style-slides skill。
这个旧 deck 是我认可的风格，请把新内容改成类似的版式节奏、图文比例和图注风格。
```

```text
请使用 personal-style-slides skill。
根据这些模拟结果生成一份组会汇报，风格尽量贴近 assets/templates/ 里的模板。
```

## Demo

见 `examples_demo/demo_template_seed/`：

```text
input/demo_template.html
input/research_notes.md
output/style_profile.auto.json
output/style_summary.auto.md
```

这个 demo 展示了基本路径：

```text
模板种子 -> 风格摘要/画像 -> 个性化 deck 生成
```

demo 使用合成材料，不包含私人数据。

## 仓库结构

```text
personal-style-slides/          # 安装这个目录作为 skill
  SKILL.md
  agents/
  assets/
  references/
  scripts/

examples_demo/                  # 可公开的合成 demo
README.md
README_EN.md
requirements.txt
THIRD_PARTY_NOTICES.md
LICENSE
```

## 隐私

请把私人材料留在本地，不要提交到公开仓库，包括：

- 真实模板或旧演示文稿
- 未发表结果图或保密项目图片
- 机构 logo
- 导师或客户批注
- 个人 style memory
- 商业字体或系统字体文件

这个仓库用于发布 skill 框架，而不是发布个人内容。

## 局限

- 这是 skill 包，不是独立 slide 应用、Web 应用或完整 CLI 产品。
- 风格提取只是紧凑风格种子，不是完整视觉重建。
- 风格指纹比较只是辅助提示，不能证明视觉相似。
- 静态 HTML 检查不能证明浏览器渲染后没有重叠。
- 浏览器渲染验证依赖 Playwright 或本地浏览器。

## Credits

Created by @MV with Codex.

## License

MIT