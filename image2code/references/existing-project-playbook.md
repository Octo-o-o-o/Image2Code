# Existing Project Playbook

Use this reference for redesigning an app that already exists.

## Repository Discovery

Start with a read-only pass:

1. Read README/agent instructions plus platform config: `package.json`, workspace files, Vite/Next/Tailwind configs, Xcode/XcodeGen files, Swift Package files, Android manifests, and native app plist/manifest files.
2. Locate the screen inventory source:
   - React Router: route config, `<Route>`, `createBrowserRouter`, file-based route folders.
   - Next: `app/`, `pages/`, route groups, layout files.
   - Electron desktop shell: activity registry, shell router, navigation store, titlebar/activity bar/statusbar.
   - iOS/SwiftUI: `@main App`, `TabView`, `NavigationStack`, `NavigationSplitView`, sidebar/list definitions, UI test screenshot flows.
   - Android: activity/fragment navigation, Compose navigation graph, XML navigation graph, bottom bar/drawer registries.
   - Custom SPA: tab registry, menu registry, command palette, sidebar item arrays.
3. Locate design primitives: `src/styles`, token files, Tailwind config, design-system package, SwiftUI design-system/theme files, asset catalogs, shared components.
4. Locate realistic data: renderer-only stubs, mock services, fixtures, seeds, test factories, demo HTML, e2e setup.
5. Locate visual references: existing screenshots, previous design folders, large static HTML demos, Storybook, Playwright reports.

Run `scripts/collect_frontend_context.py` and treat the output as a starting inventory, not as proof that discovery is complete.

## Screenshot Capture Strategy

- Prefer the repo's mock, seed, preview, fixture, or renderer-only mode for UI redesign screenshots.
- For Electron apps, look for scripts such as `dev:renderer`, `RENDERER_ONLY=true`, Electron Playwright config, or renderer stubs before launching the full native app.
- For iOS apps, look for UI test screenshot helpers, debug launch arguments, seeded mock data, available simulator devices, and supported orientations in `Info.plist`.
- For Android apps, look for Compose previews, emulator-friendly seed data, and screenshot test infrastructure.
- For authenticated apps, use mock login state or seed users when available. Do not block on live credentials unless the user explicitly wants authenticated production capture.
- Capture the shell and the main task surfaces, not just home/dashboard.
- Name screenshots with route/activity, state, viewport/device, orientation, and data mode, for example `home-default-1440x900.png`, `bookshelf-ipad-pro-13-landscape-mock.png`, `files-empty-1440x900.png`.

## Screen Inventory

Write a screen matrix before image generation:

| Screen | Entry Point | Source File | Primary Data | States | Screenshot |
| --- | --- | --- | --- | --- | --- |

For old projects, include shared shell pieces separately:

- Titlebar/window controls.
- Activity bar/sidebar/navigation.
- Main content layout.
- Command palette/search overlays.
- Dialogs, drawers, toasts, statusbar, context tray.

## Design Constraints

Classify the redesign before proposing images:

- Preserve: modernize style, spacing, states, and component polish while keeping brand language, navigation, and workflows stable.
- Refresh: improve component language and hierarchy while preserving information architecture and product model.
- Overhaul: change the broad visual language or shell only when the user explicitly requests it.

Preserve:

- Product vocabulary and task flow.
- Existing component ownership boundaries where reasonable.
- Data density expected by current users.
- Accessibility, keyboard/pointer/touch, and window-size/orientation behavior.
- Platform conventions for the target surface, including desktop, web, iPadOS, iOS, Android, or Electron.
- Routes, deep links, primary navigation labels, analytics-sensitive action labels, form field names/order, legal/consent/privacy copy, and brand marks unless the user explicitly approves changing them.

Challenge:

- Decorative UI that obscures dense workflows.
- One-off components that should become shared primitives.
- Visual inconsistency between activity pages.
- New designs that require replacing the whole framework.

## Implementation Mapping

Map every visual decision to code before implementation:

| Design Decision | Token/Component | Existing File | Change Type |
| --- | --- | --- | --- |

Use this map to prevent image-only handoffs from becoming guesswork.

## Component Provenance

For every important reusable component in `design-model.yaml`, mark the decision as:

- `observed`: directly found in existing screenshots, source files, UI specs, or design-system docs.
- `derived`: inferred from observed primitives because the exact component did not exist.
- `new`: intentionally introduced to satisfy the pack goal.

Old-project redesigns should prefer `observed` and `derived`. Use `new` only when the current system lacks a pattern that the requested adjustment level allows.
