# Personal Style Slides

让 Codex / Claude 学你的模板，然后按你的审美生成 HTML slides。

中文 | [English](README_EN.md)

<!-- TODO: Add a small before/after screenshot once a public demo deck is ready. -->

## 为什么做这个

做科研汇报最烦的地方，往往不是“做一页 slide”，而是每次都要重新找回自己的风格：标题怎么放、图多大、文字密度多少、图注放哪里、页脚怎么对齐。

通用模板能帮一点，但很容易变成别人的 PPT。这个 skill 的思路比较直接：

```text
你认可的模板 / 旧 deck / 截图
        |
        v
提取一个紧凑的风格种子
        |
        v
让 Codex / Claude 按这个风格生成或修改 HTML slides
        |
        v
你反馈后，再决定要不要写入本地风格记忆
```

它主要为博士开题、答辩、组会、文献汇报、模拟结果汇报和学术演示准备。也可以用在别的个性化 slide 场景，只要你的目标是“按我的模板和审美来”，而不是套一个通用主题。

先说清楚边界：**默认输出是浏览器可打开的 HTML slides，不是 PowerPoint 里可继续编辑的原生 `.pptx` 文件。** PPTX 可以作为风格参考或素材来源，但这个项目目前不是高保真 PPTX 复刻器，也不是一键 PPTX 生成器。

## 核心特性

- **模板驱动**：从你认可的 PPTX、HTML deck、PDF、旧 deck 或截图里学习风格。
- **个人化优先**：保留你的标题习惯、图文比例、内容密度、图注风格和页面节奏。
- **HTML-first**：默认生成 `index.html` + 本地资源目录，适合浏览器演示和 PDF/print 方向检查。
- **科研友好**：强调真实图像、来源追踪、谨慎表述，不鼓励随便换图或编结论。
- **版式安全护栏**：提供 `layout_safety.css` 和渲染后 DOM 检查，尽量减少拥挤、溢出和遮挡。
- **风格指纹比较**：用可解释的颜色、字号、密度、图文比例和 layout motif 比较结果是否偏离模板。
- **轻量风格记忆**：只有你明确同意时，才把长期偏好写入本地 `style_memory`。
- **可降级检查**：有 Playwright 就做渲染验证；没有也会跑静态检查，并说明哪些东西没验证。
- **隐私默认本地**：真实模板、未发表图、机构 logo、导师批注和个人风格记忆都不应该提交到公开仓库。

## 快速开始

这个仓库有两层。真正要安装的是里面的 skill 子目录，不是仓库根目录。

```text
repo root/
  README.md
  README_EN.md
  requirements.txt
  examples_demo/

  personal-style-slides/   # 安装这个目录
    SKILL.md
    agents/
    assets/
    references/
    scripts/
```

如果你使用支持 GitHub URL 的 skill installer，请指向子目录：

```text
https://github.com/m925855108/personal-style-slides/tree/main/personal-style-slides
```

Codex installer 示例：

```bash
python install-skill-from-github.py --repo m925855108/personal-style-slides --path personal-style-slides --dest D:/CodexSkills
```

如果直接给仓库根地址：

```text
https://github.com/m925855108/personal-style-slides
```

安装器可能会报错，因为它不知道哪个子目录才是真正的 skill。

### 手动安装到 Codex

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.codex/skills/
```

Windows PowerShell：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.codex\skills\personal-style-slides"
```

### 手动安装到 Claude

```bash
git clone https://github.com/m925855108/personal-style-slides.git
cp -r personal-style-slides/personal-style-slides ~/.claude/skills/
```

Windows PowerShell：

```powershell
git clone https://github.com/m925855108/personal-style-slides.git
Copy-Item -Recurse .\personal-style-slides\personal-style-slides "$env:USERPROFILE\.claude\skills\personal-style-slides"
```

如果你的客户端使用不同的 skills 目录，把目标路径换成实际路径即可。安装后如果没立刻识别，重启 Codex / Claude。

可以用这个 prompt 检查是否加载成功：

