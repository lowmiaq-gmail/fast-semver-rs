#!/usr/bin/env python3
"""Fail fast when backend release versions or the Cargo lockfile drift."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


BACKEND_PACKAGE = "fast-semver-rs-backend"


class ContractError(RuntimeError):
    """The backend release inputs are inconsistent."""


@dataclass(frozen=True)
class BackendVersions:
    pyproject: str
    cargo_toml: str
    cargo_lock: str


def _read_toml(path: Path) -> dict:
    with path.open("rb") as source:
        return tomllib.load(source)


def read_backend_versions(repository_root: Path) -> BackendVersions:
    backend = repository_root / "backend"
    pyproject_version = _read_toml(backend / "pyproject.toml")["project"]["version"]
    cargo_toml_version = _read_toml(backend / "Cargo.toml")["package"]["version"]

    lock_packages = _read_toml(backend / "Cargo.lock").get("package", [])
    backend_packages = [
        package for package in lock_packages if package.get("name") == BACKEND_PACKAGE
    ]
    if len(backend_packages) != 1:
        raise ContractError(
            "backend/Cargo.lock must contain exactly one [[package]] entry named "
            f'"{BACKEND_PACKAGE}"; found {len(backend_packages)}.'
        )

    return BackendVersions(
        pyproject=str(pyproject_version),
        cargo_toml=str(cargo_toml_version),
        cargo_lock=str(backend_packages[0]["version"]),
    )


def validate_versions(
    versions: BackendVersions, requested_version: str | None = None
) -> None:
    sources = {
        "backend/pyproject.toml": versions.pyproject,
        "backend/Cargo.toml": versions.cargo_toml,
        "backend/Cargo.lock": versions.cargo_lock,
    }
    if requested_version is not None:
        sources["requested version"] = requested_version

    if len(set(sources.values())) == 1:
        return

    details = "\n".join(f"  {name:<24} {version}" for name, version in sources.items())
    raise ContractError(
        "backend release version contract violated\n"
        f"{details}\n\n"
        "Do not release. Update both backend manifests, refresh backend/Cargo.lock "
        "through Cargo, and commit all three files.\n"
        "Use: python scripts/bump_backend_version.py <new-version>"
    )


def run_locked_metadata(repository_root: Path) -> int:
    command = [
        "cargo",
        "metadata",
        "--locked",
        "--manifest-path",
        "backend/Cargo.toml",
        "--format-version",
        "1",
    ]
    result = subprocess.run(
        command,
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        print(
            "ERROR: cargo metadata --locked failed; backend/Cargo.lock must be "
            "refreshed through Cargo and committed before release.",
            file=sys.stderr,
        )
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--requested-version",
        help="also require the workflow_dispatch version to match all backend files",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    try:
        versions = read_backend_versions(repository_root)
        validate_versions(versions, args.requested_version)
    except (ContractError, KeyError, OSError, tomllib.TOMLDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    metadata_status = run_locked_metadata(repository_root)
    if metadata_status != 0:
        return metadata_status

    print(
        "[OK] Backend release contract: "
        f"pyproject.toml = Cargo.toml = Cargo.lock = {versions.pyproject}; "
        "cargo metadata --locked succeeded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
