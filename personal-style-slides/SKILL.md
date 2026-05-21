---
name: personal-style-slides
description: Create personalized HTML slide decks by learning from the user's approved templates, prior decks, screenshots, and feedback. Use when Codex needs to generate or revise a presentation that preserves the user's established visual style, slide rhythm, typography, density, layout habits, figure treatment, and communication preferences. Optimized for research and academic presentations, but usable for other personalized slide work when source traceability, readable projection geometry, browser-render verification, PDF/print support, and clear downgrade notes are important.
---

# Personal Style Slides

## Overview

This is not a universal slide-design system. It is a template-seeded, feedback-refined personal HTML slide workflow, optimized for research and academic presentations. The user does not need to manually build a style library: an approved template, old deck, or screenshot is the style seed; conversation feedback becomes reusable style memory only when the user approves or uses clear long-term wording.

This skill is HTML-first. It generates or revises browser-based slide decks, usually `index.html` plus local assets. It can inspect PPTX files as sources or style seeds, but it does not directly generate high-fidelity editable `.pptx` output unless the user separately provides or requests a dedicated PPTX conversion workflow.

Prioritize preserving the user's established visual grammar while keeping scientific claims traceable, figures source-backed, text readable for projection, and rendered slides free of avoidable layout failures.

## Priority Order

1. Scientific correctness and source traceability.
2. Explicit user instruction in the current conversation.
3. Current user-provided template, prior deck, screenshot, or approved example.
4. Accepted long-term style memory in `assets/style_memory/`, merged only when it does not conflict with the current style seed.
5. Auto-extracted style profile from the current style seed.
6. Layout readability and browser-render verification.
7. Default academic fallback.

Research and verification rules are guardrails. They prevent scientific, readability, and delivery failures. They should not override the user's approved visual style unless that style causes unreadability, overlap, broken delivery, or scientific misrepresentation.

## Workflow Profiles

Choose the lightest profile that can safely satisfy the request. If uncertain, prefer `draft-build` rather than `formal-build`.

### quick-fix

Use for localized edits to an existing deck: one-slide correction, typo fix, image replacement, spacing/layout adjustment, color/style tuning, export-path repair, or a small interaction fix.

- Do not stop for outline confirmation.
- Inspect only affected HTML/CSS/assets plus nearby template rules.
- Preserve the deck's existing user style unless the requested fix requires a style change.
- Run `scripts/check_html_deck.py` when an HTML file is changed.
- Use browser/render verification only when the change can plausibly affect overlap, sizing, image rendering, navigation, or print output.
- Final response should include changed file, checks run, and any visual risk not rendered.

### draft-build

Use for a first version, rough group-meeting deck, paper introduction, exploratory research report, or quick personalized presentation.

- Produce a concise outline and proceed unless the user asked to review first or the science is ambiguous.
- Select 1-3 closest user examples when available and imitate their visual rhythm before using fallback academic style.
- If the user provides a template or old deck, run or emulate template-based style learning and treat it as the current style contract.
- Use source images and templates when available, but keep the confirmation artifact short.
- Use a light risk table: `Slide | Potentially risky claim | Needs confirmation`.
- Prefer `portable-folder` output. CDN is acceptable only when speed matters or the user approves.
- Run static checks and render verification when a browser is available or the deck is layout-sensitive.

### formal-build

Use when the user explicitly says proposal, defense, thesis, qualifying report, official/final presentation, advisor review, conference talk, or when source accuracy and template inheritance are critical.

- Inspect relevant user examples, style memory, template/source materials before building.
- Treat the current template/deck/screenshot as the style seed and extract a compact style profile before designing.
- Prepare a personal style contract, source/image manifest, and claim-source table.
- Ask for content confirmation before final HTML unless the user explicitly requests direct generation.
- If the user requests direct generation, build the deck and include unconfirmed assumptions in the risk report.
- Ask once before saving a reusable Markdown memory file after first substantial inspection of a reusable template/source.
- Ask about multi-figure slides only when figures would be too small; otherwise choose split slides or a zoomable layout based on readability.
- Confirm browser choice before external browser automation unless the user already specified an available browser.
- Run static and render verification when available; otherwise clearly downgrade the verification claim.

## Failure Downgrade Protocol

