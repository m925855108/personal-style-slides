# Research HTML Presentation Requirements

Use this reference for template-seeded, feedback-refined personal research decks. The goal is not a universal presentation style; the goal is to let the user provide an approved template, old deck, or screenshot; automatically extract style; generate personalized research slides; and refine local style memory from conversation feedback with user approval.

## Requirements Distilled From Prior Work

### Workflow

- Treat the current user-provided template, old deck, or screenshot as the style seed. The user should not need to manually maintain a style library.
- Current user instructions override old style memory.
- Accepted long-term style memory may refine the current style seed only when it does not conflict with the current template or request.
- First create a complete outline with slide titles and core points.
- Before the outline, inspect the requested template and inventory source images. Do not design from memory when templates or document figures are provided.
- Before a substantial design, extract a compact style profile from the current style seed. If no current style seed exists, retrieve the closest prior examples from `assets/examples/` and style memory from `assets/style_memory/`.
- Use the lightest reliable workflow. Small HTML fixes do not need a full source audit; new decks and major redesigns do.
- Use `quick-fix` for localized existing-deck edits, `draft-build` for fast first versions and group-meeting drafts, and `formal-build` for proposals, defenses, advisor review, final reports, and conference talks. If uncertain, prefer `draft-build`.
- Let the user confirm extracted text before final HTML in `formal-build` unless they explicitly request direct generation. In that case, generate the deck and mark unconfirmed scientific assumptions.
- Do not combine "here is the outline" and "here is the completed HTML" in the same response unless the user explicitly says to skip review.
- The formal-build confirmation artifact should include the selected template, template-style contract, image/figure inventory, slide list, per-slide title, core bullets, exact visual source for each image slide, claim-source table, and open questions.
- After first substantial inspection of a reusable source or template, ask once whether to save a concise Markdown memory file for future work.
- Keep user-corrected text stable. If the user has corrected a conclusion, do not paraphrase it into a different claim.
- Separate text/content revision from layout revision when the user asks for staged review.
- When the user asks for layout polish or "academic display texture", preserve the approved content and modify only typography, spacing, alignment, visual hierarchy, and slide structure.
- Ask only about genuinely ambiguous scientific claims, figure meanings, or required institutional details.

### Template-Based Style Learning

Use the current template, old deck, or screenshot as the style seed. Run or emulate `scripts/extract_style_profile.py` to create:

- `style_summary.auto.md`
- `style_profile.auto.json`
- optional template screenshots or rendered page references when available

Extract at least:

- canvas ratio
- title position, title scale, and title tone
- footer, page number, and logo placement
- primary, secondary, and accent colors
- typography hierarchy for title, body, caption, and footnote
- common layouts: two-column, three-column, card grid, workflow, figure-text, timeline
- figure/text ratio
- caption position and style
- image border, radius, shadow, and crop habits
- section divider, agenda, and closing page style
- page density and whitespace habits

Some traits may be inferred manually from screenshots when scripts cannot extract them. Do not claim that title/footer geometry, crop behavior, card radius/shadow, logo coordinates, or shape styling was automatically extracted unless the script output actually contains that evidence.

If several examples are available, select the closest 1-3 by:

- research scenario: group meeting, paper introduction, simulation result, research plan, proposal/defense, conference talk
- slide role: title, agenda, background, method, workflow, result, validation, plan, conclusion
- visual structure: two-column, card grid, figure-first, left navigation, timeline, flowchart, dense result page
- figure/text ratio
- language and density
- user approval status

Create a current-task style contract:

- visual density and whitespace habits
- title style: short/long, declarative/traditional, section-like/story-like
- layout archetypes
- palette and material preferences
- typography hierarchy
- figure and caption treatment
- diagram style
- section/navigation/footer habits
- text tone and scientific communication rhythm
- known dislikes and rejected patterns
- allowed modernization level
- style seed to imitate and rejected patterns to avoid

If no approved examples or template exist, use the default academic fallback and ask after delivery whether the result should become the first style reference.

After user feedback:

- summarize accepted visual traits
- summarize rejected visual traits
- distinguish one-time feedback from reusable style preference
- save reusable preferences only when the user approves or uses explicit long-term wording such as "always do this later", "avoid this later", or "remember this style"
- append to `assets/style_memory/user_feedback_log.md` rather than overwriting old memory

