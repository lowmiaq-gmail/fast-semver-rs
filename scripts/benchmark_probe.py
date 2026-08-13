from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import time


def values() -> list[str]:
    rng = random.Random(20260813)
    result = []
    for index in range(20_000):
        prerelease = "" if index % 3 else "-" + rng.choice(("alpha", "rc.1", "0", "beta.2"))
        build = "" if index % 5 else "+" + rng.choice(("build.1", "sha-abc", "9"))
        result.append(f"{rng.randrange(100_000)}.{rng.randrange(100_000)}.{rng.randrange(100_000)}{prerelease}{build}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oracle-root", type=Path)
    parser.add_argument("--workload", choices=("parse", "compare", "match"), required=True)
    args = parser.parse_args()
    if args.oracle_root:
        sys.path.insert(0, str(args.oracle_root.resolve()))
    import semver

    corpus = values()
    started = time.perf_counter_ns()
    if args.workload == "parse":
        output = [str(semver.Version.parse(item)) for item in corpus]
    elif args.workload == "compare":
        output = [str(semver.compare(item, "50000.50000.50000")) for item in corpus]
    else:
        output = [str(semver.match(item, ">=50000.0.0")) for item in corpus]
    elapsed = time.perf_counter_ns() - started
    print(json.dumps({
        "elapsed_ns": elapsed,
        "calls": len(corpus),
        "digest": hashlib.sha256("\n".join(output).encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