- If browser render verification is unavailable, run static checks and state: "Static checks passed, but rendered overlap was not verified."
- If source image extraction fails, use page-rendered screenshots or manually cropped regions when possible. Mark the source as `page-rendered fallback` and ask only if the fallback changes scientific meaning.
- If template parsing fails, use screenshots/style observation fallback and mark template inheritance as approximate.
- If PPTX visual rendering is needed, it requires LibreOffice for PPTX-to-PDF conversion and PyMuPDF for PDF-page-to-PNG rendering. Without both, fall back to OOXML metadata and state that visual slide screenshots were not extracted.
- If a scientific claim has no clear source in `formal-build`, put it in the risk table and use cautious wording or omit it.
- If PPTX/PDF/DOCX tooling is missing, do not invent missing figures, fonts, or layouts. Report the limitation and use the best available fallback.

## Core Principles

1. **Content Before Code** - Draft the slide outline and key text first. In `formal-build`, wait for user confirmation unless direct generation was requested. In `draft-build`, proceed after a concise outline unless the user asked to review first or the science is ambiguous. In `quick-fix`, do not stop for outline confirmation.
2. **Scientific Accuracy First** - Preserve source conclusions, figure meanings, equations, model names, and conditional claims. Do not simplify a research claim into a stronger or different claim.
3. **PPT-Like Geometry** - Every slide must occupy a consistent visual frame. Titles, content blocks, figures, footers, page numbers, and section markers should align across the deck.
4. **Projection Readability First** - Do not solve layout pressure by shrinking body text. Increase usable layout space, redistribute content vertically, and split slides before making text hard to read.
5. **No Overflow, No Cramping** - Keep each slide within one viewport. If content does not fit with comfortable line height and balanced whitespace, split it into another slide.
6. **Show the Research** - Use real figures, diagrams, equations, flowcharts, timelines, and data visualizations. Decorative visuals are secondary to scientific explanation.
7. **Example-Led Personal Style** - Check `assets/examples/`, `assets/style_memory/`, and user-provided prior decks/screenshots before inventing a new visual system. Imitate approved examples before applying any default academic style.
8. **Source Images By Default** - Use images from the supplied documents, extracted assets, or templates by default. Do not replace document figures with unrelated generated images, web images, or placeholders unless the user explicitly approves that substitution.
9. **Evidence Over Aesthetics** - In research decks, figures, equations, tables, and source-backed diagrams are first-class content. Decorative visuals must never displace evidence.
10. **Imitate, Do Not Blindly Copy** - Preserve the user's visual grammar, but adapt layout density, figure scale, and slide splitting to the new scientific content.
11. **Use Explainable Style Fingerprints** - Treat personal style as a set of comparable traits: canvas, title/footer habits, density, color, type scale, layout motifs, figure treatment, caption style, and image/text ratio. Do not claim a trained style model exists unless one was actually used.
12. **Be Honest About Output** - Do not describe the result as editable PowerPoint output unless a real `.pptx` file was produced and verified. For this skill, the default deliverable is an HTML slide deck.

## Phase 0: Detect Scenario

Determine the research scenario and let it tune density, confirmation, and visual rhythm:

- **Group meeting / work-in-progress** - faster iteration, more process figures, 4-6 main bullets allowed, lighter confirmation.
- **Paper introduction / literature report** - large source figures, clear claim-source mapping for conclusions, concise narrative.
- **Simulation or code result report** - workflow, parameter table, validation/result comparison, failure cases, reproducibility notes.
- **Research plan** - objectives, route map, risks, timeline, expected outcomes.
- **Proposal / qualifying / defense / advisor review** - formal-build, strict source tracing, stable template, fewer bullets, minimal decorative motion.
- **Conference talk** - strong story, larger figures, less text, speaker notes where useful.
- **Focused modification** - quick-fix unless the requested change alters scientific meaning or template-wide structure.
- **Template setup** - add or adapt user templates in `assets/templates/` for future decks.
- **Style profile setup** - add approved examples, screenshots, style memories, or rejected examples for future personalization.

For Mode B or C, read the existing file first and preserve user-approved content unless the user explicitly asks to rewrite it.

## Phase 0.5: Template-Based Style Learning

Before designing a new deck or substantial redesign, learn from the current style seed:

