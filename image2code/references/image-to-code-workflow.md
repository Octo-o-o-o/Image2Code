# Image2Code Workflow

Use this reference when implementing a generated pack or when the user asks for a one-to-one image-to-code build.

## Core Loop

1. Read `design-model.yaml`, the markdown spec, and every target image before editing code.
2. Capture the current implementation with representative data.
3. Segment each target screen into regions: shell, navigation, toolbars, repeated lists/cards, content panels, modals, empty states, and responsive variants.
4. Map each region to existing files, components, tokens, and data sources.
5. Implement the smallest layer that makes the next screenshot visibly closer: tokens, shared layout, shared components, page regions, then state polish.
6. Render the app and capture after-screenshots into `implementation-screenshots/`.
7. Compare target, before, and after screenshots. Record mismatches and decisions in `06-implementation-plan.md`.
8. Iterate until remaining differences are either fixed or explicitly accepted with a reason.

## Segmentation Checklist

- Large screenshots should be decomposed before coding. Note which regions can share components and which are page-specific.
- Preserve working information architecture unless the pack explicitly approves a layout refactor.
- Keep generated image text as visual guidance only; exact copy, values, states, and accessibility labels must come from markdown specs or product data.
- For native apps, verify each required device class and orientation. For web/desktop apps, verify each viewport breakpoint and dense-data state.
- For broad redesigns, build a disposable demo/prototype first, screenshot it, and use the mismatch list to de-risk production edits.

## Verification Record

For every implemented screen, add a row to `06-implementation-plan.md`:

| Page | Target Image | Current Screenshot | Implementation Screenshot | Observed Difference | Decision | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Example | images/10-dashboard.png | input/current-screenshots/dashboard-before.png | implementation-screenshots/dashboard-after.png | Header height is 4px taller than target | Accepted; matches existing shell constraint | done |

Run `scripts/sync_manifest.py` after adding screenshots so `manifest.json` records the evidence.

## Failure Modes To Watch

- Omission: target regions, states, or controls are missing in code.
- Distortion: visual hierarchy, spacing, typography, or control styling is materially different.
- Misarrangement: components exist but their order, alignment, grouping, or responsive behavior does not match the target.
- Style drift: implementation introduces a new design language not present in the pack or existing app.
- Behavior drift: visual work changes navigation, persistence, validation, or data semantics without explicit approval.
- Model drift: code follows a target image while ignoring the structured tokens, component provenance, or implementation constraints in `design-model.yaml`.
