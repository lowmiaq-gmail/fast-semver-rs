from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]


def corpus() -> list[str]:
    rng = random.Random(20260813)
    result = []
    for index in range(20_000):
        pre = "" if index % 3 else "-" + rng.choice(("alpha", "rc.1", "0", "beta.2"))
        build = "" if index % 5 else "+" + rng.choice(("build.1", "sha-abc", "9"))
        result.append(
            f"{rng.randrange(100_000)}.{rng.randrange(100_000)}.{rng.randrange(100_000)}{pre}{build}"
        )
    return result


def probe(workload: str) -> dict[str, object]:
    from consumer.osv import semver_index

    values = corpus()
    started = time.perf_counter_ns()
    if workload == "normalize":
        output = [semver_index.normalize(value) for value in values]
    elif workload == "sort":
        output = sorted(values, key=semver_index.normalize)
    else:
        output = values
    elapsed = time.perf_counter_ns() - started
    return {
        "elapsed_ns": elapsed,
        "digest": hashlib.sha256("\n".join(output).encode()).hexdigest(),
    }


def pythonpath(oracle: bool) -> str:
    roots = [ROOT / "upstream" / "src", ROOT] if oracle else [ROOT]
    return os.pathsep.join(str(root) for root in roots)


def invoke(python: Path, workload: str, oracle: bool) -> dict[str, object]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = pythonpath(oracle)
    output = subprocess.check_output(
        [str(python.absolute()), __file__, "--probe", workload],
        cwd=tempfile.gettempdir(),
        env=environment,
        text=True,
    )
    return json.loads(output)


def suite(python: Path, oracle: bool) -> str:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = pythonpath(oracle)
    completed = subprocess.run(
        [str(python.absolute()), "-m", "unittest", "-v", "consumer.osv.semver_index_test"],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    lines = (completed.stdout + "\n" + completed.stderr).splitlines()
    ran = next((line for line in lines if line.startswith("Ran ")), "")
    status = next((line for line in reversed(lines) if line in {"OK", "FAILED"}), "")
    if not ran or status != "OK":
        raise SystemExit("consumer suite did not produce a verified OK summary")
    return f"{ran}; {status}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", choices=("normalize", "sort", "control"))
    parser.add_argument("--oracle-python", type=Path)
    parser.add_argument("--candidate-python", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pairs", type=int, default=12)
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(probe(args.probe), sort_keys=True))
        return

    evidence: dict[str, object] = {
        "consumer": "google/osv.dev semver_index",
        "consumer_commit": "918f43604b8db3b6ab1237be6de3d84588402e5a",
        "oracle_suite": suite(args.oracle_python, True),
        "candidate_suite": suite(args.candidate_python, False),
        "artifact": args.artifact.name,
        "artifact_sha256": hashlib.sha256(args.artifact.read_bytes()).hexdigest(),
        "pairs": args.pairs,
        "workloads": {},
    }
    for workload in ("normalize", "sort", "control"):
        samples = {"oracle": [], "candidate": []}
        digests = {"oracle": set(), "candidate": set()}
        for index in range(args.pairs):
            order = ("oracle", "candidate") if index % 2 == 0 else ("candidate", "oracle")
            for implementation in order:
                python = args.oracle_python if implementation == "oracle" else args.candidate_python
                result = invoke(python, workload, implementation == "oracle")
                samples[implementation].append(result["elapsed_ns"])
                digests[implementation].add(result["digest"])
        if digests["oracle"] != digests["candidate"]:
            raise SystemExit(f"consumer output mismatch: {workload}")
        oracle_median = statistics.median(samples["oracle"])
        candidate_median = statistics.median(samples["candidate"])
        evidence["workloads"][workload] = {
            "oracle_raw_ns": samples["oracle"],
            "candidate_raw_ns": samples["candidate"],
            "median_speedup": oracle_median / candidate_median if candidate_median else 1.0,
            "output_digest": next(iter(digests["oracle"])),
        }
    args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print("consumer: PASS", evidence["oracle_suite"], evidence["candidate_suite"])
    for name, value in evidence["workloads"].items():
        print(name, f"{value['median_speedup']:.3f}x", "digest_equal=true")


if __name__ == "__main__":
    main()