- If the user supplies a template, old deck, or screenshot, use it as the style seed.
- If no file is supplied, look for the most relevant approved template/example in `assets/templates/` or `assets/examples/`.
- Run or emulate `scripts/extract_style_profile.py` to create a compact style summary for the current task.
- Merge `assets/style_memory/` only when it does not conflict with the current style seed or current user instruction.
- Do not require the user to manually organize examples or maintain a style library.
- For PPTX style seeds, prefer the OOXML-derived font family, font size, and coarse geometry fields when available. These are style clues, not a promise of exact PowerPoint reconstruction.

When several examples exist, select the closest 1-3 by:

1. research scenario
2. slide role
3. visual structure
4. figure/text ratio
5. language and density
6. user approval status

Create a compact current-task style contract with:

- visual density and whitespace habits
- title style: short/long, declarative/traditional, section-like/story-like
- layout archetypes: two-column, card modules, left nav, section divider, figure-first, workflow, timeline
- color and material preferences
- typography habits and size hierarchy
- figure/caption treatment: borders, labels, numbering, shadows, crop behavior
- diagram style: flat/vector/transparent/physically plausible/annotated
- section/navigation/footer habits
- text tone: proposal formality, group-meeting brevity, conference narrative
- known dislikes and rejected patterns
- allowed modernization level
- examples/templates to imitate and rejected patterns to avoid

For early-stage personalization, prefer a deterministic style fingerprint over a vague style description:

- Use rendered screenshots when available because they preserve title placement, footer placement, spacing, and visual motifs better than file metadata alone.
- Extract a compact fingerprint with `scripts/extract_style_fingerprint.py` when comparing a reference deck/template against a generated deck.
- Compare generated output with `scripts/compare_style_fingerprint.py` when the user explicitly cares about template fidelity or when a previous attempt drifted from the user's style.
- Treat fingerprint output as advisory. It is a structured similarity check, not proof that the deck fully matches the user's aesthetic.

After delivery or user feedback:

- Summarize accepted visual traits.
- Summarize rejected visual traits.
- Distinguish one-time task feedback from reusable style preference.
- Save reusable preferences only when the user approves or uses clear long-term wording such as "always do this later", "avoid this later", or "remember this style".
- Append to `assets/style_memory/user_feedback_log.md` rather than overwriting old memory.

If no style seed or style memory exists, use the default academic fallback and ask after delivery whether to save the generated deck as the first style reference.

## Phase 1: Style, Template, And Source Audit

Inventory the available materials:

- Source documents: reports, papers, thesis chapters, notes, advisor comments.
- Existing presentations: PPTX, HTML, screenshots, template decks.
- Research assets: figures, tables, equations, simulation plots, diagrams, logos.
- Talk constraints: duration, audience, defense/proposal/conference context, required sections, language.

Inspect user examples and templates before designing:

- If user examples exist, imitate examples before inventing a new visual system.
- If a style memory exists, treat it as persistent preference context unless the current user request overrides it.
- If the user names a template, use that template.
- If `assets/templates/` contains exactly one plausible template, use it by default and state that choice.
- If multiple plausible templates exist and the user did not name one, ask which template to use before final HTML. You may still draft content while waiting, but do not finalize style.
- For PPTX templates, infer style from slide size, title/footer placement, colors, typography, recurring shapes, and sample slide screenshots if extraction tools are available.
- When `scripts/inspect_sources.py` reports PPTX font typefaces, font sizes, or geometry summaries, use them to seed the type scale, title/content/footer placement, and layout fingerprint before falling back to generic academic defaults.
- For LaTeX Beamer templates, infer style from theme declarations, color themes, title/frame commands, section structure, logo usage, and included figure patterns.
- For HTML/CSS templates, reuse the layout grammar and CSS tokens directly where practical.
- Treat approved user examples as the primary design source and templates as implementation sources. For each generated slide type, choose the closest prior example or template exemplar and adapt its structure before inventing a new layout.

Create a personal style contract first. If a current template is also used, add a template-style contract below it:

- canvas ratio and slide shell
- title, subtitle, content, footer, and page-number positions
- color tokens and accent rules
- typography scale for title, section labels, body, captions, and footnotes
- grid rules for text-only, figure-text, section, timeline, and conclusion slides
- recurring visual motifs such as rules, sidebars, labels, frames, and logo/watermark placement
- exemplar mapping: which template slide or layout pattern will guide each output slide type
- style similarity targets: which example slide/screenshots each output slide should resemble and which traits should be preserved

