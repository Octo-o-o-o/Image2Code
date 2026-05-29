# Image2Code Implementation Handoff Prompt

Use this template for `handoff-prompt.md`. Replace bracketed placeholders with actual paths and project details.

```text
I have a complete image-based UI design pack at [ABSOLUTE_PACK_PATH]
Please read design-model.yaml, every markdown file, and every image in that folder before editing code. Pay special attention to ui-spec.md, the design read, visual dials, style policy, adjustment level, component provenance, preservation boundaries, and implementation constraints.

Target project: [ABSOLUTE_REPO_PATH]
Target platform: [PLATFORM_AND_VIEWPORTS]
Goal: implement the design pack as a careful UI refactor while preserving existing product behavior.

Style policy: preserve the original UI specification unless the pack explicitly says this is an intentional style change.
Adjustment level: follow the pack's selected level. Do not expand a Level 1 or Level 2 change into an architecture refactor.

First, inspect the repository structure, routes/navigation, design system, theme/token files, reusable components, and available mock or seed data. Start the local app if possible. Use browser screenshots for web/desktop surfaces, simulator/device screenshots for native apps, and capture every page covered by the pack.

Then design the implementation plan in this order:
1. Screen and region segmentation.
2. Global structure and design tokens.
3. Shared layout and navigation.
4. Shared components.
5. Page-by-page implementation.
6. Responsive and state behavior.
7. Screenshot verification.

Before changing production code, create a small demo/prototype if the design direction is broad or ambiguous. Use the fastest faithful target surface: HTML/CSS for web, SwiftUI previews or simulator-only scaffolding for iOS, or equivalent native previews. Screenshot it, compare it against the target design images, and revise the plan if the demo exposes mismatches.

Implement the refactor in the existing project style. Do not introduce a new UI framework unless it is already used by the project or I explicitly approve it. Keep behavior intact unless the design pack explicitly requests a behavior change.

After implementation, run the app locally with mock data. Capture every changed screen on the target platform into implementation-screenshots/ and compare against the design pack. If there are mismatches, decide whether to update code, update the implementation plan, or keep the existing behavior with a written reason. Continue until the screenshots match the design intent closely.

When done, update [ABSOLUTE_PACK_PATH]/06-implementation-plan.md with what was implemented, reference screenshots, implementation screenshots, remaining differences, decisions, and follow-up risks. Run sync_manifest.py so the screenshot evidence is recorded. Commit and push only if I explicitly ask for that in this task.
```

## Handoff Checklist

The generated handoff prompt must include:

- Absolute design pack path.
- Absolute repo path when known.
- Instruction to read images and markdown first.
- Instruction to read design-model.yaml as the structured source for tokens, component provenance, screen mappings, and constraints.
- Instruction to preserve routes, navigation labels, form semantics, analytics-sensitive actions, legal copy, accessibility behavior, and brand marks unless the pack explicitly approves changes.
- Browser/simulator/device screenshot comparison workflow.
- Mock data instruction.
- Demo-first instruction when appropriate.
- Screenshot evidence directory and manifest sync instruction.
- Existing-stack constraint.
- Clear commit/push policy.
