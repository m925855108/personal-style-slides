# Changelog / 更新日志

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
