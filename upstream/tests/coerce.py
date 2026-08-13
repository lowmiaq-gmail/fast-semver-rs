"""Materialized from upstream's docs/advanced/coerce.py symlink for Windows CI."""

import re
from semver import Version
from typing import Optional, Tuple


BASEVERSION = re.compile(
    r"""[vV]?
        (?P<major>0|[1-9]\d*)
        (\.
        (?P<minor>0|[1-9]\d*)
        (\.
            (?P<patch>0|[1-9]\d*)
        )?
        )?
    """,
    re.VERBOSE,
)


def coerce(version: str) -> Tuple[Version, Optional[str]]:
    match = BASEVERSION.search(version)
    if not match:
        return (None, version)
    ver = {
        key: 0 if value is None else value for key, value in match.groupdict().items()
    }
    return Version(**ver), match.string[match.end() :]
