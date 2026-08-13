from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--oracle-root", type=Path)
    args = parser.parse_args()
    if args.oracle_root:
        sys.path.insert(0, str(args.oracle_root.resolve()))

    import semver

    records = []
    for line in args.corpus.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        value = case["value"]
        if case.get("bytes"):
            value = value.encode("utf-8")
        try:
            result = semver.Version.parse(
                value,
                optional_minor_and_patch=case.get("optional_minor_and_patch", False),
            )
            record = {
                "ok": True,
                "tuple": result.to_tuple(),
                "string": str(result),
                "repr": repr(result),
            }
        except Exception as error:  # exact public exception evidence
            record = {
                "ok": False,
                "exception": type(error).__name__,
                "message": str(error),
            }
        records.append(json.dumps(record, ensure_ascii=True, sort_keys=True))
    args.output.write_text("\n".join(records) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
