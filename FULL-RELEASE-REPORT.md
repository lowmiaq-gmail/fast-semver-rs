# Release Report

Current status: `DONE`.

Release source commit: `016a416da374e8ef6f37c3840aeb331f91d7798e`.

Public evidence:

- CI `31670578682`: Linux x86_64, macOS arm64, Windows x86_64, universal fallback and sdist contract passed, including the frozen Google OSV consumer regression;
- release run `31670657636`: seven immutable artifacts passed five native build lanes, `337` tests per artifact lane, 10,000-case differential, strict artifact audit and exact-artifact consumer/benchmark evidence;
- PyPI Trusted Publishing uploaded `fast-semver-rs==0.1.0`; all five public native reinstall lanes passed;
- PyPI JSON read-back returned five native wheels, one universal wheel and one sdist; every SHA256 equals the audited artifact from run `31670657636`;
- public resolver simulation for CPython 3.7 on unsupported `manylinux2014_i686` selected `fast_semver_rs-0.1.0-py3-none-any.whl`; its clean install passed `337` tests and the 10,000-case differential;
- GitHub Release `v0.1.0` was created last, targets `016a416da374e8ef6f37c3840aeb331f91d7798e`, is neither draft nor prerelease, and its seven distribution digests equal PyPI.

Release recovery postmortem:

1. Windows CRLF changed Core Metadata description bytes. Root cause: no repository line-ending contract. Permanent fix: `.gitattributes` plus explicit README content type and a stricter metadata equality gate.
2. Release-only Google OSV validation used an empty Oracle venv. Root cause: the consumer harness did not bind the frozen upstream source. Permanent fix: explicit Oracle `PYTHONPATH` and a normal-CI consumer regression.
3. That new regression exposed hard-coded `/tmp` on Windows. Permanent fix: `tempfile.gettempdir()`; CI `31670578682` passed on all three OS lanes.
4. Python 3.7 on x86_64 correctly selected the compatible abi3 native wheel, contradicting the fallback test assumption. Permanent fix: resolve an unsupported native platform (`manylinux2014_i686`) and require the universal wheel. The published universal wheel was then tested independently.

The first two release attempts stopped before upload. The third uploaded to PyPI, then correctly remained `PARTIAL` until fallback verification recovered and GitHub Release was created last.