```text
请检查 personal-style-slides skill 是否可用，并概括它适合做什么。
```

## 跑一个 demo

仓库里有一个合成 demo，不含私人数据。它不是复杂 PPTX 继承能力展示，只是确认脚本链路能跑通。

```bash
python examples_demo/run_demo.py
```

输出会写到：

```text
examples_demo/demo_template_seed/run_output/
```

这个 demo 会做几件事：

- 检查环境能力
- 从 demo HTML 模板提取风格画像
- 提取轻量风格指纹
- 对 demo HTML 做静态检查

## 常见用法

### 1. 根据模板生成科研汇报

把你认可的模板放进本地 skill 的 `assets/templates/`，然后对 Codex / Claude 说：

```text
请使用 personal-style-slides skill。
以 assets/templates/my_template.pptx 作为风格模板，根据 proposal.docx 生成一份 8 分钟博士开题报告 HTML 演示文稿。
```

### 2. 按旧 deck 风格改新内容

```text
请使用 personal-style-slides skill。
这个旧 deck 是我认可的风格，请把新内容改成类似的版式节奏、图文比例和图注风格。
```

### 3. 快速做组会结果汇报

```text
请使用 personal-style-slides skill。
根据这些模拟结果生成一份组会汇报，风格尽量贴近 assets/templates/ 里的模板。
```

### 4. 只改一两页

```text
请使用 personal-style-slides skill。
只调整第 3 页，让左侧图更大，右侧解释文字保持三条以内，不要重新设计整套 deck。
```

小改动应该走轻流程。这个 skill 不应该因为你换一张图，就重新跑完整风格学习和正式审计。那样很烦，也没必要。

## 工具脚本

这些脚本是给 agent 调用的辅助工具。你也可以手动跑。它们不是固定流水线，不需要每次全部执行。

| 脚本 | 做什么 | 常见时机 |
| --- | --- | --- |
| `doctor.py` | 检查 Python、浏览器、LibreOffice、PyMuPDF、Playwright 等环境能力。 | 安装后、脚本失败、浏览器验证不可用。 |
| `inspect_sources.py` | 检查 PPTX、DOCX、PDF、HTML、LaTeX 或截图目录里的文字、图片、页面和模板信息；PPTX 会尝试提取字体、字号和粗略几何线索。 | 有源文档、模板或素材目录时。 |
| `extract_style_profile.py` | 从模板、旧 deck、PDF、HTML 或截图里提取紧凑风格种子。 | 生成或大改 deck 前。 |
| `check_html_deck.py` | 静态检查 HTML slides 的 section、图片路径、重复图片和风险 CSS。 | 生成 HTML 后。 |
| `verify_rendered_deck.py` | 用 Playwright 或本地浏览器做渲染检查、截图和 DOM box 检查。 | 布局风险较高，或需要截图证据时。 |
| `extract_style_fingerprint.py` | 提取轻量风格指纹，包括颜色、字号、密度、图文比例、layout motif 和 CSS/class 线索。 | 要比较模板和生成结果时。 |
| `compare_style_fingerprint.py` | 比较两个风格指纹，报告匹配、漂移和需要人工复核的地方。 | 检查结果是否大体保留模板风格。 |
| `update_style_memory.py` | 查看、追加或移除本地 style memory。 | 只有你明确同意长期记住某个偏好时。 |
| `style_utils.py` | 内部公共函数。 | 通常不用直接跑。 |

`assets/layout_safety.css` 不是主题模板，而是一组中性的版式安全护栏：标题区、内容区、页脚区预留空间，限制图片高度，并用 grid/flex 减少 HTML slide 里常见的拥挤和遮挡。正式做 deck 时可以按你的模板风格改色、改间距，但不建议删掉这些安全边界。

对自定义 HTML，`verify_rendered_deck.py --generic-mode` 可以减少“不是 Reveal.js 就无法验证”的问题；如果报告 `verification-incomplete`，说明截图可能有了，但 DOM 重叠检查没有真正完成。

手动跑几个常见检查：

