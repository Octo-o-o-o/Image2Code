#!/usr/bin/env python3
"""Synchronize image and screenshot file lists into an Image2Code manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


IMAGE_EXTENSIONS = {".gif", ".jpg", ".jpeg", ".png", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, help="Design pack directory")
    parser.add_argument("--status", help="Optional manifest status to set")
    parser.add_argument(
        "--default-viewport",
        default="desktop-1440x900",
        help="Viewport value to use for newly discovered final images",
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


def screen_name(path: Path) -> str:
    stem = path.stem
    parts = [part for part in stem.replace("_", "-").split("-") if part]
    if parts and parts[0].isdigit():
        parts = parts[1:]
    return " ".join(part.capitalize() for part in parts) or stem


def main() -> None:
    args = parse_args()
    pack = Path(args.pack).expanduser().resolve()
    manifest_path = pack / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest.json not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    existing_final = {
        item.get("path"): item for item in manifest.get("final_images", []) if item.get("path")
    }
    final_images = []
    for path in image_files(pack, "images"):
        relative = rel(path, pack)
        item = existing_final.get(relative) or {
            "path": relative,
            "screen": screen_name(path),
            "viewport": args.default_viewport,
            "purpose": "Generated final design image",
            "source_prompt": "04-image-prompts.md",
        }
        final_images.append(item)
    manifest["final_images"] = final_images

    source_context = manifest.setdefault("source_context", {})
    source_context["input_images"] = [
        rel(path, pack) for path in image_files(pack, "input")
    ]
    source_context["user_screenshots"] = [
        rel(path, pack) for path in image_files(pack, "input/user")
    ]
    source_context["current_screenshots"] = [
        rel(path, pack) for path in image_files(pack, "input/current-screenshots")
    ]
    source_context["browser_screenshots"] = [
        rel(path, pack) for path in image_files(pack, "browser-screenshots")
    ]
    source_context["implementation_screenshots"] = [
        rel(path, pack) for path in image_files(pack, "implementation-screenshots")
    ]
    source_context.setdefault("repo", "")

    manifest["updated_at"] = datetime.now().isoformat(timespec="seconds")
    if args.status:
        manifest["status"] = args.status

    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(manifest_path)


if __name__ == "__main__":
    main()
