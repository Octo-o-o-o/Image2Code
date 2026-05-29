# Image2Code Pack Schema

Use this reference when creating, revising, or auditing a design pack.

## Directory

```text
docs/image2code/<YYYYMMDD-HHMM>-<project-slug>/
  manifest.json
  design-model.yaml
  ui-spec.md
  00-brief.md
  01-current-state.md
  02-design-system.md
  03-screen-specs.md
  04-image-prompts.md
  05-review-log.md
  06-implementation-plan.md
  handoff-prompt.md
  input/
  images/
  reviews/
  demo-pages/
  browser-screenshots/
  implementation-screenshots/
  input/current-screenshots/
  input/user/
  input/references/
```

## Manifest Fields

Use relative paths from the pack root.

```json
{
  "project": "Project Name",
  "mode": "redesign",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "platform": "desktop|web|ios|android|native|mobile|cross-platform",
  "status": "draft|ready|reviewed|final|implemented",
  "design_model": "design-model.yaml",
  "viewport_targets": ["desktop-1440x900"],
  "source_context": {
    "repo": "/absolute/path",
    "input_images": [],
    "user_screenshots": [],
    "current_screenshots": [],
    "browser_screenshots": [],
    "implementation_screenshots": []
  },
  "final_images": [
    {
      "path": "images/10-dashboard-default.png",
      "screen": "Dashboard",
      "viewport": "desktop-1440x900",
      "purpose": "Canonical default state",
      "source_prompt": "04-image-prompts.md#dashboard-default"
    }
  ],
  "review_rounds": [],
  "implementation": {
    "target_repo": "/absolute/path",
    "handoff_prompt": "handoff-prompt.md"
  }
}
```

## File Requirements

`design-model.yaml`:

- Structured source of truth for style policy, adjustment level, design provenance, tokens, components, iconography, optional hero/stage treatment, screen mapping, and implementation constraints.
- Includes `design_read` and `visual_dials` so image generation and implementation are calibrated to the surface type, audience, motion needs, and density.
- Important components use `source: observed|derived|new` with evidence and rationale.
- Token values match `02-design-system.md`; screen entries match `03-screen-specs.md`.
- Icon fallback limitations are documented when the original icon set is proprietary or unavailable.
- Read `references/design-model.md` before writing or revising it.

`00-brief.md`:

- Product purpose, users, platform, technical stack if known.
- One-line design read and visual dials.
- Goals and non-goals.
- Page inventory.
- Assumptions and open questions.
- Style policy: preserve current style or intentionally change style.
- Adjustment level: Level 1 polish, Level 2 UI refresh, Level 3 layout refactor, or Level 4 architecture refactor.

`ui-spec.md`:

- Existing UI spec source files, or a note that no canonical spec existed.
- Current visual language: color, type, density, radius, shadows, icons, surface hierarchy.
- Current layout system: shell, navigation, grid, spacing, responsive behavior.
- Current component conventions: buttons, forms, tables, cards, drawers, dialogs, toasts, empty/loading/error states.
- Accessibility and platform conventions.
- Inconsistencies found in the current project.
- Style policy for this pack: preserve original UI spec by default, or explicit style change with rationale.
- Adjustment level and allowed scope.

`01-current-state.md`:

- Current screenshots or references.
- Device/browser matrix for captured screenshots, including OS, viewport/device, orientation, and data mode when known.
- Codebase findings: framework, routes, theme files, component boundaries.
- Problems ranked by severity: structure, hierarchy, density, visual style, accessibility, responsiveness.

`02-design-system.md`:

- Color tokens with hex values and usage.
- Typography scale, weights, line heights.
- Spacing scale, grid, panel widths, toolbar sizes.
- Component specs for navigation, tables, forms, filters, cards, modals, charts, notifications, empty/error/loading states.

`03-screen-specs.md`:

- One section per screen.
- State matrix: default, loading, empty, error, overflow/dense data, permission/disabled states.
- Layout measurements and responsive changes.
- Image references for every screen.

`04-image-prompts.md`:

- Exact prompts used for each generated image.
- Inputs included: screenshots, design constraints, viewport, style direction.
- Revision prompts and what each revision attempted to fix.

`05-review-log.md`:

- Critique round summary.
- Scores from `design-rubric.md`.
- Issues found, action taken, final decision.
- Rejected ideas and why.
- Visual-quality preflight decisions from `references/visual-quality-preflight.md`.

`06-implementation-plan.md`:

- Code mapping from design system to repo files.
- Stepwise implementation plan.
- Screen and region segmentation for complex targets.
- Verification plan with browser, simulator, or device screenshot targets.
- Reference design image, current screenshot, implementation screenshot, observed difference, decision, and status for each target.
- Preservation boundaries for routes, navigation labels, form semantics, legal copy, accessibility behavior, analytics-sensitive actions, and brand marks.
- Risks and fallback decisions.

`handoff-prompt.md`:

- Self-contained prompt for implementing the pack in the target repository.
- Design pack path. Use an absolute path by default, or a relative path when repository documentation rules require it.
- Browser, simulator, or device screenshot and mock data instructions depending on platform.
- Demo-first instruction when appropriate.

## Audit

Before final handoff, run:

```bash
python3 scripts/audit_design_pack.py --pack /absolute/pack/path
```

Use `--strict-relative` if the target repository requires generated documentation to avoid local absolute filesystem paths.

## Naming

Use stable numeric prefixes:

- `00-` to `09-` for docs.
- `10-` to `39-` for final screen images.
- `40-` to `59-` for states and responsive images.
- `90-` to `99-` for overview boards and design-system sheets.

Prefer names like `10-dashboard-default.png`, `11-dashboard-empty.png`, `20-detail-panel.png`, `90-design-system-board.png`.