```bash
python personal-style-slides/scripts/doctor.py
python personal-style-slides/scripts/extract_style_profile.py personal-style-slides/assets/templates/my_template.pptx
python personal-style-slides/scripts/check_html_deck.py outputs/index.html
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --out-dir render_check
```

如果输出是自定义 HTML，而不是 Reveal.js deck，渲染检查建议加：

```bash
python personal-style-slides/scripts/verify_rendered_deck.py outputs/index.html --generic-mode --out-dir render_check
```

`--generic-mode` 会用 `[data-slide]` / `.slide` / `section` 来枚举页面。它是为了让个性化 HTML 也能被检查，不是要求所有 deck 都必须长成 Reveal.js。

## 配置和依赖

skill 本体可以直接安装。下面这些依赖只影响辅助脚本能力：

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

依赖能力大概是这样：

| 环境能力 | 能做什么 | 限制 |
| --- | --- | --- |
| 无额外依赖 | 安装 skill、读取说明、生成/修改 HTML slides、运行部分标准库脚本。 | PDF/PPTX 视觉解析和浏览器 DOM 验证会降级。 |
| `PyMuPDF` / `pypdf` | 改善 PDF 文本、图片和页面渲染读取。 | PDF 里的矢量图、组合图和复杂版式仍可能需要截图或人工裁剪。 |
| LibreOffice + PyMuPDF | 尝试 PPTX -> PDF -> PNG 页面渲染，把 PPTX 页面截图作为视觉参考。 | 仍不是完整 PPTX 语义解析，不能保证还原每个 shape、裁剪或动画。 |
| Playwright + Chromium | 做更可靠的浏览器截图、DOM box、溢出和加载检查。 | 只能降低风险，不能替代最终人工看图。 |

默认建议把用户自己的材料放在本地安装目录里：

```text
personal-style-slides/
  assets/
    templates/      # 你的模板、旧 deck、HTML starter
    examples/       # 你认可的历史示例，可选
    style_memory/   # 长期偏好和负面偏好，只在你同意时写入
```

不要把真实模板、未发表结果图、机构 logo、导师批注、个人 style memory、商业字体或系统字体提交到公开仓库。

## 测试

仓库包含最小 smoke tests：

```bash
python -m unittest discover tests
```

这些测试覆盖：

- HTML 静态检查
- 缺失图片报错
- demo 风格画像提取
- 风格指纹比较

它们能防止脚本升级时静默坏掉，但不代表完整视觉质量验收。

## 现在还做不到什么

直接说，别期待它现在解决所有 slide 问题。

- 它是 skill 包，不是独立 Web app，也不是完整 CLI 产品。
- 默认生成 HTML slides，不直接生成可编辑 `.pptx`。
- 风格提取是紧凑风格种子，不是完整视觉重建。
- PPTX 可以作为模板和素材来源，但不能保证高保真复刻 PowerPoint 版式、裁剪、动画或所有 shape 语义。
- 风格指纹比较只是辅助判断，不能证明“看起来完全像”。它更像一组可解释的个人风格特征，不是训练出来的小模型。
- 静态 HTML 检查不能证明浏览器渲染后没有重叠。
- 浏览器渲染验证会检查更多风险，比如标题/正文/页脚冲突、文本密度、多图拥挤和中间窄带布局；但最后还是建议人工看截图。

## 贡献

欢迎提 issue 或 PR。比较有价值的方向：

- 更好的 demo，特别是多页中文科研汇报和复杂图文场景。
- 更强的 PPTX 页面截图和 layout fingerprint。
- 更稳的浏览器渲染检查。
- 更多测试用例，尤其是缺图、溢出、字体、公式和多图场景。
- 文档里的真实使用案例和失败案例。

提交前建议至少跑：

```bash
python examples_demo/run_demo.py
python -m unittest discover tests
```

如果改了 skill 本体，也建议用 Codex 的 skill validator 检查 `personal-style-slides/` 目录。

<!-- TODO: Add CONTRIBUTING.md if external contributions become frequent. -->

## Credits

Created by @MV with Codex.

## License

MIT
