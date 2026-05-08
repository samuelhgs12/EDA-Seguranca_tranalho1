"""Validation helpers for envelope interoperability rules."""

from __future__ import annotations

from pathlib import Path


LEGACY_BIN_EXTENSION = ".bin"


def ensure_supported_envelope_extension(path: str | Path, expected_suffix: str) -> None:
    """Ensure a given artifact path matches the expected extension.

    Args:
        path: File path to validate.
        expected_suffix: Required extension such as `.cif`, `.env`, or `.sig`.

    Raises:
        ValueError: If extension does not match.
    """

    suffix = Path(path).suffix.lower()
    if suffix != expected_suffix.lower():
        hint = ""
        if suffix == LEGACY_BIN_EXTENSION:
            hint = f" Legacy '.bin' is not accepted; rename/use '{expected_suffix}'."
        raise ValueError(
            f"Invalid extension '{suffix}' for '{path}'. Expected '{expected_suffix}'.{hint}"
        )
