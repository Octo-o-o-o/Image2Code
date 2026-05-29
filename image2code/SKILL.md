---
name: image2code
description: Create complete image-led UI design packs and implementation handoffs for web, desktop, mobile, and native apps. Use when Codex should act like a product UI designer and UI engineer: gather screenshots and repository context, generate multiple Codex image mockups, review and refine them, write a code-ready markdown spec, save everything inside the project, or implement an existing image pack with browser/simulator/device screenshots, mock data, visual comparison, and iterative UI refactoring. Trigger for requests about Image2Code, "设计稿", "界面重构", "视觉重构", image-based design specs, screenshot-to-redesign workflows, new product UI concepts, old project UI modernization from screenshots, iPad/iPhone/native app UI polish, or one-to-one implementation from generated design images.
---

# Image2Code

## Overview

Use this skill to turn a product brief, existing UI screenshots, or a codebase into a complete image-led design package that another Codex session can implement as code. Treat generated images as visual targets, the markdown specification as the implementation contract, and rendered screenshots as verification evidence.

## Decision Tree

- If the user asks for new designs, redesigns, visual exploration, or a designer-quality package, run **Design Pack Mode**.
- If the user points to an existing pack and asks to build it into a project, run **Implementation Mode**.
- If the user asks to revise a prior pack, run **Revision Mode** and preserve the existing pack history.

Do not skip context gathering for old projects. Existing UI, routing, component libraries, data density, and current screenshots are constraints, not optional inspiration.

## Output Contract

Default to `docs/image2code/<YYYYMMDD-HHMM>-<project-slug>/` inside the target project unless the user names a folder. Use `scripts/init_design_pack.py` to create the structure:

```bash
python3 /path/to/image2code/scripts/init_design_pack.py \
  --project "Project Name" \
  --mode redesign \
  --platform desktop \
  --viewport desktop-1440x900 \
  --repo /absolute/project/path
```

If generated documentation must avoid local absolute paths, pass `--relative-paths` or explicit `--repo-label` and `--pack-label`.

Required outputs:

- `manifest.json`: canonical file list, project metadata, and status.
- `ui-spec.md`: current UI specification; copy/summarize an existing project UI spec or generate one from the project before designing.
- `00-brief.md`: goal, product context, audience, constraints, screens, and assumptions.
- `01-current-state.md`: current screenshots, repository/design-system notes, and UI problems.
- `02-design-system.md`: tokens, layout grid, typography, colors, components, states.
- `03-screen-specs.md`: per-screen details, responsive behavior, edge states.
- `04-image-prompts.md`: prompts used for generated images and revisions.
- `05-review-log.md`: critique rounds, scores, rejected ideas, final decisions.
- `06-implementation-plan.md`: code mapping, phases, risks, acceptance checklist.
- `handoff-prompt.md`: ready-to-use prompt for implementation from the pack.
- `images/`: generated final design images.
- `input/`: user-provided screenshots, current UI captures, references.
- `reviews/`: intermediate generated images and critique artifacts.
- `demo-pages/`: generated demo-page images or later HTML demo artifacts.
- `implementation-screenshots/`: after-code screenshots used to verify image-to-code fidelity.

Read `references/pack-schema.md` before writing or auditing the package.
After adding or renaming generated images/screenshots, run:

```bash
python3 /path/to/image2code/scripts/sync_manifest.py \
  --pack /absolute/pack/path \
  --status reviewed
```

Before declaring a pack done, run:

```bash
python3 /path/to/image2code/scripts/audit_design_pack.py \
  --pack /absolute/pack/path
```

Use `--strict-relative` when the target repository forbids local absolute paths in docs.

## Design Pack Mode

1. **Gather context**
   - For an existing project, inspect routes/navigation, design system, CSS/theme/token files, package scripts, native app config, sample data paths, and user-provided screenshots.
   - Run `scripts/collect_frontend_context.py` for existing projects and save its output into the pack before writing `01-current-state.md`:

     ```bash
     python3 /path/to/image2code/scripts/collect_frontend_context.py \
       --repo /absolute/project/path \
       --output /absolute/pack/path/01-current-state.repo-context.md
     ```

   - If repository docs prohibit absolute paths, pass `--repo-label` with a relative label such as `../../..`.
   - When creating the pack itself for such repositories, pass `--relative-paths` to `init_design_pack.py` so `manifest.json` and `handoff-prompt.md` are compatible with strict-relative audits.
   - If the repository has noisy scratch, vendor, or generated folders, pass repeatable `--exclude` values so the report focuses on the shipping UI.
   - If a local app can run, capture each important screen with mock or seeded data before designing. Use browser screenshots for web/desktop surfaces, simulator/device screenshots for native mobile/tablet apps, and record device, OS, orientation, and data mode.
   - For a new project, infer missing details conservatively and write assumptions in `00-brief.md`.
   - Read `references/existing-project-playbook.md` for old-project redesigns, Electron apps, SPAs, and apps without URL routes.

