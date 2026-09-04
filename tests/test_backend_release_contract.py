from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

if sys.version_info < (3, 11):
    raise unittest.SkipTest("backend release contract requires stdlib tomllib")

from scripts.check_backend_release_contract import (
    BackendVersions,
    ContractError,
    read_backend_versions,
    validate_versions,
)


class BackendReleaseContractTests(unittest.TestCase):
    def read_fixture(
        self,
        pyproject_version: str,
        cargo_toml_version: str,
        cargo_lock_version: str,
        *,
        other_package_version: str | None = None,
    ) -> BackendVersions:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            backend = root / "backend"
            backend.mkdir()
            (backend / "pyproject.toml").write_text(
                "[project]\n"
                'name = "fast-semver-rs-backend"\n'
                f'version = "{pyproject_version}"\n',
                encoding="utf-8",
            )
            (backend / "Cargo.toml").write_text(
                "[package]\n"
                'name = "fast-semver-rs-backend"\n'
                f'version = "{cargo_toml_version}"\n',
                encoding="utf-8",
            )
            lock_packages = ""
            if other_package_version is not None:
                lock_packages += (
                    '[[package]]\nname = "another-package"\n'
                    f'version = "{other_package_version}"\n\n'
                )
            lock_packages += (
                '[[package]]\nname = "fast-semver-rs-backend"\n'
                f'version = "{cargo_lock_version}"\n'
            )
            (backend / "Cargo.lock").write_text(
                f"version = 4\n\n{lock_packages}", encoding="utf-8"
            )
            return read_backend_versions(root)

    def test_matching_versions_pass(self):
        validate_versions(self.read_fixture("0.1.2", "0.1.2", "0.1.2"))

    def test_pyproject_only_bump_fails(self):
        with self.assertRaisesRegex(ContractError, "version contract violated"):
            validate_versions(self.read_fixture("0.1.3", "0.1.2", "0.1.2"))

    def test_stale_cargo_lock_fails(self):
        with self.assertRaisesRegex(ContractError, "backend/Cargo.lock"):
            validate_versions(self.read_fixture("0.1.3", "0.1.3", "0.1.2"))

    def test_requested_release_version_must_match(self):
        versions = self.read_fixture("0.1.2", "0.1.2", "0.1.2")
        with self.assertRaisesRegex(ContractError, "requested version"):
            validate_versions(versions, requested_version="0.1.3")

    def test_reads_named_lock_package_not_another_version(self):
        versions = self.read_fixture(
            "0.1.2", "0.1.2", "0.1.2", other_package_version="99.0.0"
        )
        self.assertEqual(versions.cargo_lock, "0.1.2")


if __name__ == "__main__":
    unittest.main()
