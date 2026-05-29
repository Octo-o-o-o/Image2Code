#!/usr/bin/env python3
"""Create a structured Image2Code design pack folder."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


DOC_TEMPLATES = {
    "ui-spec.md": """# Current UI Specification

## Source Files

- Existing UI spec:
- Token/theme files:
- Component files:
- Screenshots:

## Style Policy

- Preserve current style by default unless the user explicitly requests a style change.
- Requested style change:

## Adjustment Level

- Selected level:
- Rationale:

## Current Visual Language

- Color:
- Typography:
- Density:
- Radius:
- Shadows:
- Icon style:

## Layout System

- Shell:
- Navigation:
- Grid:
- Spacing:
- Responsive behavior:

## Component Conventions

- Buttons:
- Forms:
- Tables:
- Cards:
- Dialogs/drawers:
- Toasts/notifications:
- Empty/loading/error states:

## Accessibility And Platform Rules

-

## Inconsistencies To Resolve

-
""",
    "00-brief.md": """# Design Brief

## Product Context

- Project:
- Mode:
- Target platform:
- Target users:

## Goals

-

## Non-Goals

-

## Page Inventory

-

## Constraints

-

## Style Policy

- Preserve current UI spec unless explicitly changing style:

## Adjustment Level

- Level:
- Rationale:

## Assumptions And Open Questions

-
""",
    "01-current-state.md": """# Current State

## Inputs

- User screenshots:
- Browser screenshots:
- Reference materials:

## Repository Findings

- Framework:
- Routes:
- Theme/CSS:
- Component system:
- Mock/seed data:

## UI Problems

| Severity | Area | Problem | Evidence |
| --- | --- | --- | --- |
| High |  |  |  |
""",
    "02-design-system.md": """# Design System

## Visual Direction

-

## Color Tokens

| Token | Value | Usage |
| --- | --- | --- |
| --color-bg |  |  |

## Typography

| Role | Size | Weight | Line Height | Usage |
| --- | --- | --- | --- | --- |

## Spacing And Layout

-

## Components

-

## States

-
""",
    "03-screen-specs.md": """# Screen Specs

## Screen Inventory

| Screen | Image | Route | States |
| --- | --- | --- | --- |

## Screen: [Name]

- Route:
- Final image:
- Layout:
- Components:
- Data:
- States:
- Responsive behavior:
- Acceptance checks:
""",
    "04-image-prompts.md": """# Image Prompts

## Prompt Log

| Image | Round | Purpose | Prompt |
| --- | --- | --- | --- |
""",
    "05-review-log.md": """# Review Log

## Round 1

| Category | Score | Notes |
| --- | --- | --- |

## Decisions

-

## Rejected Ideas

-
""",
    "06-implementation-plan.md": """# Implementation Plan

## Code Mapping

| Design Area | Existing File/Component | Planned Change |
| --- | --- | --- |

## Phases

1. Screen and region segmentation.
2. Tokens and global layout.
3. Shared components.
4. Page implementation.
5. Responsive and state polish.
6. Screenshot verification.

## Verification Targets

| Page | Target Image | Current Screenshot | Implementation Screenshot | Observed Difference | Decision | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Risks

-
""",
}

TEMPLATE_NOTE = (
    "<!-- Fill this scaffold in place, delete unused prompts, and do not append "
    "a second completed document below this template. -->\n\n"
)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "project"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="docs/image2code",
        help="Root folder for design packs. Defaults to docs/image2code",
    )
    parser.add_argument("--project", required=True, help="Human-readable project name")
    parser.add_argument(
        "--output",
        help="Exact output folder. When set, --root is ignored.",
    )
    parser.add_argument(
        "--mode",
        choices=["new", "redesign", "implementation", "revision"],
        default="redesign",
        help="Design pack mode",
    )
    parser.add_argument(
        "--platform",
        default="desktop",
        help=(
            "Target platform label, for example desktop, web, ios, android, "
            "native, mobile, or cross-platform"
        ),
    )
    parser.add_argument(
        "--viewport",
        action="append",
        dest="viewports",
        help=(
            "Viewport or device target. Repeat for multiple targets. "
            "Defaults to desktop-1440x900."
        ),
    )
    parser.add_argument("--slug", help="Optional folder slug")
    parser.add_argument("--repo", help="Absolute target repository path")
    parser.add_argument("--status", default="draft", help="Initial manifest status")
    parser.add_argument(
        "--timestamp",
        help="Override timestamp prefix as YYYYMMDD-HHMM for deterministic tests",
    )
    return parser.parse_args()


def unique_pack_dir(root: Path, timestamp: str, slug: str) -> Path:
    pack_dir = root / f"{timestamp}-{slug}"
    if not pack_dir.exists():
        return pack_dir
    counter = 2
    while True:
        candidate = root / f"{timestamp}-{slug}-{counter}"
        if not candidate.exists():
            return candidate
        counter += 1


def capture_guidance(platform: str) -> str:
    normalized = platform.strip().lower()
    if normalized in {"ios", "android", "mobile", "native"}:
        return (
            "Use platform-appropriate screenshot tooling: iOS/Android simulators "
            "or device screenshots for native apps, and browser screenshots only "
            "for web surfaces."
        )
    return (
        "Use the browser tool with mock data for web/desktop surfaces, or the "
        "platform-specific screenshot path if the project is not browser-rendered."
    )


def handoff_prompt(pack_dir: Path, repo: str | None, platform: str) -> str:
    repo_path = str(Path(repo).expanduser().resolve()) if repo else "[ABSOLUTE_REPO_PATH]"
    return f"""# Implementation Handoff Prompt