Inventory images before outlining:

- Extract or list images from source DOCX/PPTX/PDF/HTML when possible.
- Identify figure numbers, captions, source paths, and what each image shows.
- When the prompt names a figure such as "Figure 3" or "Figure 13", use that exact source image if available.
- If a required image cannot be found or extracted, ask the user before substituting.
- Prefer embedding/copying the actual extracted image asset into the HTML workflow. Use custom diagrams only for concepts not already covered by the source figures or when the user requests a replacement.
- If multiple source figures are planned for one slide and each would become too small for projection, either split the slide or ask whether to keep the multi-figure layout with zoom interaction.

Use bundled source-inspection scripts when they save time or reduce uncertainty:

- Run `scripts/inspect_sources.py` for PPTX, DOCX, HTML, LaTeX, and PDF inputs when source/image inventory or template style extraction is needed.
- Run `scripts/extract_style_profile.py` when a template, old deck, screenshot, or screenshot directory should become the style seed for the current deck.
- For PPTX inputs, prefer a hybrid approach: parse OOXML metadata when available and render representative slides to images when tooling allows. Use parsed metadata for text/media inventory, not as the sole source of template geometry.
- For PDF inputs, extract embedded raster images when available and allow page-level rendering fallback. When figure boundaries are uncertain, use page screenshots or manually cropped regions rather than claiming exact figure extraction.
- When a source or template is likely to be reused, ask after the first inspection whether to write a concise Markdown memory file near the output or in an agreed notes location.
- Do not load large generated Markdown summaries into context unless the current task needs them; use targeted search inside them.

Extract and separate:

- **Facts** - claims directly supported by the source.
- **Narrative links** - how one slide motivates the next.
- **User-fixed wording** - text or conclusions the user has corrected and should not be changed.
- **Unclear items** - claims, figure meanings, or terminology that need user confirmation.

## Phase 2: Outline Before HTML

Prepare a slide outline before writing the final HTML:

- Use one row per slide: slide number, title, purpose, core bullets, figure/visual, speaker note intent.
- For every slide with an image, include image source: document filename, figure number/caption if known, extracted asset path, or template asset.
- For every multi-figure slide, state whether the recommended treatment is split slides, side-by-side, grid, or zoomable multi-figure.
- In `formal-build`, include `Slide | Core claim | Source paragraph/figure | Evidence type | Risk | Needs confirmation`.
- In `draft-build`, include only `Slide | Potentially risky claim | Needs confirmation` when there are real scientific claims.
- Group slides into major sections such as background and significance, research content and foundation, plan and expected outcomes.
- Make the logic explicit: why this slide exists, what it proves, and how it leads to the next slide.
- Ask for confirmation according to the selected profile. Do not stop for confirmation in quick-fix; in draft-build stop only when requested or scientifically ambiguous; in formal-build stop unless direct generation was requested.

Do not move to final HTML until the user confirms the content gate, unless the user explicitly waived confirmation.

## Phase 3: Design System

Use the user's personal style contract unless it conflicts with scientific clarity, readability, or delivery reliability. Default academic style is only a fallback.

- Reuse the user's preferred density, title style, layout archetypes, palette, typography rhythm, figure treatment, caption style, diagram style, navigation/footer pattern, and section rhythm.
- Avoid personal negative preferences from style memory or rejected examples.
- Use default deep navy/light gray/restrained accent styling only when examples are absent or insufficient.
- Keep body text readable for projection and split slides before shrinking below minimums.
- Do not change approved scientific content while adapting style.

Default 16:9 numeric constraints unless the template clearly requires otherwise:

- Chinese title: 34-44px; English title: 32-42px.
- Chinese body: 24-28px; English body: 22-26px.
- Caption: 16-18px; footnote/reference: 14-16px.
- Chinese body line-height: 1.45-1.65; English body line-height: 1.35-1.55.
- Formal proposal/defense bullets: 3-5 main bullets; group meeting/draft bullets: 4-6 main bullets.
- Content region should occupy at least 62% of slide height on normal content slides.
- For figure-text slides, start near 52:48 or 55:45. Let the figure dominate only when it is the evidence.
- For multi-figure slides, if a figure displays below 42% of content-region height, split the slide or add zoom interaction.
- Do not reduce body font below the minimum to fit content; split the slide instead.

Use the bundled layout baseline before writing slide-specific CSS:

