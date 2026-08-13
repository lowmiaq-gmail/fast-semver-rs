"""Materialized from upstream's docs symlink for Windows CI."""

from semver import Version


class SemVerWithVPrefix(Version):
    @classmethod
    def parse(cls, version: str) -> "SemVerWithVPrefix":
        if not version[0] in ("v", "V"):
            raise ValueError(
                f"{version!r}: not a valid semantic version tag. "
                "Must start with 'v' or 'V'"
            )
        return super().parse(version[1:], optional_minor_and_patch=True)

    def __str__(self) -> str:
        return "v" + super().__str__()
