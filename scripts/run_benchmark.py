#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def invoke(workload: str, oracle: bool) -> dict[str, object]:
    command = [sys.executable, str(ROOT / "scripts/benchmark_probe.py"), "--workload", workload]
    if oracle:
        command.extend(("--oracle-root", str(ROOT / "upstream/src")))
    return json.loads(subprocess.check_output(command, cwd="/tmp", text=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=15)
    args = parser.parse_args()
    result: dict[str, object] = {
        "artifact": args.artifact.name,
        "artifact_sha256": hashlib.sha256(args.artifact.read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "repeats": args.repeats,
        "workloads": {},
    }
    for workload in ("parse", "compare", "match"):
        samples = {"oracle": [], "candidate": []}
        digests = {"oracle": set(), "candidate": set()}
        calls = None
        for index in range(args.repeats):
            order = (True, False) if index % 2 == 0 else (False, True)
            for oracle in order:
                value = invoke(workload, oracle)
                key = "oracle" if oracle else "candidate"
                samples[key].append(value["elapsed_ns"])
                digests[key].add(value["digest"])
                calls = value["calls"]
        assert digests["oracle"] == digests["candidate"], workload
        oracle_median = statistics.median(samples["oracle"])
        candidate_median = statistics.median(samples["candidate"])
        result["workloads"][workload] = {
            "calls": calls,
            "oracle_raw_ns": samples["oracle"],
            "candidate_raw_ns": samples["candidate"],
            "oracle_median_ns": oracle_median,
            "candidate_median_ns": candidate_median,
            "median_speedup": oracle_median / candidate_median,
            "output_digest": next(iter(digests["oracle"])),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for name, value in result["workloads"].items():
        print(name, f"{value['median_speedup']:.3f}x", "digest_equal=true")


if __name__ == "__main__":
    main()