2. **Establish the UI specification**
   - Always search for existing UI specifications before designing: `design-system/`, `docs/design/`, `docs/ui-spec.md`, token files, Tailwind/theme config, component docs, Storybook, old design folders, and screenshots.
   - If a UI spec exists, summarize the applicable rules into `ui-spec.md` and cite the source files.
   - If no UI spec exists, generate `ui-spec.md` from the repository and screenshots before image generation. Include current style, layout rules, tokens, component conventions, density, accessibility, responsive behavior, and known inconsistencies.
   - Default style policy: preserve the current UI specification and visual language unless the user explicitly asks to change style.
   - If the user explicitly asks to change style, record the new style direction, what must remain compatible, and which old rules are intentionally replaced.

3. **Set the adjustment level**
   - Level 1, polish: smallest possible detail improvements, spacing, alignment, copy density, contrast, state polish.
   - Level 2, UI refresh: component-level UI improvements while preserving information architecture and workflows.
   - Level 3, layout refactor: page layout and navigation restructuring while preserving core product model.
   - Level 4, architecture refactor: broad shell/information architecture redesign, cross-page workflow changes, and deeper implementation planning.
   - If the user does not specify a level, choose the least invasive level that satisfies the request and write the choice in `00-brief.md`.

4. **Define the screen inventory**
   - List primary pages, secondary pages, modals, empty/loading/error states, dense-data states, and responsive breakpoints.
   - Prioritize the product's primary platform: desktop screens for desktop apps, device/orientation matrices for native mobile/tablet apps, and narrow variants when the product needs them.

5. **Generate an image set**
   - Use the Codex image generation tool for bitmap outputs: design overview board, design-system sheet, each major screen, key states, and demo-page images.
   - Include the style policy and adjustment level in every image prompt.
   - Generate images with realistic product data and the target viewport/device, not generic marketing art.
   - Keep image text short and also record all precise text/tokens in markdown because generated text may be imperfect.
   - If the image tool does not expose filesystem paths, do not pretend files were saved. Save available outputs through the app if possible, or ask the user to attach/export them before finalizing the pack.

6. **Review and refine**
   - Run at least two critique passes unless the user explicitly asks for a quick draft.
   - Score each pass against `references/design-rubric.md`.
   - Regenerate weak screens or targeted details. Keep rejected versions in `reviews/` when available.
   - Stop only when the design is coherent across screens, technically implementable, and the remaining tradeoffs are written down.

7. **Write the implementation contract**
   - Convert visual choices into concrete tokens, component specs, layout measurements, state rules, and page-by-page acceptance checks.
   - Map designs onto existing code locations when a repository exists.
   - Generate `handoff-prompt.md` from `references/implementation-handoff.md`.
   - Replace template placeholders in markdown files instead of appending a second completed document below the scaffold.

Read `references/image-generation-playbook.md` before the first image generation round.

## Implementation Mode

When the user asks to implement an existing pack:

1. Read every image and markdown file in the pack before editing code.
2. Capture the current app with browser, simulator, or device screenshots and mock data.
3. Build a small demo/prototype first when the design direction is broad, ambiguous, or risky. Use the fastest faithful platform surface and screenshots to compare the demo with the target images.
4. Create an implementation plan that starts with screen/region segmentation, then global structure/tokens, shared components, page-level details, and verification evidence.
5. Implement in the existing project style. Do not introduce a new UI framework unless the repo already uses it or the user approves it.
6. Re-run the app, capture screenshots for each changed screen into `implementation-screenshots/`, compare against the design pack, and iterate.
7. Commit or push only if the user explicitly requested that delivery step.

Use `references/image-to-code-workflow.md` and `references/implementation-handoff.md` for the detailed implementation prompt pattern.

## Revision Mode

When revising a previous pack:

- Keep the original files and add a dated section to `05-review-log.md`.
- Write what changed and why before generating replacement images.
- Update only the affected screen specs, image prompts, and implementation checks.
- Preserve stable design tokens unless the revision intentionally changes the system.

## Quality Gates

Before declaring the pack complete:

- Every generated final image has a matching row in `manifest.json`.
- `ui-spec.md` exists and states whether the design preserves the original style or intentionally changes it.
- `00-brief.md` states the adjustment level and why that level fits the request.
- Every important current page or intended new page has a spec in `03-screen-specs.md`.
- The pack includes a textual token table. Include a design-system/tokens image when the user requested a full visual system or the implementation needs one; otherwise explain the omission in `05-review-log.md`.
- The review log explains why the final direction won over alternatives.
- Existing-project packs include codebase findings and current UI screenshots or a clear reason they could not be captured.
- The handoff prompt is self-contained and points to the pack path. Use absolute paths by default; use relative paths when the target repository's documentation rules forbid local absolute paths.
- `scripts/audit_design_pack.py` passes, using `--strict-relative` when the project requires relative documentation links.
- Implementation work records reference screenshots, actual screenshots, observed differences, and final decisions in `06-implementation-plan.md`.

## References

- `references/research-notes.md`: prior art and design-to-code lessons from public tools and papers.
- `references/image-to-code-workflow.md`: implementation loop from image target to code, including segmentation and visual verification.
- `references/pack-schema.md`: package directory and markdown structure.
- `references/existing-project-playbook.md`: repository discovery, screen inventory, and screenshot capture guidance for existing apps.
- `references/image-generation-playbook.md`: prompt templates and review loops for generated UI images.
- `references/design-rubric.md`: visual, product, and implementation scoring criteria.
- `references/implementation-handoff.md`: prompt template for one-to-one implementation from a pack.
