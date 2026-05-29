# Image2Code

`Image2Code` contains the `image2code` Codex skill. The skill helps Codex turn screenshots, generated UI images, and repository context into a complete design-to-code package: image targets, markdown specs, implementation handoff, and screenshot-based verification after code changes.

## Installed Skill

Skill source:

```text
/Users/wangyixiao/WorkSpace/OctoSkill/Image2Code/image2code
```

Installed Codex skill path:

```text
/Users/wangyixiao/.codex/skills/image2code
```

After installing or updating a skill, restart Codex so the skill metadata is picked up.

## When To Use It

Use `$image2code` when you want Codex to:

- Generate a full set of UI design images with Codex image generation.
- Redesign an existing desktop/web/mobile/native app from screenshots and repository context.
- Produce a structured design package under `docs/image2code`.
- Review generated designs across multiple rounds before implementation.
- Turn a design image pack into an implementation plan and UI refactor.
- Verify implementation with browser, simulator, or device screenshots.
- Handle platform-specific screenshot matrices such as iPad portrait/landscape simulator captures.

It is especially useful for old-project interface reconstruction, where Codex should read the current codebase, inspect the current UI, capture screenshots, design against existing product constraints, implement carefully, and compare the rendered result back to the image targets.

Default behavior:

- Codex first reads the current project's UI specification. If no UI spec exists, it reads the project and creates `ui-spec.md` before designing.
- Codex preserves the original UI style unless you explicitly ask to change style.
- Codex supports different adjustment levels: Level 1 polish, Level 2 UI refresh, Level 3 layout refactor, and Level 4 architecture refactor.
- Codex records implementation evidence in `implementation-screenshots/` when code is built from a pack.

## Recommended Prompts

Create a design pack for an existing project:

```text
Use $image2code to create a complete desktop UI redesign pack for this project. Read the repository, use browser screenshots with mock data, generate multiple design images with Codex image generation, review them across rounds, and save the final images plus markdown spec under docs/image2code.
```

Create from current screenshots:

```text
Use $image2code. I attached several screenshots of the current desktop UI. Please read the screenshots and this repository, produce a full image-based redesign pack, include review notes, and write a handoff prompt for one-to-one implementation.
```

Create for a native iOS/iPad app:

```text
Use $image2code. This is a native iOS app. Capture simulator screenshots across the relevant iPad/iPhone sizes and orientations, preserve the current product style, generate iPadOS/iOS prototype images, and save the design pack under docs/image2code.
```

Keep the current style and only polish details:

```text
Use $image2code. Keep the current UI specification and style. Do a Level 1 polish pass only: spacing, alignment, visual hierarchy, empty/loading/error states, contrast, and component consistency.
```

Implement an existing pack:

```text
Use $image2code to implement the design pack at /absolute/path/to/docs/image2code/<pack>. Read all images and markdown first, capture the current app with browser/simulator/device screenshots and mock data, create a small platform-appropriate demo if needed, then implement and verify with screenshots saved into implementation-screenshots.
```

## Helper Scripts

Create a design pack folder:

```bash
python3 /Users/wangyixiao/.codex/skills/image2code/scripts/init_design_pack.py \
  --project "OctoDesk" \
  --mode redesign \
  --platform desktop \
  --viewport desktop-1440x900 \
  --repo /Users/wangyixiao/WorkSpace/OctoDesk
```

Collect repository context for an old-project redesign:

```bash
python3 /Users/wangyixiao/.codex/skills/image2code/scripts/collect_frontend_context.py \
  --repo /Users/wangyixiao/WorkSpace/OctoDesk \
  --exclude experiments \
  --output /Users/wangyixiao/WorkSpace/OctoDesk/docs/image2code/<pack>/01-current-state.repo-context.md
```

Synchronize generated images and input/current/browser/implementation screenshots into `manifest.json`:

```bash
python3 /Users/wangyixiao/.codex/skills/image2code/scripts/sync_manifest.py \
  --pack /Users/wangyixiao/WorkSpace/OctoDesk/docs/image2code/<pack> \
  --status reviewed
```

Audit a design pack before final handoff:

```bash
python3 /Users/wangyixiao/.codex/skills/image2code/scripts/audit_design_pack.py \
  --pack /Users/wangyixiao/WorkSpace/OctoDesk/docs/image2code/<pack>
```

## Design Pack Layout

The default output is:

```text
docs/image2code/<YYYYMMDD-HHMM>-<project-slug>/
```

Important files:

- `00-brief.md`: product context, goals, constraints, assumptions.
- `01-current-state.md`: current UI and repository findings.
- `02-design-system.md`: tokens, typography, layout, components.
- `03-screen-specs.md`: page-by-page UI specifications.
- `04-image-prompts.md`: prompts and revision prompts.
- `05-review-log.md`: critique rounds and final decisions.
- `06-implementation-plan.md`: code mapping and verification plan.
- `handoff-prompt.md`: prompt for implementation from the pack.
- `images/`: final generated design images.
- `browser-screenshots/`: current browser screenshots.
- `implementation-screenshots/`: after-code screenshots used for verification.
- `reviews/`: rejected or intermediate image rounds.

## Notes

Generated images are visual targets, not the full source of truth. The markdown spec must capture exact text, tokens, spacing, states, and implementation constraints because generated image text and pixel details can be imperfect.
