from __future__ import annotations

import importlib.util
import os

import pytest
import semver


def test_native_module_and_frozen_version() -> None:
    native = importlib.util.find_spec("semver._native")
    if os.environ.get("FAST_SEMVER_EXPECT_NATIVE") == "1":
        assert native is not None
        assert native.origin and native.origin.endswith((".so", ".pyd"))
    assert semver.__version__ == "3.0.4"


def test_python_arbitrary_integer_fallback() -> None:
    huge = "999999999999999999999999999999.2.3"
    parsed = semver.Version.parse(huge)
    assert parsed.major == int(huge.split(".", 1)[0])
    assert str(parsed) == huge


def test_subclass_and_optional_minor_patch_remain_python_contract() -> None:
    class CustomVersion(semver.Version):
        pass

    parsed = CustomVersion.parse("1.2.3-rc.1+build.2")
    assert type(parsed) is CustomVersion
    assert parsed.to_tuple() == (1, 2, 3, "rc.1", "build.2")
    assert semver.Version.parse("7", optional_minor_and_patch=True).to_tuple() == (
        7,
        0,
        0,
        None,
        None,
    )


@pytest.mark.parametrize("value", ["01.2.3", "1.02.3", "1.2", "", "v1.2.3"])
def test_exact_invalid_message(value: str) -> None:
    with pytest.raises(ValueError) as captured:
        semver.Version.parse(value)
    assert str(captured.value) == f"{value} is not valid SemVer string"
