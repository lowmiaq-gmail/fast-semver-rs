# Changelog

## 0.1.1

- Make the PyPI long description release-state invariant instead of retaining
  the 0.1.0 pre-release status sentence.
- Add cross-platform Core Metadata, frozen-consumer Oracle, portable temporary
  directory and actual unsupported-platform fallback regressions.

## 0.1.0

- Add a behavior-compatible `semver==3.0.4` Python surface.
- Accelerate strict parsing with Rust while preserving Python fallbacks.
- Ship five native abi3 wheels, a universal fallback wheel and an sdist.
- Add full upstream, 10,000-case differential, Google OSV consumer, artifact and public-install gates.
- Build the universal wheel once on a modern packaging toolchain and install that immutable artifact on Python 3.7.
