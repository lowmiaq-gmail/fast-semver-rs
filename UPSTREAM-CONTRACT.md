# Upstream Contract

## Frozen source

- package: `semver`
- version/tag: `3.0.4`
- repository: `https://github.com/python-semver/python-semver`
- peeled commit: `6adf8765f6e21910f1f0c13151ce84f32f8d431d`
- PyPI sdist SHA256: `afc7d8c584a5ed0a11033af086e8af226a9c0b206f313e0301f8dd7b6b589602`
- upstream Python support: `>=3.7`
- license: BSD-3-Clause, retained in `LICENSE` and `upstream/LICENSE.txt`
- test fixture portability: the two upstream test symlinks are materialized as ordinary files with equivalent code so Windows runners execute them.

## Required public contract

- import/module paths, `Version` and alias `VersionInfo`, metadata constants and `py.typed`;
- immutable/subclassable Python class, constructor/properties, tuple/dict/iteration/index/repr/str/hash;
- parse/is_valid, optional minor/patch, bytes, arbitrary-size integers and exact TypeError/ValueError behavior;
- comparisons against strings/bytes/dicts/tuples/lists/subclasses, prerelease precedence and ignored build metadata;
- bump/replace/finalize/match/is_compatible and all deprecated top-level wrappers/warnings;
- `semver.cli`, `python -m semver`, and `pysemver` command behavior.

## Architecture boundary

Rust may parse only strict valid SemVer into parts. Python constructs `cls`,
retains dynamic behavior, and falls back when Rust's `u64` representation cannot
express Python's arbitrary-size integers or when exact public errors are needed.
The mature Rust `semver` crate is reused as a core, not asserted to be a Python
drop-in.
