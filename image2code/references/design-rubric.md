# Design Review Rubric

Use this rubric after every image generation round. Score each category from 1 to 10 and record the result in `05-review-log.md`.

## Categories

1. Product fit: The design supports the actual user workflow, data density, and domain.
2. Information architecture: Navigation, page hierarchy, and actions are predictable.
3. Visual hierarchy: Primary content, secondary content, and controls scan correctly.
4. Layout precision: Grid, alignment, spacing, and rhythm are consistent.
5. Typography: Sizes, weights, line lengths, and labels fit the product surface.
6. Color and contrast: Palette is coherent, accessible, and not one-note.
7. Component quality: Tables, forms, filters, cards, modals, charts, and empty states feel complete.
8. State coverage: Loading, empty, error, disabled, hover/active, overflow, and dense-data states are addressed.
9. Responsiveness: The design has clear behavior for target widths and does not rely on fragile pixel-perfect assumptions.
10. Implementation realism: The design can be mapped to the existing stack without a rewrite.
11. Image readability: Target images are large enough to inspect text, spacing, controls, and component details without guessing.
12. Consistency locks: Palette, radius system, typography hierarchy, icon treatment, CTA language, and motion level stay coherent across the pack.

## Passing Bar

- Minimum for final pack: average score 8.5 or higher.
- No category below 7.5 unless the tradeoff is explicitly accepted.
- Existing-project redesigns must score at least 8 on implementation realism.

## Common Failure Patterns

- Generic SaaS dashboard visuals that ignore the product's actual tasks.
- Decorative backgrounds that reduce legibility or are costly to implement.
- Inconsistent button sizes, table density, card radii, or icon style across screens.
- Beautiful single screen with no state model.
- Text in generated images treated as source of truth even when it is misspelled or distorted.
- Design tokens omitted from markdown, forcing implementers to infer from pixels.
- New framework assumptions that fight the existing codebase.
- Too many screens or sections compressed into one unreadable board.
- Cropped overview fragments used as implementation targets instead of fresh detail images.
- Hero/first-view surfaces that overflow the target viewport or bury the primary action.
- Redesigns that silently change routes, navigation labels, form semantics, legal copy, analytics-sensitive actions, or working accessibility behavior.

## Review Method

For each round:

1. Inspect the full image set together, not one image in isolation.
2. Compare against current screenshots for old-project redesigns.
3. Mark issue locations by image name and region.
4. Decide: regenerate whole screen, regenerate detail/state sheet, fix in markdown spec, or accept as tradeoff.
5. Run `references/visual-quality-preflight.md` when the design is close to final.
6. Write the next image prompt from the critique, not from the original prompt alone.