- Start from `assets/layout_safety.css`, `assets/unified-type-scale.css`, and `assets/unified-image-scale.css` for new decks or substantial redesigns.
- Treat these files as guardrails, not a fixed theme. A user's approved template, current instructions, or accepted style memory may override values such as colors, spacing, and type scale.
- Keep the variable names and role classes (`--ts-title`, `--ts-body`, `--img-full`, `.slide-title`, `.slide-content`, `.slide-footer`) even when values are customized. This lets static and rendered checks reason about typography and figure sizing.
- Do not create per-slide ad hoc font sizes or image heights unless there is a documented scientific or template reason.

If `assets/templates/` contains user templates, inspect the relevant template and reuse its only after checking whether approved user examples/style memory should override it:

- aspect ratio and slide frame
- title/footer placement
- colors and fonts
- recurring shapes, dividers, and figure treatment
- section divider style

If the output does not visibly follow the personal style contract, treat that as a failed build and revise before delivery. A deck that merely borrows colors but ignores the user's density, title/footer habits, spacing system, figure treatment, diagram style, or slide rhythm has failed personalization.

## Phase 4: Build HTML Presentation

Default to Reveal.js when the user wants a talk-ready academic presentation with notes, navigation, and PDF export. Use a self-contained HTML/CSS/JS structure when offline portability, custom animation, or no external dependencies matter more.

Choose the HTML shell deliberately:

| Shell | Use when | Required structure |
| --- | --- | --- |
| Reveal.js | The deck needs talk navigation, notes, print/PDF flow, or compatibility with common slide tooling. | Use `assets/slide-shell-reveal.html` as the slide skeleton. |
| Custom HTML | The user prioritizes offline portability, custom transitions, or a non-Reveal visual system. | Use `assets/slide-shell-custom.html`; every slide must include `data-slide` so verification tools can enumerate slides. |

Custom HTML is allowed, but it must preserve the same title/content/footer regions and type/image variables unless the user explicitly approves a different structure.

These shells are starting constraints for reliable first generation. Later personalization may tune density, title placement, image scale, spacing, and motifs through the user's template or style memory. Do not remove the role variables or `data-slide`/slide region structure unless the user explicitly chooses a less verifiable custom layout and accepts the verification downgrade.

Choose an output dependency mode:

- **portable-folder** - Default: `index.html` plus `assets/`, `figures/`, and local vendor files when feasible.
- **portable-single-html** - Use for small decks with few images or when the user asks for one file.
- **cdn-light** - Use for fast draft-build only, or when the user approves network dependencies.

Formal-build should avoid CDN unless local vendoring is unavailable and the risk is documented. Do not generate a long README by default. For formal-build, create a concise `delivery_notes.md` only when multiple assets, verification reports, or export instructions are involved; otherwise keep delivery notes in the final response.

Do not promise a native editable PowerPoint deck. If the user needs `.pptx`, state that this skill's primary output is HTML slides and either ask whether HTML is acceptable or use a separate PPTX-capable workflow/tool if one is available.

Required features:

- Keyboard and touch navigation.
- Speaker notes when the talk benefits from them.
- Print/PDF styles.
- Responsive layout for laptop and projector screens.
- Page numbers fixed at the bottom right.
- Optional interaction only where it clarifies research, such as clickable method modules, timeline stages, or figure annotations.
- Zoom interaction for approved multi-figure slides where individual figures are too small for comfortable reading.
- All figures should resolve to the approved image inventory. If a slide uses a custom diagram instead, document that decision in the delivery notes.

Slide layout requirements:

