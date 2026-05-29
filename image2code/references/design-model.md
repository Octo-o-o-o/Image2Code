# Design Model

Use this reference when writing `design-model.yaml` and the design-system sections of an Image2Code pack.

## Purpose

`design-model.yaml` is the structured source of truth for design decisions in a pack. The markdown files explain the work for humans; the model keeps tokens, component provenance, screen mappings, and implementation constraints easy to audit.

Do not turn Image2Code into a brand-skill generator. The model serves this project-specific pack and its implementation handoff.

## When To Write It

Create or update `design-model.yaml` after `ui-spec.md` and current-state discovery, before final image prompts. Keep it in sync when images, tokens, components, or screen specs change.

For implementation mode, read `design-model.yaml` before editing code. Treat it as the exact source for tokens and component decisions unless a later review-log decision explicitly overrides it.

## Required Sections

```yaml
project: "Project Name"
mode: "redesign"
platform: "desktop"
style_policy:
  preserve_existing: true
  requested_change: ""
adjustment_level:
  level: 2
  rationale: "Component refresh while preserving navigation and workflows."
source_provenance:
  repo_context: "01-current-state.repo-context.md"
  screenshots: []
  source_files: []
  external_references: []
visual_direction:
  summary: ""
  product_fit: ""
  primary_tension: ""
tokens:
  colors: {}
  typography: {}
  spacing: {}
  radii: {}
  elevation: {}
  motion: {}
components: {}
iconography: {}
hero_or_stage: {}
screens: []
implementation_constraints: []
```

Use valid YAML. Keep values concrete: hex colors, pixel sizes, line-height values, component heights, density rules, breakpoints, file paths, and screen names.

## Provenance Rules

Every important component decision should state where it came from:

```yaml
components:
  primary_button:
    source: "observed" # observed | derived | new
    evidence:
      - "input/current-screenshots/dashboard-default-1440x900.png"
      - "src/components/Button.tsx"
    tokens:
      height: "36px"
      radius: "{radii.control}"
      background: "{colors.accent}"
    rationale: "Matches existing button geometry; color updated for contrast."
```

- `observed`: copied from the current project, screenshot, source file, or existing UI spec.
- `derived`: not directly present, but inferred from observed tokens and component rules.
- `new`: intentionally introduced by this pack. Explain why the existing system cannot satisfy the goal.

Prefer `observed` or `derived` for old-project redesigns. Use `new` sparingly and map it to implementation files in `06-implementation-plan.md`.

## Iconography

If the current product uses proprietary or unavailable icons, document both sides:

```yaml
iconography:
  observed_style:
    stroke_weight: "2px"
    corner_treatment: "rounded caps"
    fill_style: "outline"
    density: "balanced"
    evidence: ["src/icons/", "input/current-screenshots/sidebar.png"]
  implementation_kit:
    name: "lucide-react"
    reason: "Already installed and close to the observed outline geometry."
    limitations: "Not the product's historical custom glyph set."
```

Never claim a fallback kit is the original brand icon set. Prefer an icon library already used by the repository.

## Hero Or Stage

Only model a hero/stage when it matters to the product surface: landing pages, first-run screens, branded dashboards, welcome screens, or visual overview boards. For dense operational apps, this section can be explicit and quiet:

```yaml
hero_or_stage:
  applies: false
  reason: "Primary surfaces are data-dense operational screens; decorative staging would reduce scan speed."
```

When it applies, define the background, foreground subject, and their relationship in implementable terms:

```yaml
hero_or_stage:
  applies: true
  background: "subtle radial wash using {colors.accent_subtle}, no blur over content"
  subject: "product screenshot card, not decorative illustration"
  relation: "shadow-only"
  constraints:
    - "No stock imagery."
    - "Must leave first viewport's next section visible."
```

## Screen Mapping

Each important screen should connect design images to routes, states, and implementation regions:

```yaml
screens:
  - name: "Dashboard"
    route: "/dashboard"
    final_image: "images/10-dashboard-default.png"
    current_screenshot: "input/current-screenshots/dashboard-before.png"
    states: ["default", "loading", "empty", "dense-data"]
    regions:
      - "shell"
      - "filters toolbar"
      - "metric cards"
      - "results table"
```

This makes later screenshot comparison and implementation planning less dependent on visual guessing.

## Audit Checklist

Before handoff:

- `design-model.yaml` names the style policy and adjustment level.
- Tokens in `02-design-system.md` match the YAML values.
- Components include `source` and evidence/rationale for important decisions.
- Icon fallback limitations are documented when applicable.
- Screens in `03-screen-specs.md` have matching screen entries in the YAML.
- Implementation constraints are concrete enough to guide code choices.
