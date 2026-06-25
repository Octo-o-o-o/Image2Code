# Image2HTML Prototype Workflow

Use this reference when converting one or more screenshots or design images directly into an HTML/CSS/JS prototype. The goal is editable, componentized code that visually matches the source images, not a screenshot pasted into a browser.

## Fidelity Contract

Before editing files, write a short contract for the run:

- Source image matrix: file path, width, height, aspect ratio, inferred screen name, and whether the image appears to be a full viewport or a scrollable/full-page capture.
- Target viewport: match the source aspect ratio unless the user specifies another target. If the source is a full viewport, the prototype screenshot must not require extra scroll to show the same content.
- Output shape: single HTML file, small static site, React app, or integration into an existing project. For quick image2HTML work, default to one self-contained HTML file unless the repository already has a frontend stack.
- Component naming: choose the naming convention before coding. For static HTML, use a stable prefix such as `crm-` plus BEM-style classes and `data-component="PascalCaseName"` for inspectable component boundaries.
- Source-image policy: do not embed source screenshots as `<img>`, CSS backgrounds, canvas bitmaps, or masked overlays in the deliverable unless the user explicitly asks for a tracing/debug layer. If debug overlays are used, keep them disabled by default and document them.
- Acceptance threshold: list what must match exactly, what may be approximate, and which differences require a written reason.

## Source Decomposition

Inspect every image before writing code:

- Mark shared shell regions: browser chrome, app top bar, sidebar, icon rail, right panel, bottom bars.
- Mark screen-specific regions: calendar grid, filter panel, metric cards, results list, chart cards, forms, modals, empty states.
- Record repeated components and variants: buttons, icon buttons, avatars, cards, list rows, table rows, calendar events, chips, badges, charts, filters.
- Extract design tokens from pixels and repeated visual rules: color palette, typography scale, spacing rhythm, radii, shadows, border color, opacity, icon style.
- Record copy and data separately from generated or blurry image text. If text is unreadable, preserve the visual slot and write an explicit uncertainty.

Use a region/component inventory table:

| Source Image | Region | Component Name | Shared? | Fidelity Notes |
| --- | --- | --- | --- | --- |
| screen-a.png | top navigation | TopNavigation | yes | active pill is 52px tall, black fill |

## Implementation Order

1. Build the global canvas first: viewport sizing, body background, app shell, token variables, font scale, and shared shadow/radius rules.
2. Build shared shell components: brand, top navigation, action icons, side navigation, rail, right panel, avatar system.
3. Build repeated components with names before page details: card, metric card, result row, filter field, chip, calendar event, chart shell.
4. Build one screen fully, render it, and compare against its source image before copying the system to other screens.
5. Add the remaining screens using the same shell and components. Do not fork component styling unless the source image shows a real variant.
6. Add minimal JS only for required screen switching or state changes. Keep visual implementation in CSS.
7. Remove temporary tracing overlays, ruler guides, or source screenshots before final delivery unless explicitly requested.

## Verification Loop

Run verification after each meaningful pass:

1. Render each screen at the target viewport with browser automation.
2. Capture implementation screenshots with stable filenames.
3. Check viewport fit:
   - implementation screenshot dimensions match the target dimensions;
   - document `scrollWidth` equals viewport width;
   - if the source is a full viewport, document `scrollHeight` should not exceed viewport height except for minor browser rounding.
4. Check runtime layout:
   - exactly one intended screen/state is active;
   - no text or element has unintended horizontal overflow;
   - no important content is clipped by fixed headers, sidebars, or cards;
   - hover/active state dimensions do not shift the layout.
5. Compare source and implementation:
   - first use side-by-side visual review;
   - compute simple image metrics when possible, such as aspect-ratio delta and resized screenshot difference;
   - for high-stakes fidelity, compare by regions rather than relying on one whole-image score.
6. Write a mismatch log and iterate. Do not call the work high fidelity while unresolved layout, spacing, or missing-region issues are only known mentally.

Recommended mismatch log:

| Screen | Region | Expected From Source | Actual In HTML | Decision | Status |
| --- | --- | --- | --- | --- | --- |
| Calendar | bottom form | visible in source viewport | below fold due extra scroll | compress layout to source viewport | fixed |

## Automated Checks

Use `scripts/audit_html_prototype.py` when the inputs are local files:

```bash
python3 /path/to/image2code/scripts/audit_html_prototype.py \
  --html /absolute/path/to/index.html \
  --min-components 12 \
  --require-screen-count 3 \
  --source calendar=/absolute/path/source-calendar.png \
  --screenshot calendar=/absolute/path/rendered-calendar.png
```

The script checks static HTML concerns: component naming, source screenshot embedding, suspicious `data:image` bitmap embeds, screen/target consistency, and source/implementation image aspect ratios. It does not replace browser automation for runtime layout, overflow, active-state, or visual comparison.

For browser verification, collect at least:

```text
screen name
source image dimensions
target viewport
implementation screenshot path and dimensions
document scrollWidth/clientWidth
document scrollHeight/clientHeight
active screen/state
overflow element sample count
```

## Fidelity Gates

Do not mark the prototype complete until:

- Every source image has a matching rendered implementation screenshot.
- The target viewport matches the source aspect ratio or the deviation is documented.
- Full-viewport source images fit in the same viewport without extra vertical scroll.
- The source screenshots are not embedded in the deliverable unless explicitly approved.
- Shared components have consistent names and are reused across screens.
- Component names are auditable in markup (`data-component` or framework component names).
- Navigation and active states match the source for every rendered screenshot.
- No unexpected horizontal overflow or text clipping is present at the target viewport.
- Major regions are neither missing nor reordered.
- Remaining differences are recorded with decisions, not silently accepted.

## Failure Modes From Prototype Audits

- Aspect-only matching: the screenshot aspect ratio matches the source, but the page scrolls and hides content that was visible in the source viewport.
- Plausible SaaS drift: the design language feels close, but card density, type scale, and side-panel proportions differ enough to fail one-to-one matching.
- Component naming afterthought: CSS classes exist, but no stable component names map source regions to implementation regions.
- Static-only validation: the HTML parses and screenshots render, but active screen state, overflow, and viewport fit are never measured.
- Whole-image metric misuse: a single pixel score is treated as proof even though large blank backgrounds hide region-level mismatches.
