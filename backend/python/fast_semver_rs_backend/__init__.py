"""Small parser-only backend consumed by an optional python-semver adapter."""

from ._native import parse_parts

__all__ = ["parse_parts"]
