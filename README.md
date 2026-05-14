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
静态检查 + 可选浏览器渲染验证
        |
        v
用户反馈修改
        |
        v
经用户允许后写入本地风格记忆
```

## 功能优势

- 从你自己的 PPTX、HTML、PDF、旧 deck 或截图中学习风格，而不是套用通用主题。
- 保留页面节奏、字体层级、内容密度、图文比例、图注处理、页脚样式等个人习惯。
- 针对科研场景增加保护：保留科学表述、来源图片、证据链和不确定性说明。
- 输出浏览器可打开的 HTML slides，并支持 print/PDF。
- 内置辅助脚本：source inspection、style profile 提取、静态检查、浏览器渲染验证、style memory 更新。
- 隐私优先：真实模板、未发表结果图、机构 logo、导师批注、商业字体和个人 style memory 都留在本地。

## 安装

这个仓库的根目录不是 skill。真正需要安装的是内层目录：

```text
personal-style-slides/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

### 安装到 Codex

Windows PowerShell：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\"
```

macOS/Linux：

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

如果你的 Codex skills 目录不同，请把目标路径替换为实际目录。

### 安装到 Claude

macOS/Linux：

```bash
git clone https://github.com/m925855108/personal-style-slides.git
mkdir -p ~/.claude/skills
cp -r personal-style-slides/personal-style-slides ~/.claude/skills/
```

Windows PowerShell：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.claude\skills\"
```

如果你的 Claude 客户端使用不同的 skills 目录，请按实际路径复制。

### 下载 ZIP 安装

从 GitHub 下载 ZIP，解压后只复制内层 `personal-style-slides/` 文件夹到 Codex 或 Claude 的 skills 目录。不要复制整个仓库根目录。

## 快速开始

安装可选依赖：

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

检查本地环境：

```bash
python personal-style-slides/scripts/doctor.py
```

把你认可的模板或旧 deck 放到：

```text
personal-style-slides/assets/templates/
```

提取风格种子：

```bash
python personal-style-slides/scripts/extract_style_profile.py \
  personal-style-slides/assets/templates/my_template.pptx \
  --out-dir style_profile_output
```

生成 deck 后运行检查：

```bash
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

PPTX 视觉渲染需要 LibreOffice 完成 PPTX 到 PDF 的转换，并需要 PyMuPDF 将 PDF 页面渲染为 PNG。如果缺少这些工具，PPTX 检查会降级为 OOXML 元数据提取。

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

## License

MIT
