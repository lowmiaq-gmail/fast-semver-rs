# Release Report

Current status: `DONE`.

Final release source commit: `d11032c9c572480556275e5189a97bd8a6dad982`.

Public evidence:

- CI `31671558402`: Linux x86_64, macOS arm64, Windows x86_64, universal fallback and sdist contract passed for the exact `0.1.1` source;
- release run `31671636525`: seven immutable artifacts passed five native build lanes, `337` tests per artifact lane, 10,000-case differential, strict artifact audit and exact-artifact consumer/benchmark evidence;
- PyPI Trusted Publishing uploaded `fast-semver-rs==0.1.1`; all five public native reinstall lanes and the unsupported-platform fallback lane passed;
- PyPI JSON read-back returned five native wheels, one universal wheel and one sdist; every SHA256 equals the matching GitHub Release distribution asset;
- an independent clean macOS arm64 environment installed the public native wheel and passed version, native-module, parse, compare and match smoke tests;
- the rendered PyPI `0.1.1` page contains the release-state-invariant gate description and no longer contains the stale `0.1.0` pre-release/DONE warning;
- GitHub Release `v0.1.1` was created last, targets `d11032c9c572480556275e5189a97bd8a6dad982`, is neither draft nor prerelease, and its seven distribution digests equal PyPI.

Release recovery postmortem:

1. Windows CRLF changed Core Metadata description bytes. Root cause: no repository line-ending contract. Permanent fix: `.gitattributes` plus explicit README content type and a stricter metadata equality gate.
2. Release-only Google OSV validation used an empty Oracle venv. Root cause: the consumer harness did not bind the frozen upstream source. Permanent fix: explicit Oracle `PYTHONPATH` and a normal-CI consumer regression.
3. That new regression exposed hard-coded `/tmp` on Windows. Permanent fix: `tempfile.gettempdir()`; CI `31670578682` passed on all three OS lanes.
4. Python 3.7 on x86_64 correctly selected the compatible abi3 native wheel, contradicting the fallback test assumption. Permanent fix: resolve an unsupported native platform (`manylinux2014_i686`) and require the universal wheel. The published universal wheel was then tested independently.
5. The immutable `0.1.0` PyPI long description retained a pre-release status sentence after the release had completed. Root cause: release-specific mutable status was embedded in package metadata, while JSON metadata read-back did not inspect rendered semantics. Permanent fix: publish `0.1.1` with release-state-invariant wording and require a rendered PyPI page semantic read-back.

The first two `0.1.0` release attempts stopped before upload. The third uploaded to PyPI, then correctly remained `PARTIAL` until fallback verification recovered and GitHub Release was created last. The page-level metadata defect was subsequently corrected by the fully successful `0.1.1` release.
