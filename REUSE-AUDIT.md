# Reuse Audit

## Decision

`ADAPT`: reuse Rust `semver` for strict parsing, preserve the frozen Python
package for its public object/CLI/deprecation contract, and reuse existing
PyO3/Maturin/fallback/artifact/release production assets.

## Gap evidence

- PyPI returned 404 for `fast-semver-rs`, `semver-rs`, `semver_rs` and `pyo3-semver` during admission.
- The stale `rs_versions` project exposes a different namespace and narrow API;
  it does not provide `semver.Version`, CLI or compatibility wrappers.
- Rust `semver` is actively maintained and handles the strict parse core, but
  its Cargo-oriented `u64` model cannot express Python arbitrary-size fields or
  the dynamic public object model.
- A packaged PyO3 spike preserved 10,000 valid tuples, complete upstream tests
  and Google OSV consumer tests while showing measurable consumer speedup.

## Rejected work

- no new SemVer specification, resolver, package manager, service, database,
  dashboard or Orchestrator;
- no 100% Rust purity goal; Python behavior is retained where it is the contract;
- no release merely from microbenchmark success; exact artifacts, full tests,
  real consumer, adoption path and public release gates remain required.