### Narrative

- Build the talk around a research argument, not a document dump.
- Distinguish "background", "significance", "research content", "research foundation", "research plan", and "expected outcomes".
- Use section divider or agenda slides when the deck has three or more major sections.
- Each slide should answer one question: What is the point? What evidence supports it? Why does the next slide follow?
- Plans and expected outcomes should correspond item by item when shown together.

### Scientific Text

- Preserve exact model names, source names, figure numbers, observational missions, equations, and conditional phrases.
- Treat "if conditions allow", "qualitatively reproduce", "preliminary verification", and similar qualifiers as meaningful.
- Do not invent stronger conclusions than the report supports.
- For Chinese research presentations, use Chinese labels in diagrams unless the user asks otherwise.
- For bilingual decks, keep terminology consistent across slides.
- In `formal-build`, maintain a claim-source table: `Slide | Core claim | Source paragraph/figure | Evidence type | Risk | Needs confirmation`.
- In `draft-build`, use a light risk table only when real scientific claims may be uncertain: `Slide | Potentially risky claim | Needs confirmation`.
- If a claim has no clear source, use cautious wording or omit it from formal decks.

### Visuals and Diagrams

- Prefer actual research figures when they are relevant and readable.
- Use supplied document figures by default. Do not substitute generated, web, or decorative images for figures that exist in the source document.
- If the user references a figure number or caption, locate and use that exact extracted image.
- If extraction is not possible, stop and ask before replacing it.
- Keep an image manifest: source document, figure number or caption, extracted asset path, slide assignment, and reason for use.
- Use custom diagrams when a source figure is wrong, repeated, low quality, or does not match the concept.
- If one slide needs multiple figures and the figures become small relative to text, ask during content confirmation whether to keep a multi-figure slide. If yes, add double-click or click-to-zoom image enlargement.
- If a multi-figure slide would make any figure display below 42% of the content-region height, split the slide or add zoom interaction.
- Prefer splitting dense figure evidence across slides when zoom would hide the narrative or make oral explanation awkward.
- Scientific diagrams must be physically plausible for the domain. Labels should sit near the corresponding process, region, arrow, or data feature.
- For user-specific diagrams, imitate prior accepted diagram grammar: line weight, transparency, color, labels, arrows, physical scale, and whether the style is flat, semi-realistic, schematic, or annotated.
- Check personal negative preferences before drawing diagrams, especially rejected colors, exaggerated visual metaphors, too-thick corona/cloud effects, sci-fi energy effects, excessive blankness, or cramped central-band layouts.
- Use arrows to show radiation, propagation, scattering, model flow, or causal direction.
- Use interactive modules only when they reduce clutter, such as clicking a workflow node to reveal implementation details.

### Layout

- A slide should feel like a coherent PPT page with a stable frame, not a webpage section.
- If a user template exists, the slide should first feel like that template: same shell logic, title/footer placement, color hierarchy, and recurring motifs.
- Treat template use as a contract, not inspiration. If the generated HTML only borrows colors but ignores the template structure, revise it.
- Keep title height consistent and controlled. Long titles need smaller max sizes or two-line treatment.
- Do not solve overflow or crowding by simply reducing body font size. For doctoral proposal and defense decks, projection readability is more important than fitting too much onto one slide.
- Prefer larger readable body text with relaxed line height, commonly around 1.55-1.65, then use wider columns, taller content regions, or slide splitting.
- Page numbers belong in a consistent bottom-right position.
- Avoid cases where all content occupies only the top half of the slide.
- Avoid cases where text is squeezed into a central horizontal band with empty space above and below.
- Avoid narrow text cards surrounded by unused empty space.
- Reduce dead space between title and figure/content.
- Balance image and text regions. Typical figure:text ratios are 1:1 or 4.5:5.5.
- Use comfortable line height and paragraph spacing; never compress text into a crowded panel.
- Judge the position of text on the whole screen, not only the position of the card/container.
- For short-text method or research-content slides, stretch the two-column or module layout across roughly 60-70vh of usable height so the page feels evenly occupied.
- Let left/right modules align and distribute vertically; avoid stacking every important element around the exact center.
- Split dense content into continuation slides instead of shrinking everything.
- Use one controlled type scale across the deck: title, section label, body, caption, footnote, tag. Same role should have same size unless a documented slide type requires otherwise.
- Avoid absolute positioning for major text blocks unless the region is explicitly reserved and checked. Prefer grid/flex layout with stable rows and columns.
- Reserve slide regions for header, content, footer, page number, and captions to avoid overlap.
- For all generated HTML, inspect CSS for ad hoc per-slide font sizes, negative margins, excessive absolute positioning, and content containers without min/max constraints.

