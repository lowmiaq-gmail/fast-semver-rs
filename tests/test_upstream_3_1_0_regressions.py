from __future__ import annotations

import semver


def test_bump_prerelease_increments_a_non_numeric_suffix() -> None:
    assert (
        str(semver.Version.parse("3.4.5-rc1").bump_prerelease())
        == "3.4.5-rc1.0"
    )
    assert (
        str(semver.Version.parse("3.4.5-rc9").bump_prerelease())
        == "3.4.5-rc9.0"
    )


def test_bump_prerelease_can_bump_a_release_patch() -> None:
    version = semver.Version.parse("3.4.5")
    assert str(version.bump_prerelease(bump_when_empty=True)) == "3.4.6-rc.1"
    assert str(version.bump_prerelease("dev", bump_when_empty=True)) == "3.4.6-dev.1"


def test_next_version_does_not_strip_build_metadata_without_bumping() -> None:
    assert (
        str(semver.Version.parse("1.2.3+build.5").next_version("patch"))
        == "1.2.4"
    )
    assert (
        str(semver.Version.parse("1.2.3-rc.1+build.5").next_version("prerelease"))
        == "1.2.3-rc.2"
    )


def test_next_version_switches_prerelease_token() -> None:
    version = semver.Version.parse("1.2.3-dev.4")
    assert str(version.next_version("prerelease", "rc")) == "1.2.3-rc.1"
