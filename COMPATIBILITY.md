# Compatibility Evidence

Current verdict: `DONE`; public release `0.1.1` completed.

Current evidence:

- exact native and fallback Candidate suites: `337 passed` each;
- deterministic valid/invalid/bytes/optional/large-integer differential: `10,000` cases, zero mismatch;
- Google OSV frozen `semver_index` suite: Oracle and Candidate `3 passed`;
- OSV normalize/sort output digests equal;
- exact native wheel parse/compare/match output digests equal with local median speedups `1.72x / 1.32x / 1.40x`;
- exact native wheel OSV normalize/sort output digests equal with local median speedups `1.21x / 1.15x`;
- native/fallback/sdist metadata and sanitation audit plus Twine checks pass;
- five public native reinstall lanes pass;
- the public universal fallback selected for an unsupported native platform passes `337` tests and the 10,000-case differential;
- PyPI and GitHub Release distribution SHA256 sets are identical.
- the rendered PyPI page uses release-state-invariant wording and passed semantic read-back.

Release run: `31671636525`. GitHub Release target: `d11032c9c572480556275e5189a97bd8a6dad982`.