Default 16:9 academic deck metrics:

- Chinese title: 34-44px; English title: 32-42px.
- Chinese body: 24-28px; English body: 22-26px.
- Caption: 16-18px; footnote/reference: 14-16px.
- Chinese body line-height: 1.45-1.65; English body line-height: 1.35-1.55.
- Formal proposal/defense bullets: 3-5 main bullets; group meeting/draft bullets: 4-6 main bullets.
- Content region should occupy at least 62% of slide height on normal content slides.
- Figure-text slides should start near 52:48 or 55:45 unless the figure is the main evidence.
- Do not reduce body font below the minimum to fit content; split the slide instead.

### Style

Use the user's personal style contract first:

- Preserve density, title rhythm, layout archetypes, palette, typography, figure treatment, diagram style, section rhythm, and footer/navigation habits from approved examples.
- Do not generalize to a popular academic style when user examples are sufficient.
- Default academic palette such as deep navy, light gray, and restrained accents is only a fallback.
- Use charts, vectors, equations, and data visualizations as the primary visual language when the user's examples do not say otherwise.
- Do not let style additions alter scientific wording, conclusions, figure meaning, or slide order that the user already approved.

Imitation is structural and stylistic, not blind duplication:

- Imitate title placement, figure/text ratio, card/rule/sidebar motifs, typography scale, color logic, caption style, and section rhythm.
- Do not blindly copy old page count, old figure count, old image positions, old title length, or decorative elements that do not fit the new content.

### Template Contract

When a user example or template is available, derive a personal style contract first. A template contract is secondary unless the template is the user's approved style reference.

- canvas ratio and margins
- title, subtitle, section label, footer, page number, and logo positions
- typography scale and font families
- color tokens and accent usage
- content grid for text, figure-text, multi-panel, timeline, and closing slides
- shape language such as rules, frames, sidebars, tabs, section chips, or background bands
- figure treatment such as border, caption style, image crop rules, and label placement
- exemplar mapping from template examples to generated slide types

Ask the user to approve the template choice when multiple templates are available.

The generated deck should look like a continuation of the user's approved examples. A deck that only copies colors but changes the density, shell, spacing system, title/footer placement, figure treatment, diagram style, or slide rhythm has failed personalization.

For PPTX templates, prefer a hybrid approach:

- Parse OOXML metadata when available: slide size, text, media assets, relation mapping, theme colors, master/layout names, and rough shape counts.
- Render representative slides to images when tooling allows and use screenshots as the primary visual reference for title bars, footers, color blocks, logos, and spacing.
- PPTX visual rendering requires LibreOffice for PPTX-to-PDF conversion and PyMuPDF for PDF-page-to-PNG rendering. Without both, use OOXML metadata only and report the limitation.
- Do not claim exact PPTX geometry when only ZIP/XML metadata was inspected.

For LaTeX Beamer templates, inspect theme declarations, frame title patterns, sectioning, color definitions, logo commands, and `\includegraphics` usage.

### Functionality

- Reveal.js is preferred for academic talks because it supports keyboard navigation, speaker notes, fragments, and PDF export.
- A custom self-contained HTML deck is acceptable when offline reliability or detailed custom animation matters more.
- Default output is `portable-folder`: `index.html` plus `assets/`, `figures/`, and local vendor files when feasible.
- Use `portable-single-html` for small decks or when the user requests one file.
- Use `cdn-light` only for draft-build or when the user approves network dependencies. Formal-build should avoid CDN unless the risk is documented.
- Include keyboard navigation and touch-friendly controls.
- Include print/PDF CSS.
- Add speaker notes for oral explanation when useful.
- Add progress indication if it does not distract from the research.

### Visual Verification

Before using a browser, detect available options and ask the user to confirm the preview browser unless they already specified an available one. Prefer Google Chrome when the user asks for Chrome, otherwise use a local browser selected or approved by the user. Do not force Microsoft Edge as the default fallback.

