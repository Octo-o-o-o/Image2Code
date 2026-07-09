#!/usr/bin/env python3
"""Audit static properties of an Image2HTML prototype."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


PASCAL_CASE = re.compile(r"^[A-Z][A-Za-z0-9]*$")


class PrototypeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.components: list[str] = []
        self.screens: list[str] = []
        self.screen_targets: list[str] = []
        self.image_sources: list[str] = []
        self.styles: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        if "data-component" in attr_map:
            self.components.append(attr_map["data-component"])
        if "data-screen" in attr_map:
            self.screens.append(attr_map["data-screen"])
        if "data-screen-target" in attr_map:
            self.screen_targets.append(attr_map["data-screen-target"])
        if tag.lower() == "img" and "src" in attr_map:
            self.image_sources.append(attr_map["src"])
        if "style" in attr_map:
            self.styles.append(attr_map["style"])


def parse_name_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"Expected name=path, got {value!r}")
    name, raw_path = value.split("=", 1)
    if not name:
        raise argparse.ArgumentTypeError("Image name cannot be empty")
    return name, Path(raw_path)


def read_png_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) >= 24 and header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR":
        return struct.unpack(">II", header[16:24])
    return None


def read_jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            marker_prefix = handle.read(1)
            if not marker_prefix:
                return None
            if marker_prefix != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if length < 2:
                return None
            if marker in {
                b"\xc0",
                b"\xc1",
                b"\xc2",
                b"\xc3",
                b"\xc5",
                b"\xc6",
                b"\xc7",
                b"\xc9",
                b"\xca",
                b"\xcb",
                b"\xcd",
                b"\xce",
                b"\xcf",
            }:
                data = handle.read(5)
                if len(data) != 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return width, height
            handle.seek(length - 2, 1)


def read_image_size(path: Path) -> tuple[int, int]:
    if not path.exists():
        raise FileNotFoundError(path)
    size = read_png_size(path) or read_jpeg_size(path)
    if size is None:
        raise ValueError(f"Unsupported image type or unreadable image header: {path}")
    return size


def collect_url_references(text: str, parser: PrototypeParser) -> list[str]:
    refs = list(parser.image_sources)
    refs.extend(re.findall(r"url\(([^)]+)\)", text))
    refs.extend(re.findall(r"src=[\"']([^\"']+)[\"']", text))
    return [ref.strip("\"' ") for ref in refs]


def sorted_names(items: Iterable[tuple[str, Path]]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name, path in items:
        if name in result:
            raise ValueError(f"Duplicate image name: {name}")
        result[name] = path
    return result


def audit(args: argparse.Namespace) -> tuple[list[str], dict[str, object]]:
    issues: list[str] = []
    html_path = Path(args.html)
    if not html_path.exists():
        return [f"HTML file does not exist: {html_path}"], {}

    text = html_path.read_text(encoding="utf-8")
    parser = PrototypeParser()
    parser.feed(text)

    if len(parser.components) < args.min_components:
        issues.append(
            f"Expected at least {args.min_components} data-component entries, found {len(parser.components)}"
        )

    bad_components = [name for name in parser.components if not PASCAL_CASE.match(name)]
    if bad_components:
        sample = ", ".join(bad_components[:8])
        issues.append(f"data-component values should be PascalCase. Bad values: {sample}")

    if args.require_screen_count is not None and len(set(parser.screens)) != args.require_screen_count:
        issues.append(
            f"Expected {args.require_screen_count} unique data-screen values, found {len(set(parser.screens))}"
        )

    missing_targets = sorted(set(parser.screens) - set(parser.screen_targets))
    if missing_targets:
        issues.append(f"data-screen values without matching data-screen-target: {', '.join(missing_targets)}")

    orphan_targets = sorted(set(parser.screen_targets) - set(parser.screens))
    if orphan_targets:
        issues.append(f"data-screen-target values without matching data-screen: {', '.join(orphan_targets)}")

    sources = sorted_names(args.source or [])
    screenshots = sorted_names(args.screenshot or [])
    references = collect_url_references(text, parser)
    data_images = re.findall(r"data:image/[a-zA-Z0-9.+-]+;base64,", text)
    if data_images and not args.allow_data_images:
        issues.append(
            f"Found {len(data_images)} embedded data:image bitmap(s). "
            "Use --allow-data-images only when these are intentional non-source assets."
        )
    if not args.allow_source_embeds:
        for name, path in sources.items():
            basename = path.name
            if basename in text or any(basename in ref for ref in references):
                issues.append(f"Source screenshot appears embedded or referenced in HTML: {basename}")

    image_report: dict[str, object] = {}
    for name, source_path in sources.items():
        if name not in screenshots:
            issues.append(f"Missing implementation screenshot for source {name!r}")
            continue
        source_size = read_image_size(source_path)
        screenshot_size = read_image_size(screenshots[name])
        source_aspect = source_size[0] / source_size[1]
        screenshot_aspect = screenshot_size[0] / screenshot_size[1]
        aspect_delta = abs(source_aspect - screenshot_aspect)
        image_report[name] = {
            "source": str(source_path),
            "source_size": source_size,
            "screenshot": str(screenshots[name]),
            "screenshot_size": screenshot_size,
            "source_aspect": round(source_aspect, 6),
            "screenshot_aspect": round(screenshot_aspect, 6),
            "aspect_delta": round(aspect_delta, 6),
        }
        if aspect_delta > args.max_aspect_delta:
            issues.append(
                f"Aspect ratio delta for {name!r} is {aspect_delta:.4f}, "
                f"above --max-aspect-delta {args.max_aspect_delta:.4f}"
            )

    report = {
        "html": str(html_path),
        "component_count": len(parser.components),
        "unique_component_count": len(set(parser.components)),
        "screens": sorted(set(parser.screens)),
        "screen_targets": sorted(set(parser.screen_targets)),
        "data_image_count": len(data_images),
        "image_report": image_report,
    }
    return issues, report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", required=True, help="Path to the generated HTML prototype.")
    parser.add_argument(
        "--source",
        action="append",
        type=parse_name_path,
        help="Source screenshot as name=path. Repeat for multiple screens.",
    )
    parser.add_argument(
        "--screenshot",
        action="append",
        type=parse_name_path,
        help="Rendered implementation screenshot as name=path. Repeat for multiple screens.",
    )
    parser.add_argument("--min-components", type=int, default=1)
    parser.add_argument("--require-screen-count", type=int)
    parser.add_argument("--max-aspect-delta", type=float, default=0.02)
    parser.add_argument("--allow-source-embeds", action="store_true")
    parser.add_argument("--allow-data-images", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        issues, report = audit(args)
    except Exception as exc:  # noqa: BLE001 - command-line audit should report concise failures.
        raise SystemExit(f"Audit failed: {exc}") from exc

    if args.json:
        print(json.dumps({"ok": not issues, "issues": issues, "report": report}, indent=2))
    elif issues:
        print("HTML prototype audit failed:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("HTML prototype audit passed")

    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
