# Image Generation Playbook

Use this reference before generating UI design images with Codex image generation.

## Image Set

For a complete design pack, generate the images that match the target platform:

- Overview board: product direction, core screens, design principles.
- Design-system board: tokens, components, spacing, states.
- Canonical page images: one image per major screen.
- Section-level images for website/landing-page packs when section details need to be implemented separately.
- State sheets: empty, loading, error, dense data, hover/selected, modal/drawer.
- Responsive/device/orientation variants when they matter.
- Detail/extraction images when typography, buttons, spacing, icons, or component internals are too small to inspect.
- Demo-page image: a stitched view showing how the experience feels as a flow.

Prefer more readable implementation-target images over one compressed board. Overview boards help direction, but final code should not depend on tiny text or tiny components in a collage.

## Prompt Structure

Use this structure for each generated image:

```text
Create a high-fidelity [target platform] UI design image for [product/page].
Viewport/device: [1440x900, iPad Pro 13 landscape, iPhone portrait, or target].
Context: [product domain, user role, current UI problems, repo constraints].
Style policy: [preserve existing UI spec by default, or explicit style-change direction].
Adjustment level: [Level 1 polish / Level 2 UI refresh / Level 3 layout refactor / Level 4 architecture refactor].
Layout: [navigation, grid, major regions, component hierarchy].
Visual system: [palette, type, spacing, density, radius, icon style].
Design model: [cite the relevant design-model.yaml tokens/components/screens and any observed/derived/new component constraints].
Content: [realistic data and labels; keep text short and readable].
States: [default/empty/error/loading/etc.].
Implementation constraints: [existing framework/components, avoid impossible effects].
Output: single clean UI screenshot/prototype, no browser chrome unless explicitly needed, no marketing mockup frame.
```

For existing UI redesigns, include what must remain recognizable: route names, product vocabulary, critical workflows, and current data density.

If the user did not explicitly ask for a new style, prompts must inherit the current `ui-spec.md` visual language. Do not use unrelated trends, palettes, or decorative systems just because the user asked for a redesign.

When `design-model.yaml` exists, prompts must use it as the exact source for tokens, component provenance, icon rules, and screen mappings. If a prompt needs a visual rule not yet in the model, update the model and markdown spec first.

## Granularity Rules

- One important app screen gets its own large image.
- One important website section gets its own large horizontal image when section fidelity matters.
- One native mobile screen gets its own device/orientation image when it belongs to a flow.
- Complex modals, tables, pricing blocks, forms, onboarding screens, and dense states get separate detail/state images.

Do not crop a region out of an old overview image and promote it to source-of-truth. If a detail matters and is unclear, regenerate a fresh standalone image that preserves the same design model.

## Iteration Prompts

After critique, write prompts that name the concrete defects:

```text
Regenerate the [screen] design while preserving [approved parts].
Fix these issues: [specific hierarchy/spacing/component/state problems].
Keep the same visual tokens: [colors/type/radius/grid].
Do not add [rejected ideas].
```

## Annotation Images

Generated annotation boards are useful, but never rely on them as the only spec because image text can be unreliable. Mirror every measurement, token, and decision in markdown.

## Good Constraints

- Prefer real workflow screens over moodboards.
- Keep app redesigns quiet, dense, and operational unless the product is consumer/editorial/game-like.
- Use stable, implementable primitives: nav, toolbar, table, detail pane, cards, forms, charts, modal, drawer.
- Use explicit viewport sizes, device names, or orientation targets.
- Use consistent component names across prompts and docs.

## Avoid

- Purely decorative hero layouts for operational apps.
- Vague terms like "modern", "beautiful", or "premium" without product-specific constraints.
- One-color palettes dominated by a single hue family.
- Tiny unreadable labels in generated images.
- Shadows, blurs, glass, or gradients that the existing stack cannot reproduce cleanly.
- Treating generated visual artifacts as exact copy, icon, or data requirements.
