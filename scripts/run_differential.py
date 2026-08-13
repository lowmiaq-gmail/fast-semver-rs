from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SEED = 20260813


def cases(count: int) -> list[dict[str, object]]:
    rng = random.Random(SEED)
    values: list[dict[str, object]] = [
        {"value": "1.2.3-alpha.1+build.9"},
        {"value": "999999999999999999999999999999.2.3"},
        {"value": "7", "optional_minor_and_patch": True},
        {"value": "1.2.3", "bytes": True},
        {"value": "01.2.3"},
        {"value": "1.2"},
        {"value": ""},
    ]
    invalid_templates = (
        "0{major}.{minor}.{patch}",
        "{major}.0{minor}.{patch}",
        "{major}.{minor}.0{patch}",
        "{major}.{minor}",
        "v{major}.{minor}.{patch}",
        "{major}.{minor}.{patch}-01",
        "{major}.{minor}.{patch}+",
    )
    while len(values) < count:
        major, minor, patch = (rng.randrange(1, 1_000_000) for _ in range(3))
        if len(values) % 5 == 0:
            template = rng.choice(invalid_templates)
            values.append({"value": template.format(major=major, minor=minor, patch=patch)})
            continue
        prerelease = "" if len(values) % 3 else "-" + rng.choice(("alpha", "rc.1", "0", "beta.2"))
        build = "" if len(values) % 7 else "+" + rng.choice(("build.1", "sha-abc", "9"))
        values.append({"value": f"{major}.{minor}.{patch}{prerelease}{build}"})
    return values[:count]


def run(python: Path, corpus: Path, output: Path, oracle: bool) -> None:
    command = [
        str(python.absolute()),
        str(ROOT / "scripts/probe_contract.py"),
        "--corpus",
        str(corpus),
        "--output",
        str(output),
    ]
    if oracle:
        command.extend(["--oracle-root", str(ROOT / "upstream/src")])
    subprocess.run(command, cwd=tempfile.gettempdir(), check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oracle-python", type=Path, required=True)
    parser.add_argument("--candidate-python", type=Path, required=True)
    parser.add_argument("--cases", type=int, default=10_000)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="fast-semver-diff-") as directory:
        root = Path(directory)
        corpus = root / "corpus.jsonl"
        expected = root / "oracle.jsonl"
        actual = root / "candidate.jsonl"
        generated = cases(args.cases)
        corpus.write_text(
            "\n".join(json.dumps(item, sort_keys=True) for item in generated) + "\n",
            encoding="utf-8",
        )
        run(args.oracle_python, corpus, expected, True)
        run(args.candidate_python, corpus, actual, False)
        expected_lines = expected.read_text(encoding="utf-8").splitlines()
        actual_lines = actual.read_text(encoding="utf-8").splitlines()
        if expected_lines != actual_lines:
            for index, (left, right) in enumerate(zip(expected_lines, actual_lines)):
                if left != right:
                    raise AssertionError(
                        f"differential mismatch at {index}:\noracle={left}\ncandidate={right}"
                    )
            raise AssertionError("differential cardinality mismatch")
        print(f"differential: PASS seed={SEED} cases={len(generated)}")


if __name__ == "__main__":
    main()
