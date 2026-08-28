# Start Here

Read `PROGRESS.md`, `PROJECT.md`, this map and `AGENTS.md` before task-specific evidence and source.

## Repository Directory Map

- `PROJECT.md`: goal, scope, success and ownership.
- `PROGRESS.md`: current status and next action.
- `UPSTREAM-CONTRACT.md`: frozen upstream and compatibility surface.
- `REUSE-AUDIT.md`: ADAPT/REUSE decision and prohibited duplication.
- `COMPATIBILITY.md`: validated Build Lane evidence and remaining Release gates.
- `python/semver/`: public compatibility package; optional native import lives in `version.py`.
- `src/`: standalone Rust/PyO3 strict parser binding.
- `core/`: shared Rust parser core used by both distribution surfaces.
- `backend/`: backend-only PyO3 binding and package metadata; it must not provide `semver`.
- `tests/`: candidate-only contract regressions.
- `scripts/`: differential, benchmark, Google OSV, fallback and artifact validation.
- `consumer/`: frozen applicable Google OSV consumer files and license.
- `upstream/`: immutable oracle source/test snapshot.
- `.github/workflows/`: packaged-wheel CI and guarded Release Lane.
- `dist/` and `target/`: ignored generated output; release workflow owns immutable artifacts.

## Repository Intelligence

Use targeted source/test inspection for this small mixed Rust/Python library. Actual source, packaged artifacts and runtime tests outrank generated summaries.

## Document Map

The top entries route goal, status, requirements, audit and verification; do not create duplicate completion state.

## 修改路由 (Where to Change)

- public Python behavior: `python/semver/` plus candidate and complete upstream tests;
- native strict parsing: `core/` and `src/lib.rs` plus differential/benchmark scripts;
- fallback/packaging/CI: manifests, build/inspector scripts and `.github/workflows/`;
- current status/rules: `PROGRESS.md` / `AGENTS.md` and shared pipeline state.
