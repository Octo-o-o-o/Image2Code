# Image2Code

`Image2Code` is a Codex/Claude Code skill for image-led UI work. It helps an agent turn product briefs, screenshots, generated mockups, and repository context into a design-to-code pack with visual targets, markdown specs, implementation handoff, and screenshot-based verification.

The skill itself lives in [`image2code/`](./image2code/). The repository root contains human-facing setup notes and validation tooling.

## What It Does

- Creates a structured pack under `docs/image2code/<timestamp>-<project>/`.
- Captures repository UI context before design or implementation work.
- Preserves the existing product style unless the user explicitly requests a style change.
- Records a structured `design-model.yaml` so design reads, visual dials, tokens, component provenance, icon choices, screen mappings, and implementation constraints stay auditable.
- Supports web, desktop, mobile, iOS, Android, and other native app surfaces.
- Records design prompts, review rounds, tokens, screen specs, implementation plan, and screenshot evidence.
- Guides one-to-one implementation with before/after screenshots and visual-difference review.

## Install

### Codex

```bash
git clone https://github.com/Octo-o-o-o/Image2Code.git
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/image2code
cp -R Image2Code/image2code ~/.codex/skills/image2code
```

Restart Codex so the skill metadata is reloaded.

### Claude Code

```bash
git clone https://github.com/Octo-o-o-o/Image2Code.git
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/image2code
cp -R Image2Code/image2code ~/.claude/skills/image2code
```

Restart Claude Code, then ask it to use `$image2code` or to read `image2code/SKILL.md`.

## Quick Prompts

Create a design pack for an existing app:

```text
Use $image2code to create a complete UI redesign pack for this project. Read the repository, capture current screenshots with realistic data, generate image mockups, review them across rounds, and save the markdown spec plus final images under docs/image2code.
```

Create a native iPad/iPhone design pack:

```text
Use $image2code. This is a native iOS app. Capture simulator screenshots across the relevant iPad/iPhone sizes and orientations, preserve the current product style, generate iPadOS/iOS prototype images, and save the design pack under docs/image2code.
```

Implement an existing pack:

```text
Use $image2code to implement the design pack at docs/image2code/<pack>. Read all images and markdown first, capture current screenshots, implement in the existing project style, then save verification screenshots into implementation-screenshots and update 06-implementation-plan.md.
```

## Helper Scripts

Create a pack:

```bash
python3 image2code/scripts/init_design_pack.py \
  --project "OctoDesk" \
  --mode redesign \
  --platform desktop \
  --viewport desktop-1440x900 \
  --repo /path/to/OctoDesk
```

Create a pack that avoids local absolute paths in generated docs:

```bash
python3 image2code/scripts/init_design_pack.py \
  --project "OctoDesk" \
  --mode redesign \
  --platform ios \
  --viewport ipad-11-landscape \
  --repo /path/to/OctoDesk \
  --relative-paths
```

Collect repository UI context:

```bash
python3 image2code/scripts/collect_frontend_context.py \
  --repo /path/to/OctoDesk \
  --repo-label ../../.. \
  --exclude experiments \
  --output /path/to/OctoDesk/docs/image2code/<pack>/01-current-state.repo-context.md
```

Synchronize generated images and screenshot evidence into `manifest.json`:

```bash
python3 image2code/scripts/sync_manifest.py \
  --pack /path/to/OctoDesk/docs/image2code/<pack> \
  --status reviewed
```

Audit a pack before handoff:

```bash
python3 image2code/scripts/audit_design_pack.py \
  --pack /path/to/OctoDesk/docs/image2code/<pack>
```

Use strict relative path checks when a repository forbids machine-local paths:

```bash
python3 image2code/scripts/audit_design_pack.py \
  --pack /path/to/OctoDesk/docs/image2code/<pack> \
  --strict-relative
```

## Pack Layout

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
```

Generated images are visual targets, not the full source of truth. `design-model.yaml` and the markdown spec must capture exact text, tokens, spacing, states, accessibility, and implementation constraints because generated image text and pixel details can be imperfect.

## Validate

Run this before publishing changes to the skill:

```bash
python3 tools/validate_skill.py
```

The validation script checks required files, skill metadata, Python syntax, pack creation, manifest sync, and strict-relative audit behavior.
