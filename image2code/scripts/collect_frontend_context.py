#!/usr/bin/env python3
"""Collect read-only UI context for an Image2Code design pack."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".claude",
    ".git",
    ".next",
    ".pnpm-store",
    ".staging",
    ".swiftpm",
    ".workflow",
    ".wrangler",
    "DerivedData",
    "build",
    "coverage",
    "dist",
    "dist-electron",
    "dist-mobile",
    "experiments",
    "experimental",
    "gpt-img-2-design",
    "image2code",
    "node_modules",
    "out",
    "playwright-report",
    "release",
    "release-asar",
    "release-local",
    "test-results",
    "tmp",
    "temp",
    "Vendor",
    "vendor",
}

EXTRA_EXCLUDES: set[str] = set()

TEXT_EXTENSIONS = {
    ".cjs",
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".pbxproj",
    ".plist",
    ".scss",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
    ".xml",
    ".yaml",
    ".yml",
}

CONFIG_NAMES = {
    "AndroidManifest.xml",
    "Info.plist",
    "Package.swift",
    "build.gradle",
    "build.gradle.kts",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "nuxt.config.ts",
    "package.json",
    "pnpm-workspace.yaml",
    "postcss.config.js",
    "project.yml",
    "tailwind.config.js",
    "tailwind.config.ts",
    "vite.config.js",
    "vite.config.mjs",
    "vite.config.ts",
    "workspace.yml",
    "xcodegen.yml",
}

UI_PATTERNS = [
    r"createBrowserRouter",
    r"createHashRouter",
    r"BrowserRouter",
    r"HashRouter",
    r"<Route\b",
    r"ActivityRouter",
    r"ALL_ACTIVITY_IDS",
    r"viewRegistry",
    r"navigationStore",
    r"currentActivity",
    r"@main\s+struct",
    r":\s*App\s*\{",
    r":\s*View\s*\{",
    r"NavigationSplitView",
    r"NavigationStack",
    r"TabView",
    r"List\s*\{",
    r"ContentUnavailableView",
    r"UISupportedInterfaceOrientations",
]

STYLE_PATH_KEYWORDS = ("color", "designsystem", "style", "theme", "token")

MOCK_PATH_KEYWORDS = (
    "demo",
    "factory",
    "fixture",
    "mock",
    "sample",
    "seed",
    "stub",
)

VISUAL_PATH_KEYWORDS = (
    "design",
    "gpt-img-2-design",
    "image2code",
    "playwright-report",
    "screenshot",
    "snapshot",
    "storybook",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Repository root to inspect")
    parser.add_argument("--output", help="Write markdown report to this path")
    parser.add_argument("--max-files", type=int, default=120, help="Maximum files per section")
    parser.add_argument(
        "--repo-label",
        help=(
            "Repository label to print in the report. Use a relative label such "
            "as ../../.. when project documentation must avoid absolute paths."
        ),
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help=(
            "Additional directory, file name, or path substring to exclude. "
            "Repeat for multiple values."
        ),
    )
    return parser.parse_args()


def should_skip(path: Path) -> bool:
    if any(
        part in SKIP_DIRS or (part.startswith(".") and part not in {".", ".."})
        for part in path.parts
    ):
        return True
    path_text = str(path)
    return any(
        exclude and (exclude in path.parts or exclude in path_text)
        for exclude in EXTRA_EXCLUDES
    )


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        current_path = Path(current)
        for file_name in files:
            path = current_path / file_name
            if should_skip(path):
                continue
            if path.suffix in TEXT_EXTENSIONS:
                yield path


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def read_text(path: Path, limit: int = 80_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return ""


def find_named(root: Path, names: set[str], max_files: int) -> list[str]:
    matches: list[str] = []
    for path in iter_files(root):
        if path.name in names:
            matches.append(rel(path, root))
            if len(matches) >= max_files:
                break
    return matches


def find_special_dirs(root: Path, max_files: int, suffixes: set[str] | None = None) -> list[str]:
    suffixes = suffixes or {".appiconset", ".colorset", ".xcassets", ".xcodeproj", ".xcworkspace"}
    matches: list[str] = []
    for path in root.rglob("*"):
        if len(matches) >= max_files:
            break
        if should_skip(path):
            continue
        if path.is_dir() and path.suffix in suffixes:
            matches.append(rel(path, root))
    return sorted(dict.fromkeys(matches))[:max_files]


def find_path_keywords(root: Path, keywords: tuple[str, ...], max_files: int) -> list[str]:
    matches: list[str] = []
    for path in iter_files(root):
        lowered = rel(path, root).lower()
        if any(keyword in lowered for keyword in keywords):
            matches.append(rel(path, root))
            if len(matches) >= max_files:
                break
    return matches


def find_content_patterns(
    root: Path,
    patterns: list[str],
    max_files: int,
) -> list[dict[str, str]]:
    compiled = [(pattern, re.compile(pattern)) for pattern in patterns]
    matches: list[dict[str, str]] = []
    for path in iter_files(root):
        relative_path = rel(path, root)
        text = read_text(path)
        if not text:
            continue
        found = [pattern for pattern, regex in compiled if regex.search(text)]
        if found:
            matches.append({"path": relative_path, "signals": ", ".join(found[:5])})
            if len(matches) >= max_files:
                break
    return matches


def find_style_files(root: Path, max_files: int) -> list[str]:
    matches: list[str] = []
    style_names = {
        "colors_and_type.css",
        "global.css",
        "tailwind.config.js",
        "tailwind.config.ts",
        "tokens.css",
        "variables.css",
    }
    for path in iter_files(root):
        relative_path = rel(path, root)
        lowered = relative_path.lower()
        name = path.name.lower()
        path_parts = {part.lower() for part in path.parts}
        is_style = (
            name in style_names
            or lowered.startswith(("src/styles/", "app/styles/", "design-system/"))
            or "designsystem" in path_parts
            or "design-system" in path_parts
            or lowered.endswith(("/styles.css", "/theme.swift", "/tokens.swift"))
            or any(keyword in name for keyword in STYLE_PATH_KEYWORDS)
            and path.suffix in {".css", ".scss", ".swift", ".ts", ".tsx", ".md", ".json"}
        )
        if is_style:
            matches.append(relative_path)
    matches.extend(find_special_dirs(root, max_files, {".appiconset", ".colorset", ".xcassets"}))
    return sorted(dict.fromkeys(matches))[:max_files]


def package_summaries(root: Path, max_files: int) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    for path in sorted(root.rglob("package.json")):
        if should_skip(path):
            continue
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        scripts = data.get("scripts") or {}
        summaries.append(
            {
                "path": rel(path, root),
                "name": data.get("name", ""),
                "scripts": {
                    key: scripts[key]
                    for key in sorted(scripts)
                    if key
                    in {
                        "dev",
                        "dev:direct",
                        "dev:renderer",
                        "dev:vite",
                        "preview",
                        "storybook",
                        "test:e2e",
                        "test:e2e:electron",
                    }
                    or key.startswith("dev:")
                },
            }
        )
        if len(summaries) >= max_files:
            break
    return summaries


def platform_hints(root: Path) -> list[str]:
    hints: list[str] = []
    names = {path.name for path in iter_files(root)}
    special_dirs = set(find_special_dirs(root, 200))
    if "package.json" in names:
        hints.append("Web/Node project signals found (`package.json`).")
    if "project.yml" in names or "Package.swift" in names or any(
        path.endswith((".xcodeproj", ".xcworkspace")) for path in special_dirs
    ):
        hints.append("Apple native project signals found (Xcode/XcodeGen/Swift Package).")
    if "Info.plist" in names:
        hints.append("iOS/macOS app configuration found (`Info.plist`).")
    if "AndroidManifest.xml" in names or "build.gradle" in names or "build.gradle.kts" in names:
        hints.append("Android project signals found.")
    if not hints:
        hints.append("No obvious platform marker found; inspect repository structure manually.")
    return hints


def markdown_list(items: list[str]) -> str:
    if not items:
        return "- None found\n"
    return "".join(f"- `{item}`\n" for item in items)


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "| Path | Signals |\n| --- | --- |\n| None found |  |\n"
    body = "\n".join(f"| `{row['path']}` | {row['signals']} |" for row in rows)
    return f"| Path | Signals |\n| --- | --- |\n{body}\n"


def build_report(root: Path, max_files: int, repo_label: str | None = None) -> str:
    package_info = package_summaries(root, max_files)
    config_files = sorted(
        dict.fromkeys(find_named(root, CONFIG_NAMES, max_files) + find_special_dirs(root, max_files))
    )[:max_files]
    style_files = find_style_files(root, max_files)
    mock_files = find_path_keywords(root, MOCK_PATH_KEYWORDS, max_files)
    visual_refs = find_path_keywords(root, VISUAL_PATH_KEYWORDS, max_files)
    ui_signals = find_content_patterns(root, UI_PATTERNS, max_files)

    packages_md = ""
    for package in package_info:
        packages_md += f"### `{package['path']}`\n\n"
        packages_md += f"- Name: `{package['name']}`\n"
        scripts = package["scripts"]
        if scripts:
            packages_md += "- Useful scripts:\n"
            for key, value in scripts.items():
                packages_md += f"  - `{key}`: `{value}`\n"
        else:
            packages_md += "- Useful scripts: none found\n"
        packages_md += "\n"
    if not packages_md:
        packages_md = "No package.json files found.\n"

    platform_md = "".join(f"- {hint}\n" for hint in platform_hints(root))
    label = repo_label or str(root)

    return f"""# UI Context Report

Repository: `{label}`

## Platform Hints

{platform_md}
## Package Scripts

{packages_md}## App And Config Files

{markdown_list(config_files)}
## Screen And Navigation Signals

{markdown_table(ui_signals)}
## Design System And Style Files

{markdown_list(style_files)}
## Mock, Stub, Fixture, Demo Data

{markdown_list(mock_files)}
## Visual References

{markdown_list(visual_refs)}
## Dry-Run Notes

- Confirm the real screen inventory manually; this report surfaces likely entry points, not a complete audit.
- For web/desktop apps, prefer mock or renderer-only browser screenshots.
- For native apps, prefer simulator/device screenshots and record device, OS, orientation, and data mode.
- Copy important findings into `01-current-state.md` and update `manifest.json`.
"""


def main() -> None:
    args = parse_args()
    global EXTRA_EXCLUDES
    EXTRA_EXCLUDES = set(args.exclude)
    root = Path(args.repo).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Repository does not exist: {root}")
    report = build_report(root, args.max_files, args.repo_label)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
