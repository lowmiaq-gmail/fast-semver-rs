#!/usr/bin/env python3
"""Update both backend manifests and let Cargo refresh the backend lockfile."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from check_backend_release_contract import read_backend_versions, validate_versions


SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def replace_section_version(path: Path, section: str, new_version: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    current_section: str | None = None
    replacements = 0
    version_line = re.compile(r'^(\s*version\s*=\s*)"[^"]+"(\s*(?:#.*)?\r?\n?)$')

    for index, line in enumerate(lines):
        section_match = re.match(r"^\s*\[([^]]+)]\s*(?:#.*)?$", line.rstrip("\r\n"))
        if section_match:
            current_section = section_match.group(1)
            continue
        if current_section != section:
            continue
        match = version_line.match(line)
        if match:
            lines[index] = f'{match.group(1)}"{new_version}"{match.group(2)}'
            replacements += 1

    if replacements != 1:
        raise RuntimeError(
            f"expected exactly one version in [{section}] of {path}; found {replacements}"
        )
    path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("new_version", help="new Cargo-compatible SemVer version")
    args = parser.parse_args()
    if not SEMVER_PATTERN.fullmatch(args.new_version):
        parser.error(f"invalid semantic version: {args.new_version!r}")

    repository_root = Path(__file__).resolve().parents[1]
    current_versions = read_backend_versions(repository_root)
    validate_versions(current_versions)
    if args.new_version == current_versions.pyproject:
        parser.error(f"backend version is already {args.new_version}")

    replace_section_version(
        repository_root / "backend/pyproject.toml", "project", args.new_version
    )
    replace_section_version(
        repository_root / "backend/Cargo.toml", "package", args.new_version
    )

    subprocess.run(
        [
            "cargo",
            "metadata",
            "--manifest-path",
            "backend/Cargo.toml",
            "--format-version",
            "1",
        ],
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/check_backend_release_contract.py"],
        cwd=repository_root,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "diff",
            "--",
            "backend/pyproject.toml",
            "backend/Cargo.toml",
            "backend/Cargo.lock",
        ],
        cwd=repository_root,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
