#!/usr/bin/env python3
"""Audit an Image2Code design pack for common handoff problems."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = [
    "manifest.json",
    "ui-spec.md",
    "00-brief.md",
    "01-current-state.md",
    "02-design-system.md",
    "03-screen-specs.md",
    "04-image-prompts.md",
    "05-review-log.md",
    "06-implementation-plan.md",
    "handoff-prompt.md",
]

REQUIRED_MANIFEST_FIELDS = [
    "project",
    "mode",
    "platform",
    "created_at",
    "status",
    "viewport_targets",
    "source_context",
    "final_images",
    "implementation",
]

VALID_STATUSES = {"draft", "ready", "reviewed", "final", "implemented"}
IMAGE_EXTENSIONS = {".gif", ".jpg", ".jpeg", ".png", ".webp"}

REQUIRED_HEADINGS = {
    "ui-spec.md": ["## Style Policy", "## Adjustment Level"],
    "00-brief.md": ["## Goals", "## Constraints", "## Adjustment Level"],
    "01-current-state.md": ["## Inputs", "## Repository Findings", "## UI Problems"],
    "02-design-system.md": ["## Color Tokens", "## Typography", "## Components"],
    "03-screen-specs.md": ["## Screen Inventory"],
    "04-image-prompts.md": ["## Prompt Log"],
    "05-review-log.md": ["## Round 1", "## Decisions"],
    "06-implementation-plan.md": ["## Code Mapping", "## Phases", "## Verification Targets"],
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"\[ABSOLUTE_[A-Z_]+\]"),
    re.compile(r"Screen:\s*\[Name\]"),
    re.compile(r"^- Project:\s*$", re.MULTILINE),
    re.compile(r"^- Route:\s*$", re.MULTILINE),
    re.compile(r"\| High \|  \|  \|  \|"),
    re.compile(r"\| Category \| Score \| Notes \|"),
]

ABSOLUTE_PATH_PATTERN = re.compile(r"(?<!\w)/(?:Users|home|tmp|var|private)/[^\s)`>]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, help="Design pack directory")
    parser.add_argument(
        "--strict-relative",
        action="store_true",
        help="Fail if markdown/manifest files contain local absolute filesystem paths",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Exit nonzero when warnings are present",
    )
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def image_files(root: Path, dirname: str) -> list[Path]:
    directory = root / dirname
    if not directory.exists():
        return []
    return sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def referenced_paths(manifest: dict[str, object]) -> list[str]:
    paths: list[str] = []
    for item in manifest.get("final_images", []) or []:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
    source_context = manifest.get("source_context")
    if isinstance(source_context, dict):
        for key in ("input_images", "user_screenshots", "current_screenshots", "browser_screenshots"):
            value = source_context.get(key)
            if isinstance(value, list):
                paths.extend(item for item in value if isinstance(item, str))
        value = source_context.get("implementation_screenshots")
        if isinstance(value, list):
            paths.extend(item for item in value if isinstance(item, str))
    implementation = manifest.get("implementation")
    if isinstance(implementation, dict) and isinstance(implementation.get("handoff_prompt"), str):
        paths.append(implementation["handoff_prompt"])
    return paths


def main() -> None:
    args = parse_args()
    pack = Path(args.pack).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not pack.exists():
        raise SystemExit(f"Pack does not exist: {pack}")

    for required in REQUIRED_FILES:
        if not (pack / required).is_file():
            errors.append(f"Missing required file: {required}")

    manifest: dict[str, object] = {}
    manifest_path = pack / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"manifest.json is invalid JSON: {exc}")

    for markdown_path in sorted(pack.glob("*.md")):
        text = read_text(markdown_path)
        h1s = re.findall(r"^#\s+", text, flags=re.MULTILINE)
        if len(h1s) != 1:
            errors.append(f"{rel(markdown_path, pack)} should contain exactly one H1; found {len(h1s)}")
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                warnings.append(f"{rel(markdown_path, pack)} appears to contain template placeholder text")
                break
        for heading in REQUIRED_HEADINGS.get(markdown_path.name, []):
            if heading not in text:
                warnings.append(f"{rel(markdown_path, pack)} missing expected section: {heading}")
        if args.strict_relative and ABSOLUTE_PATH_PATTERN.search(text):
            errors.append(f"{rel(markdown_path, pack)} contains local absolute filesystem paths")

    if manifest:
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                errors.append(f"manifest.json missing required field: {field}")

        status = manifest.get("status")
        if isinstance(status, str) and status not in VALID_STATUSES:
            warnings.append(f"manifest.json uses nonstandard status: {status}")

        viewports = manifest.get("viewport_targets")
        if not isinstance(viewports, list) or not viewports:
            errors.append("manifest.json viewport_targets must be a non-empty list")

        images = [rel(path, pack) for path in image_files(pack, "images")]
        final_paths = [
            item.get("path")
            for item in manifest.get("final_images", []) or []
            if isinstance(item, dict)
        ]
        missing_rows = sorted(set(images) - set(final_paths))
        stale_rows = sorted(path for path in final_paths if isinstance(path, str) and not (pack / path).exists())
        if missing_rows:
            errors.append(f"Images missing manifest rows: {', '.join(missing_rows)}")
        if stale_rows:
            errors.append(f"Manifest references missing image files: {', '.join(stale_rows)}")

        for path in referenced_paths(manifest):
            if path.startswith("/"):
                if args.strict_relative:
                    errors.append(f"Manifest contains absolute path: {path}")
                continue
            if not (pack / path).exists():
                warnings.append(f"Manifest references path not found in pack: {path}")

        if args.strict_relative and ABSOLUTE_PATH_PATTERN.search(json.dumps(manifest, ensure_ascii=False)):
            errors.append("manifest.json contains local absolute filesystem paths")

        source_context = manifest.get("source_context")
        implementation_screenshots = []
        if isinstance(source_context, dict):
            implementation_screenshots = source_context.get("implementation_screenshots") or []
        if status == "implemented" and not implementation_screenshots:
            warnings.append(
                "Pack status is implemented but manifest has no implementation screenshots"
            )

    if not image_files(pack, "images"):
        warnings.append("No final generated images found under images/")
    if not image_files(pack, "input") and not image_files(pack, "browser-screenshots"):
        warnings.append("No input/current/browser screenshots found")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        raise SystemExit(1)
    if warnings and args.fail_on_warnings:
        raise SystemExit(2)
    print("Design pack audit passed")


if __name__ == "__main__":
    main()
