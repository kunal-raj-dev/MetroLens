"""Portable, single-component names for inspection storage and API identifiers."""

import re


INSPECTION_ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}"
_SAFE_COMPONENT = re.compile(INSPECTION_ID_PATTERN, re.ASCII)
_WINDOWS_DEVICE_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}


def validate_inspection_id(value: str) -> str:
    """Reject paths, ambiguous Windows names, and excessively long identifiers."""
    if (
        not isinstance(value, str)
        or _SAFE_COMPONENT.fullmatch(value) is None
        or value.upper() in _WINDOWS_DEVICE_NAMES
    ):
        raise ValueError("Invalid inspection ID: use 1–128 ASCII letters, digits, underscores or hyphens, starting with a letter or digit")
    return value


def validate_crop_name(value: str) -> str:
    """Validate without silently mapping distinct evidence fields to one file."""
    try:
        return validate_inspection_id(value)
    except ValueError as error:
        raise ValueError("Invalid crop field name") from error
