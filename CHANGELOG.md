# Changelog / 更新日志

## 2026-05-21

### English

#### Improved

- Enhanced `scripts/inspect_sources.py` to extract lightweight PPTX OOXML style
  clues:
  - font typefaces;
  - font sizes in points;
  - text style records;
  - coarse shape geometry summaries;
  - per-slide geometry samples.
- Updated `scripts/extract_style_profile.py` so PPTX font and geometry clues
  flow into the compact style profile and Markdown summary.
- Updated `scripts/extract_style_fingerprint.py` and
  `scripts/compare_style_fingerprint.py` so style fingerprints can compare font
  families and geometry availability.
- Updated skill guidance and docs to treat OOXML data as first-pass personal
  style fingerprint evidence, not full PowerPoint reconstruction.

#### Notes

- This is a deterministic, inspectable improvement for early template learning.
  It does not train a model and does not guarantee high-fidelity PPTX cloning.

### 中文

#### 改进

- 增强 `scripts/inspect_sources.py`，现在会尝试提取轻量 PPTX OOXML 风格线索：
  - 字体名称；
  - 字号 pt；
  - 文本样式记录；
  - 粗略 shape 几何摘要；
  - 每页几何样例。
- 更新 `scripts/extract_style_profile.py`，让 PPTX 字体和几何线索进入紧凑风格画像和 Markdown 摘要。
- 更新 `scripts/extract_style_fingerprint.py` 和
  `scripts/compare_style_fingerprint.py`，让风格指纹可以比较字体家族和几何线索可用性。
- 更新 skill 说明和文档，明确 OOXML 数据是初始个人风格指纹证据，不是完整 PowerPoint 复刻。

#### 说明

- 这是面向早期模板学习的确定性、可检查改进；它不是训练模型，也不保证高保真 PPTX 克隆。

## 2026-05-21 Phase B

### English

#### Added

- Added `--generic-mode` to `scripts/verify_rendered_deck.py` so custom HTML
  decks can be checked through `[data-slide]`, `.slide`, and `section` markers
  instead of relying only on Reveal.js structure.

#### Improved

- `verify_rendered_deck.py` now waits for Reveal.js readiness when possible and
  reports `verification-incomplete` when screenshots exist but DOM item
  detection fails.
- Updated `SKILL.md`, README, and the layout-safety reference to document the
  Reveal.js path, custom HTML path, and verification downgrade behavior.
- Clarified that layout constraints are first-generation safety guardrails; user
  templates and approved style memory may tune the values while preserving
  verifiable slide structure.

#### Notes

- Custom HTML remains supported. It should keep `data-slide` or compatible slide
  markers if the user wants rendered DOM verification.

### 中文

#### 新增

- 为 `scripts/verify_rendered_deck.py` 新增 `--generic-mode`，让自定义 HTML
  deck 可以通过 `[data-slide]`、`.slide` 和 `section` 标记进行检查，而不是只依赖
  Reveal.js 结构。

#### 改进

- `verify_rendered_deck.py` 现在会尽量等待 Reveal.js 初始化；如果截图存在但 DOM
  内容检测失败，会报告 `verification-incomplete`，不再把这类情况当成完整通过。
- 更新 `SKILL.md`、README 和 layout-safety 参考文档，说明 Reveal.js 路径、自定义
  HTML 路径以及验证降级行为。
- 明确布局限制只是初次生成的安全护栏；用户模板和已确认的风格记忆可以调整这些值，但应保留可验证的 slide 结构。

#### 说明

- 自定义 HTML 仍然被支持。如果用户希望进行渲染后 DOM 验证，应保留 `data-slide`
  或兼容的 slide 标记。

## 2026-05-21 初步稳定化

### English

#### Added

- Added `assets/unified-type-scale.css` as the default role-based typography
  baseline for generated decks.
- Added `assets/unified-image-scale.css` as the default role-based figure-size
  baseline for generated decks.
- Added `assets/slide-shell-reveal.html` and `assets/slide-shell-custom.html`
  as copyable title/content/footer slide skeletons.

#### Improved

- Updated `SKILL.md` so new decks and substantial redesigns start from the
  shared layout, type, image, and shell assets.
- Made the guardrails customizable: users may override values to match personal
  style, but should keep variable names and role classes for verification.
- Enhanced `scripts/check_html_deck.py` with optional `--strict-layout` checks
  for missing type/image variables, unreadably small font sizes, excessive raw
  font-size variance, image-height variance, and unmarked custom slides.
- Updated the layout-safety reference with the customizable baseline and static
  preflight rules.

#### Notes

- These changes are an initial stabilization pass. They do not force one visual
  style; they provide a shared structure that can mature with user-specific
  preferences.

### 中文

#### 新增

