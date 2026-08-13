# fast-semver-rs 0.1.1

Metadata-corrective release of the opt-in Rust-backed API replacement for
`semver==3.0.4`.

- Keeps the 0.1.0 Python/Rust behavior and seven-artifact platform coverage.
- Makes the PyPI long description valid before and after release completion.
- Retains the strengthened cross-platform metadata, frozen Google OSV consumer,
  portable probe and unsupported-platform fallback gates discovered during the
  0.1.0 release.

The replacement is distribution-name opt-in: do not install `semver` and
`fast-semver-rs` together. See the README for install and rollback commands.
