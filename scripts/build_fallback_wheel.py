#!/usr/bin/env python3
"""Build the universal pure-Python wheel from canonical project metadata."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def record_hash(payload: bytes) -> str:
    encoded = base64.urlsafe_b64encode(hashlib.sha256(payload).digest())
    return "sha256=" + encoded.rstrip(b"=").decode("ascii")


def normalize_metadata(wheel: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        infos = archive.infolist()
        payloads = {info.filename: archive.read(info.filename) for info in infos}
    metadata_name = next(name for name in payloads if name.endswith(".dist-info/METADATA"))
    record_name = next(name for name in payloads if name.endswith(".dist-info/RECORD"))
    lines = payloads[metadata_name].decode("utf-8").splitlines(keepends=True)
    dynamic = [line.strip() for line in lines if line.startswith("Dynamic:")]
    if dynamic not in ([], ["Dynamic: license-file"]):
        raise SystemExit(f"unexpected setuptools Dynamic fields: {dynamic!r}")
    payloads[metadata_name] = "".join(
        line for line in lines if not line.startswith("Dynamic:")
    ).encode("utf-8")
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    for info in infos:
        name = info.filename
        if name == record_name:
            continue
        payload = payloads[name]
        writer.writerow((name, record_hash(payload), str(len(payload))))
    writer.writerow((record_name, "", ""))
    payloads[record_name] = output.getvalue().encode("utf-8")
    normalized = wheel.with_suffix(".normalized.whl")
    with zipfile.ZipFile(normalized, "w") as archive:
        for info in infos:
            archive.writestr(info, payloads[info.filename])
    normalized.replace(wheel)


def fallback_pyproject() -> str:
    source = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project = source[source.index("[project]\n") : source.index("[tool.maturin]\n")].rstrip()
    return "\n".join(
        (
            "[build-system]",
            'requires = ["setuptools>=77", "wheel"]',
            'build-backend = "setuptools.build_meta"',
            "",
            project,
            "",
            "[tool.setuptools]",
            'packages = ["semver"]',
            "",
            "[tool.setuptools.package-data]",
            'semver = ["py.typed"]',
            "",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.out_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fast-semver-fallback-") as tmp:
        staging = Path(tmp)
        (staging / "pyproject.toml").write_text(fallback_pyproject(), encoding="utf-8")
        for relative in ("README.md", "LICENSE"):
            shutil.copy2(ROOT / relative, staging / relative)
        shutil.copytree(
            ROOT / "python" / "semver",
            staging / "semver",
            ignore=shutil.ignore_patterns("_native.*", "__pycache__", "*.pyc"),
        )
        subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(output)],
            cwd=staging,
            check=True,
        )
    wheels = sorted(output.glob("*-py3-none-any.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected one fallback wheel, found {wheels}")
    normalize_metadata(wheels[0])
    print(wheels[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