- Use a consistent slide shell: title region, content region, footer region.
- For new decks or substantial redesigns, adapt `assets/layout_safety.css`, `assets/unified-type-scale.css`, `assets/unified-image-scale.css`, and the relevant slide shell before custom visual styling.
- Center content within the usable frame, not merely inside a card.
- Evaluate where the text sits on the whole screen, not only whether a card is centered.
- Avoid middle-band layouts where all text is compressed into a narrow horizontal strip with empty space above and below.
- Let short-text research slides occupy meaningful vertical space, often 60-70vh of effective content height, with modules distributed from upper content region to lower content region.
- Balance figure and text widths; for figure/text slides, use roughly 1:1 or 4.5:5.5 unless the figure must dominate.
- Reduce title-to-content dead space. The slide should feel occupied across the full viewport.
- Keep images, text, and diagrams vertically balanced with similar top and bottom breathing room.
- Split slides instead of shrinking text below readability.
- Put the agenda on its own slide when needed. Do not crowd the title slide with an agenda, and do not add explanatory prose to a simple agenda slide.
- Use one controlled type scale across the deck. Avoid per-slide ad hoc font sizes that cause visual jumps.
- Use one controlled image scale across the deck. Prefer `--img-full`, `--img-half`, `--img-third`, and `--img-thumb` over one-off hardcoded image heights.
- Avoid absolute-positioned text boxes for main content unless their bounding boxes are fixed and tested. Prefer CSS grid/flex with stable min/max constraints.
- Keep `line-height`, margins, and card padding consistent for the same content role across all slides.
- Prevent overlap by giving title rows, content grids, figures, captions, and footers explicit reserved regions.
- For multi-figure slides, keep captions attached to each figure, reserve footer space, and make zoomed images fit within the viewport without covering navigation irreversibly.
- If a slide exceeds density limits, split or continue the slide instead of reducing body text below the minimum readable size.

## Phase 5: Verification

Verify before delivery:

- The generated deck follows the personal style contract, not just the general color palette.
- Use `scripts/extract_style_fingerprint.py` and `scripts/compare_style_fingerprint.py` when screenshots or HTML examples are available and style similarity matters.
- Treat style fingerprint reports as advisory; they cannot prove visual similarity and should not replace screenshot/manual review.
- Each slide type maps back to an approved prior example, style memory entry, template exemplar, or documented fallback.
- The generated slide screenshots are compared against selected user example screenshots when available.
- Style drift is reported when title/footer positions, color distribution, figure/text ratio, card/rule/sidebar motifs, typography scale, or caption style diverge from the selected examples.
- Every non-decorative image comes from the approved image inventory or an explicitly approved custom diagram.
- Use `scripts/check_html_deck.py` for static resource/style audit. Static checks cannot prove visual non-overlap.
- For formal-build or a deck with prior layout failures, run `scripts/check_html_deck.py --strict-layout` so missing type/image variables, unreadably small font sizes, and excessive ad hoc sizing are treated as errors.
- Use `scripts/verify_rendered_deck.py` or another browser-render check when available to inspect screenshots, DOM boxes, image loading, overflow, and font drift.
- For custom HTML decks, use `scripts/verify_rendered_deck.py --generic-mode` and ensure every slide has `data-slide` or `.slide` markup. If generic mode still reports `verification-incomplete`, do not claim DOM overlap was verified.
- Treat `title-content-overlap`, `footer-content-overlap`, `dense-text-risk`, `bullet-density-risk`, `multi-figure-density-risk`, and `content-central-band-risk` warnings as layout failures that need revision unless a screenshot review proves the warning is harmless.
- Treat `verification-incomplete` and `screenshot-may-be-blank` as verification failures for formal-build until screenshots are manually reviewed or the markup is adjusted so the script can inspect DOM items.
- Titles do not collide, truncate, or wrap into unreadable blocks.
- Body text is not too small for a projected doctoral proposal or defense. If text feels small, increase font size and line spacing, then redistribute layout.
- Text does not overlap, overflow, or sit in a narrow column with unused empty space elsewhere.
- Same-level text roles have consistent font sizes across slides.
- No title, figure, caption, footer, page number, or body block visually overlaps another element.
- Figure captions and labels are close to the relevant visual elements.
- Every slide has consistent frame height, footer position, and page number placement.
- Content uses the middle of the screen, not only the upper half.
- Content is not squeezed into the central band of the slide; upper, middle, and lower regions feel intentionally used.
- Scientific claims still match the approved outline and source materials.

Before browser preview, detect available options such as Google Chrome, Microsoft Edge, Firefox, Chromium, or the Codex in-app browser. If the user requested a specific browser and it is available, use it. If it is not available, ask before using another browser. Do not force Edge as the default fallback.

When a user-confirmed browser automation option is available, inspect representative screenshots at 16:9 desktop and a smaller viewport. Prefer checking every slide for:

- bounding-box overlaps
- text overflow and clipped content
- inconsistent title/body/caption font sizes
- footer/page-number drift
- blank or broken images
- mismatch from the chosen template exemplar
- mismatch from the selected personal style examples

