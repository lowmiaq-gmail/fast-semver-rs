#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON:-python3}"

"$python_bin" - <<'PY'
import os
import pathlib
import semver

expected = os.environ.get("CANDIDATE_EXPECTED_ROOT")
if expected:
    actual = pathlib.Path(semver.__file__).resolve()
    root = pathlib.Path(expected).resolve()
    if root not in actual.parents:
        raise SystemExit("candidate ownership mismatch: %s not under %s" % (actual, root))
assert semver.__version__ == "3.0.4"
PY

PYTHONDONTWRITEBYTECODE=1 "$python_bin" -m pytest -q upstream/tests
