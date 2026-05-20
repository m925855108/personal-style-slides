# Layout Safety And Style Fingerprints

Use this reference when a deck must avoid crowded HTML layout, or when the
generated deck must stay close to a user's approved template/style seed.

## What Can And Cannot Be Guaranteed

Do not promise that an HTML deck is mathematically guaranteed to have no overlap.
Rendered layout depends on browser, viewport, fonts, image aspect ratios, math
rendering, and text wrapping.

Use a stricter claim:

- Static checks can catch missing assets and risky CSS.
- Rendered checks can catch many overflow, overlap, density, and broken-image
  failures.
- Screenshot/manual review is still needed for final visual judgment.

## Layout Safety Contract

For new or substantially revised decks, prefer a fixed slide shell:

```text
title region
content region
footer/page-number region
```

Rules:

- Reserve vertical space for title and footer before placing content.
- Use grid/flex layouts with `minmax(0, 1fr)` and explicit gaps.
- Keep slide height to `100vh` / `100dvh`.
- Avoid scrollable slide bodies.
- Do not reduce body text below the skill's minimum readable size to fit more
  content.
- Split slides when density exceeds the relevant threshold.
- For multi-figure pages, prefer split slides or zoom interaction when each
  figure becomes too small.

The bundled `assets/layout_safety.css` provides neutral guardrails. It is not a
visual theme. Adapt it to the user's template colors and motifs.

## Density Thresholds

Use these as default warning thresholds unless the user's template clearly
supports a different density:

| Slide type | Warning threshold |
| --- | --- |
| Text / argument slide | More than 5 main bullets in formal-build, or more than 6 in draft-build |
| Figure-text slide | Text column longer than 3 concise interpretation points |
| Multi-figure slide | 3+ figures plus substantial body text |
| Code / equation slide | Code/equation block forces title, caption, or footer out of reserved zones |
| Section divider | More than title, subtitle, and one short context line |

If a threshold is exceeded, split the slide, create a continuation slide, or add
an approved zoom interaction. Do not silently shrink text.

## Rendered Verification Signals

Use `scripts/verify_rendered_deck.py` when available. Treat these warnings as
actionable:

- `title-content-overlap`
- `footer-content-overlap`
- `element-overflow`
- `element-outside-viewport`
- `dense-text-risk`
- `bullet-density-risk`
- `multi-figure-density-risk`
- `content-central-band-risk`

If Playwright is unavailable and only screenshot fallback ran, say that DOM
overlap was not verified.

## Personal Style Fingerprint

Personal style should be represented as a lightweight, explainable fingerprint,
not as a vague aesthetic label.

Extract and compare:

- canvas and slide count
- dominant colors
- font tokens and font pixel values
- visual density
- image-per-slide ratio
- layout archetypes and layout motifs
- CSS variable and class-name hints
- whether rendered reference screenshots were available

Use `scripts/extract_style_fingerprint.py` to create fingerprints and
`scripts/compare_style_fingerprint.py` to compare them. These reports are
advisory. They help detect drift, but they cannot prove that two decks "look the
same."

## Early-Stage Style Learning

Before there is enough feedback history, prefer this order:

1. Use the current template/old deck/screenshot as the primary style seed.
2. If possible, render PPTX/PDF/HTML pages to screenshots and inspect them.
3. Extract a compact style profile and style fingerprint.
4. Generate slides by matching each new slide type to the closest style seed
   layout.
5. Compare the generated deck fingerprint against the reference fingerprint.
6. Use user feedback to update local style memory only with approval.

This is closer to personal fingerprint recognition than to training a small
model. A small model may be useful later, but the first reliable layer should be
deterministic, inspectable, and easy to correct.
