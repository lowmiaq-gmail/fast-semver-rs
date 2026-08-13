# Project Goal

Provide an opt-in Rust-backed replacement for frozen `semver==3.0.4`, accelerating only the strict parse control point while preserving the complete Python object, CLI, warning and exception contract.

## Current Scope

- Preserve the `semver` namespace, `Version`/`VersionInfo`, helpers, CLI, signatures and exact errors.
- Reuse Rust `semver` only for strict parsing; retain Python for subclasses, bytes, optional parts, arbitrary integers and dynamic behavior.
- Ship native abi3 wheels, a universal Python 3.7 fallback, sdist and exact-artifact evidence through the existing Python→Rust production pipeline.
- Validate Google OSV as a real consumer and document the distribution-name/resolver boundary and rollback.

## Non-goals

- No new semantic-version standard, resolver, package manager, service or parallel Orchestrator.
- No compatibility claim outside frozen `semver==3.0.4`.
- No claim that `fast-semver-rs` satisfies another package's `semver` distribution dependency.

## Success Criteria

`UPSTREAM-CONTRACT.md` defines behavior; `COMPATIBILITY.md` records Build evidence; `../../python-rust-rewrite-pipeline/PIPELINE-STATE.json` alone decides `READY_TO_RELEASE` and `DONE`.

## Ownership

The user owns remote repository, merge and release authority. This 0.1.0 Release Lane is explicitly authorized; future releases require new authorization.

## Source of Truth

- requirements: `UPSTREAM-CONTRACT.md`
- architecture/routing: `PROJECT-MAP.md`
- verification: `COMPATIBILITY.md` plus executable tests/scripts
- current batch status: `../../python-rust-rewrite-pipeline/PIPELINE-STATE.json`
