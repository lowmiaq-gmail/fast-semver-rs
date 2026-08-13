# fast-semver-rs 0.1.0

Initial opt-in Rust-backed API replacement for `semver==3.0.4`.

- The frozen `semver` namespace, `Version` object model, deprecated helpers, warnings and `pysemver` CLI remain Python-compatible.
- Strict parse is accelerated through a Rust `semver` backend; unsupported dynamic cases fail closed to the frozen Python path.
- Native abi3 wheels cover Linux x86_64/aarch64, macOS arm64/x86_64 and Windows x86_64; a universal fallback preserves Python 3.7 and unsupported platforms.
- Exact release artifacts are audited, benchmarked, published through PyPI Trusted Publishing, reinstalled from public PyPI and attached to this formal release last.

The replacement is distribution-name opt-in: do not install `semver` and `fast-semver-rs` together. See the README for install and rollback commands.
