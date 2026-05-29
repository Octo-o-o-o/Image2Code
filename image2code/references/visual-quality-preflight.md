# Visual Quality Preflight

Use this reference before generating final images, before accepting a design direction, and before declaring implementation complete.

This is a compact quality gate for avoiding generic image-to-code output. It complements `design-rubric.md`; it does not replace product, accessibility, or implementation review.

## Design Read

Before image generation, write a one-line design read in `00-brief.md` and `design-model.yaml`:

```text
Reading this as: [surface type] for [audience], with a [visual language], constrained by [platform/repo/business constraints].
```

Examples:

- `Reading this as: desktop operations app for support leads, with a dense utilitarian language, constrained by existing table workflows and keyboard navigation.`
- `Reading this as: iOS onboarding flow for new readers, with a calm editorial language, constrained by native safe areas and large dynamic type.`
- `Reading this as: marketing landing page for technical buyers, with a restrained product-led language, constrained by SEO and existing brand tokens.`

If two reasonable reads diverge, ask one concise clarification. Otherwise record the read and proceed.

## Visual Dials

Set these dials in `design-model.yaml` after the design read:

```yaml
visual_dials:
  layout_variance: 1-10
  motion_intensity: 1-10
  visual_density: 1-10
  rationale: ""
```

- `layout_variance`: 1 means conventional/symmetric; 10 means highly asymmetric or editorial.
- `motion_intensity`: 1 means static except states; 10 means cinematic scroll or physics. Implementation must honor reduced motion.
- `visual_density`: 1 means sparse/gallery-like; 10 means dense operational UI.

Use the product surface to calibrate the dials. Operational dashboards often need lower variance and higher density. Landing pages can tolerate higher variance. Native mobile flows need platform clarity before visual experimentation.

## Image Granularity

Generate images at a granularity that can be implemented:

- One important product screen gets its own large final image.
- One website section gets its own large image when section-level details matter.
- One native mobile screen gets its own device/orientation image when it belongs to a flow.
- Complex states get separate state sheets or detail images.

Do not compress many sections or screens into one unreadable board. Overview boards are useful for direction, but they are not implementation targets when text, spacing, and component details become too small to inspect.

## Detail And Regeneration

If typography, buttons, spacing, or component details are unclear:

1. Generate a fresh detail image for that section/screen.
2. Regenerate the unclear section as a standalone image using the same design model.
3. Update the prompt log and review log with what changed.

Do not crop a small region out of an old overview image and treat it as the implementation source. Cropping often distorts spacing, proportions, and text scale.

## Consistency Locks

Before approving final images, verify:

- One palette logic across the pack unless a theme shift is explicitly specified.
- One radius system with documented exceptions.
- One icon family or fallback strategy.
- One typography hierarchy with predictable roles.
- CTA labels and primary actions are not duplicated with different wording.
- No generated screen drifts into a different product or brand world.

Record accepted exceptions in `05-review-log.md`.

## First View And Hero Discipline

For landing pages, home screens, onboarding first screens, and other first-impression surfaces:

- The main message must be visible without scrolling on the target viewport/device.
- The headline should be short enough to scan.
- Supporting copy should be concise.
- Primary CTA or next action should be visible and readable.
- Logo walls, dense proof lists, feature bullets, or trust strips belong below the first view unless the product requires them there.
- Decorative scroll cues are not needed.

Operational apps are different: prioritize immediate task scan, current state, filters, and primary data over dramatic hero composition.

## Mobile And Native Screens

For native or mobile packs:

- Decide platform mode: iOS, Android, or cross-platform.
- Respect safe areas, status/navigation regions, touch targets, and orientation.
- Generate enough screens for a believable flow instead of one isolated mockup.
- Keep text comfortably readable at normal viewing size.
- Avoid website layouts squeezed into a phone frame.
- Keep device framing consistent when mockup frames are used.

## Redesign Preservation

For existing projects, never silently change:

- Routes, slugs, or deep links.
- Primary navigation labels.
- Form field names, order, validation semantics, or analytics-sensitive action labels.
- Legal, consent, privacy, or compliance copy.
- Accessibility behavior that already works.
- Brand logo or wordmark.

If a proposed visual improvement requires one of these changes, record it as an explicit risk and ask for approval.

## Final Preflight

Before declaring a pack or implementation done:

- `design_read` and visual dials are filled in `design-model.yaml`.
- Images are large enough to inspect and each key screen/section has an implementation target.
- Unclear details were regenerated, not guessed from tiny crops.
- Copy has been reread for generic or nonsensical phrases.
- Buttons, forms, and navigation pass contrast, wrapping, and state checks.
- Mobile collapse or device behavior is specified.
- Reduced-motion expectations are documented when motion is above basic transitions.
- Implementation screenshots are compared against target images and recorded.