I have a complete image-based UI design pack at {pack_dir}. Please read every markdown file and every image in that folder before editing code.

Target project: {repo_path}
Target platform: {platform}
Goal: implement the design pack as a careful UI refactor while preserving existing product behavior.

First, inspect the repository structure, navigation, design system, theme/token files, reusable components, and available mock or seed data. Start the local app if possible. {capture_guidance(platform)} Capture every page covered by the pack before editing.

Then design the implementation plan in this order:
1. Screen and region segmentation.
2. Global structure and design tokens.
3. Shared layout and navigation.
4. Shared components.
5. Page-by-page implementation.
6. Responsive and state behavior.
7. Screenshot verification.

Before changing production code, create a small demo/prototype first when the design direction is broad or ambiguous. Use the fastest faithful surface for this project: HTML/CSS for web, SwiftUI previews or simulator-only scaffolding for iOS, or equivalent native previews. Screenshot it, compare it against the target design images, and revise the plan if the demo exposes mismatches.

Implement the refactor in the existing project style. Do not introduce a new UI framework unless it is already used by the project or I explicitly approve it. Keep behavior intact unless the design pack explicitly requests a behavior change.

After implementation, run the app locally with mock data. Capture every changed screen on the target platform into implementation-screenshots/ and compare against the design pack. If there are mismatches, decide whether to update code, update the implementation plan, or keep the existing behavior with a written reason. Continue until the screenshots match the design intent closely.

When done, update {pack_dir}/06-implementation-plan.md with what was implemented, verification screenshots, remaining differences, and follow-up risks. Run sync_manifest.py so screenshot evidence is recorded. Commit and push only if I explicitly ask for that in this task.
"""


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M")
    slug = slugify(args.slug or args.project)
    viewports = args.viewports or ["desktop-1440x900"]
    pack_dir = (
        Path(args.output).expanduser().resolve()
        if args.output
        else unique_pack_dir(root, timestamp, slug)
    )
    pack_dir.mkdir(parents=True, exist_ok=False)

    for dirname in [
        "input",
        "input/current-screenshots",
        "input/references",
        "input/user",
        "images",
        "reviews",
        "demo-pages",
        "browser-screenshots",
        "implementation-screenshots",
    ]:
        (pack_dir / dirname).mkdir(parents=True)

    for filename, content in DOC_TEMPLATES.items():
        (pack_dir / filename).write_text(TEMPLATE_NOTE + content, encoding="utf-8")
    (pack_dir / "handoff-prompt.md").write_text(
        handoff_prompt(pack_dir, args.repo, args.platform),
        encoding="utf-8",
    )

    manifest = {
        "project": args.project,
        "mode": args.mode,
        "platform": args.platform,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": args.status,
        "viewport_targets": viewports,
        "source_context": {
            "repo": str(Path(args.repo).expanduser().resolve()) if args.repo else "",
            "input_images": [],
            "user_screenshots": [],
            "current_screenshots": [],
            "browser_screenshots": [],
            "implementation_screenshots": [],
        },
        "final_images": [],
        "review_rounds": [],
        "implementation": {
            "target_repo": str(Path(args.repo).expanduser().resolve()) if args.repo else "",
            "handoff_prompt": "handoff-prompt.md",
        },
    }
    (pack_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(pack_dir)


if __name__ == "__main__":
    main()
