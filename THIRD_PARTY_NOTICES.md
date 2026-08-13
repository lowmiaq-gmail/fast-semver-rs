# Third-Party Notices

This project derives its compatibility layer and contract from `semver==3.0.4`
by its contributors under the BSD-3-Clause License. The frozen source, tests and
license are retained under `upstream/`.

The native extension uses the Rust `semver` and PyO3 crates. Their locked source
versions and license expressions are resolved by Cargo; both direct dependencies
are available under permissive MIT/Apache-2.0 terms. No separate Python runtime
dependency is bundled into release wheels.