Use a browser check when the user confirms a browser. For each representative slide, and preferably every slide:

- run at 16:9 desktop size such as 1600x900 or 1920x1080
- capture screenshots or inspect DOM bounding boxes
- check that text does not overlap, clip, or overflow
- check that same-level text roles use consistent computed font sizes
- check that footer, page number, and section labels do not drift
- check that images load and captions stay attached to their figures
- check that each slide resembles the mapped template exemplar
- check that each slide resembles the selected user example or documented style memory entry

If the user requests a specific browser and it is missing, ask before substituting another browser.

Run static script checks before final delivery when available:

- `scripts/inspect_sources.py` for PPTX, DOCX, HTML, LaTeX, and PDF source/template inventory.
- `scripts/extract_style_profile.py` for template/old-deck/screenshot style learning.
- `scripts/check_html_deck.py` for static image/path/style audit with `error/warn/info` severity.
- `scripts/verify_rendered_deck.py` for browser screenshots and DOM bounding-box checks when available.
- `scripts/extract_style_fingerprint.py` and `scripts/compare_style_fingerprint.py` for lightweight style similarity reports.

Static checks are helpers, not replacements for visual review. If static checks pass but render checks were not run, do not claim rendered non-overlap. If screenshots or DOM checks show overlap, fix the layout.

Style similarity check:

- Compare generated slide screenshots with selected user example screenshots when available.
- Compare title/footer positions, dominant color distribution, figure/text region ratio, card/rule/sidebar motifs, typography scale, caption treatment, and layout archetype.
- Report style drift instead of claiming perfect imitation.
- Style fingerprint reports are advisory and cannot prove visual similarity.
- If examples are missing or not visually comparable, state that personalization used style memory/template fallback.

Failure downgrade protocol:

- If browser render verification is unavailable, run static-check and state that rendered overlap was not verified.
- If source image extraction fails, use page-rendered screenshots or manually cropped regions when possible and mark them as `page-rendered fallback`.
- If template parsing fails, use screenshot/style observation fallback and mark template inheritance as approximate.
- DOCX inspection is lightweight. It can list text and media assets but may not reliably bind figures, captions, equations, tables, comments, tracked changes, or exact image/text positions.
- If scientific evidence is unclear, add it to the risk table.

## Common Failure Patterns and Fixes

- **Title too large**: lower the max title size, reserve a title row, and test long Chinese titles.
- **Content in upper half only**: increase content region height, center the grid vertically, and align the usable frame rather than the card.
- **Text too small after fitting**: undo the font shrink, increase body size and line height, then redistribute blocks or split the slide.
- **Text crowded in the middle**: increase effective content height, use `align-items: stretch`, distribute modules with `space-between`, and avoid a single centered row of small cards.
- **Large blank gap below title**: reduce header margin and let figure/text grid start closer to the title row.
- **Text too narrow**: widen the text region, reduce unnecessary card padding, or switch from three columns to two slides.
- **Figure dominates without explanation**: use a balanced figure/text grid and add a concise interpretation panel.
- **Repeated or mismatched figures**: replace one figure with a custom diagram or swap figures while preserving original captions/titles as requested.
- **Flowchart misses research content**: map every research objective to at least one workflow node or implementation detail.
- **Claim drift**: compare final slide text against the approved outline and source conclusion before delivery.
- **No confirmation flow**: stop after outline and key text; ask the user to confirm before writing final HTML.
- **Template ignored**: create a template-style contract and revise the HTML until the shell, hierarchy, and recurring motifs match it.
- **Template examples ignored**: map each output slide type to a template exemplar and rebuild from that exemplar's structure.
- **Wrong images used**: create an image manifest from source documents and replace non-approved images with the exact extracted source figures.
- **Font inconsistency**: define CSS variables for title/body/caption roles and remove ad hoc slide-specific type sizes.
- **Overlap**: reserve header/content/footer regions and verify bounding boxes or screenshots before delivery.
- **Browser forced without confirmation**: detect available browsers, report options, and ask the user to choose or approve the fallback.
- **Multi-figure slide unreadable**: split the evidence across slides or add approved zoom interaction with clear captions and stable footer spacing.
- **Reusable source reread every time**: after first inspection, ask whether to save a Markdown memory file and use targeted search in that file next time.
- **False verification claim**: distinguish static audit from browser-rendered validation. Never say "no overlap verified" after static checks only.
- **Wrong workflow profile**: use quick-fix for localized edits, draft-build for uncertain first versions, and formal-build only for formal or high-accuracy contexts.
- **Generic academic drift**: generated slides look broadly academic but not like the user's prior examples. Reopen the personal style contract and map each slide to a closer example.
- **Blind copying**: old layout was copied even though new figures/text no longer fit. Preserve visual grammar but split, resize, or restructure for the new content.
- **Negative preference repeated**: a rejected color, metaphor, density, or diagram style appears again. Check `assets/style_memory/` and rejected examples before redesigning.