If no browser is available, perform static CSS/HTML checks and tell the user what was not visually verified.

Verification path:

| Output structure | Preferred check | Downgrade note |
| --- | --- | --- |
| Reveal.js deck | `verify_rendered_deck.py` | If DOM items are zero, wait/retry or report verification incomplete. |
| Custom HTML with `data-slide` / `.slide` | `verify_rendered_deck.py --generic-mode` | If DOM items are zero, screenshot evidence only; DOM overlap not verified. |
| Custom HTML without stable slide markers | Static check plus manual screenshot review | Ask to add `data-slide` markers before claiming rendered verification. |

## Phase 6: Delivery

Deliver:

- The generated or modified `.html` file path.
- How to open it locally.
- Navigation controls.
- PDF/print instructions.
- Any unresolved scientific or visual assumptions.
- Confirmation that the template-style contract was applied, or a clear note if no usable template was found.
- Personalization summary: which prior examples were imitated, which style traits were preserved, which traits changed for readability/science, and unresolved style uncertainty.
- Feedback learning summary when relevant: reusable accepted traits, reusable rejected traits, and whether style memory was updated or left unchanged pending user approval.
- Confirmation that source-document figures were used according to the approved image inventory, or a list of approved substitutions.
- A brief verification summary: static checks, render checks, browser used if any, unresolved visual risks, unconfirmed scientific assumptions, and whether multi-figure zoom was added.

If the user asks for share/export later, offer PDF export or deployment as a separate step.

## Supporting Files

This is a direct-install skill package. Keep the installed skill lean: `SKILL.md`, `agents/`, `references/`, `scripts/`, and `assets/` only. Repository-level files such as README, LICENSE, tests, demos, package manifests, and GitHub metadata belong outside the installable skill folder.

- `agents/openai.yaml` is optional UI metadata for skill lists and default prompts; it is not a runtime dependency.
- Read [references/research-html-requirements.md](references/research-html-requirements.md) when building or substantially redesigning a research HTML presentation.
- Read [references/layout-safety-and-style-fingerprint.md](references/layout-safety-and-style-fingerprint.md) when layout crowding, overlap, or personal style fidelity is a known risk.
- Use `scripts/inspect_sources.py` to inspect PPTX, DOCX, HTML, LaTeX, and PDF sources/templates and optionally create reusable Markdown summaries.
- Use `scripts/extract_style_profile.py` to turn a template, old deck, HTML file, PDF, PPTX, or screenshot folder into a compact style seed for the current task.
- Use `scripts/update_style_memory.py` only after user approval or explicit long-term feedback wording. Its `--remove` option removes active `style_profile.json` entries only; it does not rewrite historical logs.
- Use `scripts/extract_style_fingerprint.py` and `scripts/compare_style_fingerprint.py` for lightweight, advisory style similarity reports.
- Use `scripts/doctor.py` to check optional local dependencies before relying on PDF/PPT rendering or browser validation.
- Use `scripts/check_html_deck.py` before delivery for static HTML/image/style checks, especially after prior failures involving missing figures, repeated figures, or overlap-prone CSS.
- Use `scripts/verify_rendered_deck.py` for browser-rendered verification when visual overlap, screenshot evidence, print layout, or template fidelity matters.
- Use `assets/templates/` for user-provided templates, starter HTML files, PPTX templates, CSS themes, logos, fonts, and recurring research visuals. Do not load all template assets into context; inspect only the relevant files. Do not redistribute commercial or system font files in any public wrapper repository.
- Use `assets/layout_safety.css` as neutral layout guardrails when a generated HTML deck needs stronger protection against overlap, crowding, or footer/title collisions.
- Use `assets/unified-type-scale.css` as the default controlled typography baseline. Users may personalize values, but generated decks should keep the variable names and role classes.
- Use `assets/unified-image-scale.css` as the default controlled figure-size baseline. Users may personalize values, but generated decks should keep the variable names and role classes.
- Use `assets/slide-shell-reveal.html` or `assets/slide-shell-custom.html` as copyable slide skeletons for new decks and substantial redesigns.
- Use `assets/examples/` only when the user already has approved prior examples. The user is not required to manually build this folder; a current template, old deck, or screenshot can be used directly as the style seed.
- Use `assets/style_memory/` for persistent user aesthetic preferences, negative preferences, and slide-role layout habits.
