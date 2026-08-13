# fast-semver-rs

Opt-in Rust-backed, behavior-compatible API replacement for `semver==3.0.4`.
It keeps the `semver` import, `Version`/`VersionInfo` Python class, CLI and
deprecated compatibility surface while accelerating the strict parse hot path.

Rust does not replace Python's public object model. Bytes decoding, subclasses,
optional minor/patch parsing, arbitrary-size integers, exact errors, bumps,
matching, formatting, CLI and warnings remain in the frozen Python compatibility
layer. The native parser is used only when it can preserve that contract.

## Verified Build Lane evidence

- frozen upstream tag `3.0.4` at commit `6adf8765f6e21910f1f0c13151ce84f32f8d431d`;
- exact native and universal fallback wheel suites: `337 passed` each (`329` frozen upstream plus `8` candidate regressions);
- 10,000 deterministic valid, invalid, bytes, optional-part and arbitrary-integer cases produced identical results or exact exceptions;
- Google OSV `semver_index` applicable suite: Oracle and Candidate `3 passed` each;
- exact macOS arm64 wheel, 15-pair local evidence: parse `1.72x`, compare `1.32x`, match `1.40x` median speedup with identical output digests;
- Google OSV 20,000-version exact-wheel evidence: normalize `1.21x`, sort `1.15x`, identical digests;
- native wheel, universal fallback wheel and sdist passed strict metadata, `RECORD`, namespace, console-script, cache/test/binary sanitation and Twine checks.

These are local Build Lane observations, not public release or universal speed claims. CI and public reinstall remain required before `DONE`.

## Distribution limitation

The distribution name is `fast-semver-rs`, while existing consumers depend on
the separate `semver` distribution. Package resolvers do not treat one as
satisfying the other even though both provide the `semver` namespace. The
controlled opt-in flow after release will therefore be:

```bash
python -m pip uninstall -y semver
python -m pip install fast-semver-rs
python -c "from semver import Version; print(Version.parse('1.2.3-rc.1'))"
```

Do not install both distributions together. Roll back with
`python -m pip uninstall -y fast-semver-rs && python -m pip install 'semver==3.0.4'`.
An upstream optional native backend is the preferred broad-adoption path; no
upstream acceptance is claimed.

## Development

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python maturin pytest pytest-cov pytest-randomly
.venv/bin/maturin develop --release
.venv/bin/python -m pytest -q tests upstream/tests
```

BSD-3-Clause. See `THIRD_PARTY_NOTICES.md` before redistribution.
