#!/usr/bin/env python3
"""Validate the Image2Code skill repository."""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "image2code"


def run(command: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required path: {path.relative_to(ROOT)}")


def validate_metadata() -> None:
    skill_md = SKILL / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit("SKILL.md must start with YAML frontmatter")
    frontmatter = text.split("---", 2)[1]
    required = {"name: image2code", "description:"}
    missing = [item for item in required if item not in frontmatter]
    if missing:
        raise SystemExit(f"SKILL.md frontmatter missing: {', '.join(missing)}")
    if "$image2code" not in (ROOT / "README.md").read_text(encoding="utf-8"):
        raise SystemExit("README.md should include a quick $image2code usage prompt")


def validate_pack_scripts() -> None:
    tmp_root = ROOT / ".image2code-validate-tmp"
    shutil.rmtree(tmp_root, ignore_errors=True)
    try:
        pack = tmp_root / "docs/image2code/validate-pack"
        run(
            [
                sys.executable,
                str(SKILL / "scripts/init_design_pack.py"),
                "--project",
                "Validate App",
                "--platform",
                "ios",
                "--viewport",
                "ipad-11-landscape",
                "--repo",
                str(ROOT),
                "--relative-paths",
                "--output",
                str(pack),
            ]
        )
        require(pack / "implementation-screenshots")
        require(pack / "design-model.yaml")
        manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
        if manifest["design_model"] != "design-model.yaml":
            raise SystemExit("manifest should reference design-model.yaml")
        if manifest["source_context"]["repo"] != ".":
            raise SystemExit("--relative-paths should write repo label as '.'")
        if manifest["implementation"]["target_repo"] != ".":
            raise SystemExit("--relative-paths should write implementation target as '.'")
        if manifest["viewport_targets"] != ["ipad-11-landscape"]:
            raise SystemExit("viewport target was not preserved in manifest")
        run(
            [
                sys.executable,
                str(SKILL / "scripts/sync_manifest.py"),
                "--pack",
                str(pack),
                "--status",
                "ready",
            ]
        )
        run(
            [
                sys.executable,
                str(SKILL / "scripts/audit_design_pack.py"),
                "--pack",
                str(pack),
                "--strict-relative",
            ]
        )
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


def png_chunk(kind: bytes, data: bytes) -> bytes:
    checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)


def write_png(path: Path, width: int, height: int) -> None:
    raw = b"".join(b"\x00" + (b"\xff\xff\xff" * width) for _ in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + png_chunk(b"IDAT", zlib.compress(raw))
        + png_chunk(b"IEND", b"")
    )


def validate_html_prototype_script() -> None:
    tmp_root = ROOT / ".image2code-validate-tmp"
    html_dir = tmp_root / "html-audit"
    shutil.rmtree(html_dir, ignore_errors=True)
    try:
        html_dir.mkdir(parents=True, exist_ok=True)
        source = html_dir / "source.png"
        screenshot = html_dir / "screenshot.png"
        html = html_dir / "index.html"
        write_png(source, 100, 80)
        write_png(screenshot, 200, 160)
        html.write_text(
            """<!doctype html>
<html>
<body>
  <main data-component="PrototypeShell">
    <section data-component="DashboardScreen" data-screen="dashboard">
      <button data-component="PrimaryButton" data-screen-target="dashboard">Dashboard</button>
    </section>
  </main>
</body>
</html>
""",
            encoding="utf-8",
        )
        run(
            [
                sys.executable,
                str(SKILL / "scripts/audit_html_prototype.py"),
                "--html",
                str(html),
                "--min-components",
                "3",
                "--require-screen-count",
                "1",
                "--source",
                f"dashboard={source}",
                "--screenshot",
                f"dashboard={screenshot}",
            ]
        )
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


def main() -> None:
    require(SKILL / "SKILL.md")
    require(SKILL / "agents/openai.yaml")
    require(SKILL / "scripts/init_design_pack.py")
    require(SKILL / "scripts/sync_manifest.py")
    require(SKILL / "scripts/audit_design_pack.py")
    require(SKILL / "scripts/audit_html_prototype.py")
    require(SKILL / "scripts/collect_frontend_context.py")
    require(SKILL / "references/visual-quality-preflight.md")
    require(SKILL / "references/image-to-html-prototype.md")
    validate_metadata()
    run([sys.executable, "-m", "py_compile", *map(str, sorted((SKILL / "scripts").glob("*.py")))])
    validate_pack_scripts()
    validate_html_prototype_script()
    print("Image2Code skill validation passed")


if __name__ == "__main__":
    main()