## Suggested Slide Types

- Title slide: thesis/report title, author, affiliation, advisor, date; no agenda unless requested.
- Agenda slide: major sections only, no explanatory paragraph.
- Background slide: 3 concise modules that establish field context.
- Significance slide: why the problem matters and what the work will test.
- Research content slide: objectives plus method flow.
- Method interaction slide: clickable workflow nodes with implementation details.
- Research foundation slide: figure plus basic setup, core points, and conclusion.
- Validation slide: comparison figures plus what each verifies.
- Plan/outcomes slide: timeline where every plan item has a matching expected result.
- Closing/thanks slide: short acknowledgement and discussion prompt, if appropriate.

## Template Folder

Use `assets/templates/` for user-owned templates. Acceptable contents include:

- HTML starter decks
- CSS theme files
- Reveal.js snippets
- PPTX institutional templates
- logos and watermarks
- font files
- recurring diagrams or lab visual assets

When a template is present, inspect only the files needed for the current deck and adapt the output to its visual grammar.

## Example Folder

Use `assets/examples/` for user-owned prior examples. Acceptable contents include:

- approved HTML decks
- approved PPTX decks
- screenshots of accepted slides
- slide-specific examples such as method flow, result comparison, title, agenda, or plan pages
- `style_profile.json` files generated from prior examples
- `bad_examples/` containing rejected styles or failed attempts

Examples are not necessarily templates. They are evidence of the user's aesthetic and communication habits. Inspect only the closest relevant examples; do not load the full example library.

Suggested layout:

```text
assets/
  templates/
  examples/
    approved_deck_name/
      index.html
      screenshots/
      style_profile.json
    group_meeting_example/
      deck.pptx
      screenshots/
      style_profile.json
    bad_examples/
      too_landing_page/
      too_empty/
  style_memory/
    user_style_profile.md
    user_style_profile.json
```

## Source Memory Files

When the user approves saving a source memory file, keep it concise:

- source/template path, file type, hash, and inspection date
- slide or frame count
- main colors, typography hints, and layout motifs for templates
- figure list or media list for research sources
- known extraction limitations
- notes about how to reuse the source in future decks

Do not treat the memory file as authoritative if the original file changed. Reinspect when the hash, filename, or user request suggests the source has been updated.

## Style Memory Files

Use `assets/style_memory/` for persistent user aesthetic preferences:

- what the user likes in accepted decks
- what the user dislikes or rejected
- preferred layouts by slide role
- common palette, typography, figure treatment, captions, section pages, and footer styles
- diagram-specific preferences
- allowed modernization level
- examples to imitate and examples to avoid

Recommended files:

- `style_summary.md` - concise human-readable stable style summary
- `style_profile.json` - machine-readable stable style profile
- `user_feedback_log.md` - append-only feedback history
- `negative_preferences.md` - reusable rejected visual patterns

Example JSON fields:

```json
{
  "user_style_profile_version": "2026-05-14",
  "preferred_layouts": {
    "research_background": "three concise modules with restrained icons",
    "method_flow": "wide flowchart plus right-side explanation",
    "simulation_result": "large figure left, 3-point interpretation right",
    "plan": "timeline with matched expected outcomes"
  },
  "visual_preferences": {
    "palette": "derive from approved examples before fallback colors",
    "density": "avoid large unused blank areas",
    "diagram_style": "physically plausible, labeled near the process"
  },
  "negative_preferences": [
    "landing-page hero composition",
    "text compressed into central band",
    "figures too small in multi-figure slides"
  ]
}
```
