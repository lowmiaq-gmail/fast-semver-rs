# Compatibility Evidence

Current verdict: `READY_TO_RELEASE` locally; public release is not yet complete.

Current evidence:

- exact native and fallback Candidate suites: `337 passed` each;
- deterministic valid/invalid/bytes/optional/large-integer differential: `10,000` cases, zero mismatch;
- Google OSV frozen `semver_index` suite: Oracle and Candidate `3 passed`;
- OSV normalize/sort output digests equal;
- exact native wheel parse/compare/match output digests equal with local median speedups `1.72x / 1.32x / 1.40x`;
- exact native wheel OSV normalize/sort output digests equal with local median speedups `1.21x / 1.15x`;
- native/fallback/sdist metadata and sanitation audit plus Twine checks pass.

Release CI must reproduce this across five native platforms, Python 3.7 fallback,
public PyPI reinstalls and Release-last. Local evidence is not public release evidence.
