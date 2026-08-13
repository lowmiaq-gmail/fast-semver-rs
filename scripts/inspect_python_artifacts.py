#!/usr/bin/env python3
"""Fail-closed audit of the immutable native/fallback/sdist release set."""

from __future__ import annotations

import argparse
import base64
import csv
import email.parser
import hashlib
import io
from pathlib import Path, PurePosixPath
import tarfile
import zipfile

from packaging.specifiers import SpecifierSet


NAME = "fast-semver-rs"
VERSION = "0.1.0"
PYTHON = ">=3.7"
SUMMARY = "Opt-in Rust-backed API replacement for semver 3.0.4"
AUTHOR = "fast-semver-rs contributors"
LICENSE = "BSD-3-Clause"


def safe(names: list[str]) -> None:
    for name in names:
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts, name


def metadata(raw: bytes) -> tuple[object, ...]:
    value = email.parser.BytesParser().parsebytes(raw)
    assert value["Metadata-Version"] == "2.4"
    assert value["Name"] == NAME
    assert value["Version"] == VERSION
    assert value["Summary"] == SUMMARY
    assert value["Author"] == AUTHOR
    assert value["License-Expression"] == LICENSE
    assert set(value.get_all("License-File", [])) == {"LICENSE"}
    assert not value.get_all("Dynamic", [])
    assert not value.get_all("Requires-Dist", [])
    assert SpecifierSet(value["Requires-Python"]) == SpecifierSet(PYTHON)
    urls = set(value.get_all("Project-URL", []))
    assert len(urls) == 4 and any(item.startswith("Homepage,") for item in urls)
    return (
        value["Name"], value["Version"], value["Summary"], value["Author"],
        value["License-Expression"], str(SpecifierSet(value["Requires-Python"])),
        frozenset(value.get_all("Classifier", [])), frozenset(urls),
        value.get_payload().rstrip("\n"),
    )


def verify_record(archive: zipfile.ZipFile, names: list[str]) -> None:
    record_name = next(name for name in names if name.endswith(".dist-info/RECORD"))
    rows = list(csv.reader(io.StringIO(archive.read(record_name).decode("utf-8"))))
    rows = [(path.replace("\\", "/"), digest, size) for path, digest, size in rows]
    assert {row[0] for row in rows} == set(names)
    assert len(rows) == len({row[0] for row in rows})
    for path, encoded_hash, encoded_size in rows:
        if path == record_name:
            assert encoded_hash == encoded_size == ""
            continue
        algorithm, expected = encoded_hash.split("=", 1)
        payload = archive.read(path)
        actual = base64.urlsafe_b64encode(hashlib.new(algorithm, payload).digest()).rstrip(b"=").decode()
        assert actual == expected and len(payload) == int(encoded_size), path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--expected-native-wheels", type=int, required=True)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    wheels = sorted(args.artifact_dir.glob("*.whl"))
    sdists = sorted(args.artifact_dir.glob("*.tar.gz"))
    fallback = [wheel for wheel in wheels if wheel.name.endswith("-py3-none-any.whl")]
    native = [wheel for wheel in wheels if wheel not in fallback]
    assert len(native) == args.expected_native_wheels, native
    assert len(fallback) == 1, fallback
    assert len(sdists) == 1, sdists
    canonical = set()
    forbidden = (str(root), "/home/runner/work/", "\\Users\\", "target/release", "target/debug")
    for wheel in wheels:
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            safe(names)
            assert not any(
                name.endswith((".pyc", ".pyo")) or "/__pycache__/" in "/" + name
                or "/tests/" in "/" + name or "/target/" in "/" + name
                for name in names
            ), names
            metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
            canonical.add(metadata(archive.read(metadata_name)))
            verify_record(archive, names)
            assert "semver/__init__.py" in names and "semver/version.py" in names and "semver/py.typed" in names
            entry = next(name for name in names if name.endswith(".dist-info/entry_points.txt"))
            entry_text = archive.read(entry).decode("utf-8").replace(" ", "")
            assert "pysemver=semver.cli:main" in entry_text
            has_native = any(name.startswith("semver/_native") and name.endswith((".so", ".pyd")) for name in names)
            wheel_text = archive.read(next(name for name in names if name.endswith(".dist-info/WHEEL"))).decode()
            if wheel in fallback:
                assert not has_native and "Root-Is-Purelib: true" in wheel_text and "Tag: py3-none-any" in wheel_text
            else:
                assert has_native and "Root-Is-Purelib: false" in wheel_text and "-abi3-" in wheel.name
            for name in names:
                if name.endswith((".py", ".md", ".txt", ".toml", ".json")):
                    text = archive.read(name).decode("utf-8", errors="ignore")
                    assert not any(item in text for item in forbidden), name
    with tarfile.open(sdists[0], "r:gz") as archive:
        names = archive.getnames()
        safe(names)
        assert not any(
            "/target/" in "/" + name or "/.venv/" in "/" + name
            or "/__pycache__/" in "/" + name or "/.pytest_cache/" in "/" + name
            or name.endswith("consumer-benchmark.json")
            or name.endswith((".so", ".pyd", ".dll", ".dylib", ".pyc", ".pyo"))
            for name in names
        ), names
        for suffix in (
            "/Cargo.toml", "/pyproject.toml", "/src/lib.rs", "/python/semver/version.py",
            "/upstream/tests/test_parsing.py", "/consumer/osv/semver_index_test.py",
        ):
            assert any(name.endswith(suffix) for name in names), suffix
        member = next(item for item in archive.getmembers() if item.name.endswith("/PKG-INFO"))
        handle = archive.extractfile(member)
        assert handle is not None
        canonical.add(metadata(handle.read()))
    assert len(canonical) == 1, "metadata differs across artifacts"
    print(f"artifact audit: PASS native={len(native)} fallback=1 sdist=1")


if __name__ == "__main__":
    main()