- 新增 `assets/unified-type-scale.css`，作为生成 deck 时基于角色的默认字号体系。
- 新增 `assets/unified-image-scale.css`，作为生成 deck 时基于角色的默认图片尺寸体系。
- 新增 `assets/slide-shell-reveal.html` 和 `assets/slide-shell-custom.html`，
  作为可复制的标题区 / 内容区 / 页脚区页面骨架。

#### 改进

- 更新 `SKILL.md`，要求新建 deck 或大改 deck 时优先从共享的 layout、type、image
  和 shell assets 开始。
- 明确保留个性化空间：用户可以根据个人模板或长期风格记忆覆盖变量值，但应保留变量名和角色类名，方便后续验证。
- 增强 `scripts/check_html_deck.py`，新增可选 `--strict-layout` 检查：
  缺失字号/图片变量、字号过小、原始字号过多、图片高度过散、自定义 slide 未标记等。
- 更新 layout-safety 参考文档，加入“可个性化的基线”和静态预检查规则。

#### 说明

- 这是初步稳定化修改。它不会强制所有用户使用同一种视觉风格，而是提供一套可被个人习惯逐渐覆盖和完善的共享结构。

## 2026-05-20

### English

#### Added

- Added `assets/layout_safety.css` as neutral guardrails for HTML slide layout:
  reserved title/content/footer regions, viewport-safe figures, grid/flex
  constraints, and responsive density protection.
- Added `references/layout-safety-and-style-fingerprint.md` to document two
  core reliability ideas:
  - layout checks reduce overlap/crowding risk but cannot mathematically prove
    perfect rendering;
  - personal style should be treated as an explainable fingerprint before any
    small-model style learning is attempted.

#### Improved

- Enhanced `scripts/verify_rendered_deck.py` with rendered layout warnings for:
  - title/content overlap;
  - footer/content overlap;
  - dense text;
  - excessive bullet count;
  - too many visible elements;
  - multi-figure crowding;
  - central-band content placement.
- Enhanced `scripts/extract_style_fingerprint.py` to include:
  - fingerprint version;
  - font pixel tokens;
  - image-per-slide ratio;
  - image density bucket;
  - layout motifs;
  - CSS/class hints;
  - rendered-reference availability.
- Enhanced `scripts/compare_style_fingerprint.py` to compare:
  - font scale;
  - layout motifs;
  - image density;
  - image-per-slide drift;
  - rendered-reference availability.
- Updated `SKILL.md` to make layout safety and explainable personal style
  fingerprints part of the workflow.
- Updated Chinese and English README files to describe the new layout-safety
  and style-fingerprint behavior clearly.

#### Notes

- These changes still do not claim perfect visual guarantees. Browser-rendered
  checks reduce risk; final screenshot review remains recommended.
- Style fingerprints are rule-based and explainable. They are not trained small
  models and should not be described as full visual style recognition.

### 中文

#### 新增

- 新增 `assets/layout_safety.css`，作为 HTML slides 的中性版式安全护栏：
  预留标题区、内容区、页脚区，限制图片在视口中的尺寸，并通过 grid/flex
  约束降低内容拥挤、溢出和遮挡的风险。
- 新增 `references/layout-safety-and-style-fingerprint.md`，说明两个核心可靠性原则：
  - 版式检查可以降低重叠和拥挤风险，但不能数学意义上证明渲染结果绝对完美；
  - 个人风格应先被表示为可解释的风格指纹，再考虑是否需要小模型式的风格学习。

#### 改进

- 增强 `scripts/verify_rendered_deck.py`，新增渲染后版式风险提示：
  - 标题和正文重叠；
  - 页脚和正文重叠；
  - 文本过密；
  - bullet 数量过多；
  - 可见元素过多；
  - 多图页面过于拥挤；
  - 内容被压缩在中间窄带。
- 增强 `scripts/extract_style_fingerprint.py`，风格指纹现在包含：
  - 指纹版本；
  - 字号像素 token；
  - 每页图片比例；
  - 图片密度分组；
  - layout motif；
  - CSS/class 线索；
  - 是否存在渲染后的参考页面。
- 增强 `scripts/compare_style_fingerprint.py`，现在会比较：
  - 字号尺度；
  - layout motif；
  - 图片密度；
  - 每页图片比例漂移；
  - 渲染参考页可用性。
- 更新 `SKILL.md`，把版式安全和可解释个人风格指纹纳入正式 workflow。
- 更新中英文 README，更清楚地说明新版 layout safety 和 style fingerprint 的作用与边界。

#### 说明

- 这些改动仍然不声称可以保证视觉结果绝对无重叠。浏览器渲染检查能降低风险，但最终仍建议人工查看截图。
- 风格指纹是规则化、可解释的辅助判断，不是训练出来的小模型，也不应被描述为完整视觉风格识别。
