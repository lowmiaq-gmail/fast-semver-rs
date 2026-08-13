# Read Order

Read `PROJECT.md`, `PROGRESS.md`, `PROJECT-MAP.md`, this file, `UPSTREAM-CONTRACT.md`, `REUSE-AUDIT.md`, `COMPATIBILITY.md`, then actual source/tests.

## Source of Truth

The shared production SSOT is `../../python-rust-rewrite-pipeline/PIPELINE-STATE.json`; do not create another scheduler or completion state. Actual code, packaged artifacts and fresh tests outrank documents.

## Change Rules

Inspect impacted source before edits. Preserve `upstream/` as the frozen oracle and `consumer/` as the licensed Google OSV fixture. Never alter or skip tests to make Candidate pass. Benchmark only after semantic equality; unsupported Rust cases must fall back to Python. Keep Build and Release lanes independent.

## Verification

Run Rust fmt, strict Clippy and Cargo tests; candidate plus complete upstream tests; 10,000-case isolated differential; Google OSV validation; native/fallback/sdist artifact inspection; clean installs and exact-artifact benchmarks. A local pass is not CI/PyPI/GitHub Release evidence.

## Environment, Toolchain and Invocation

The working directory is this project root. `pyproject.toml`, `Cargo.toml`, `Cargo.lock`, workflows and `README.md` own version/toolchain/invocation facts. Use project-local environments. Secret and credential values stay outside the repository and must never be printed or persisted.

## Handoff

Remote creation and this 0.1.0 release are user-authorized. Future pushes/releases require explicit scope. Check diff/status before handoff and preserve unrelated work.
