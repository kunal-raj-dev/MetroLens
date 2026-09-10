"""Build ReportLab markup from trusted templates and text-only field values."""

from collections.abc import Iterable
from html import escape
from string import Formatter


class _Markup(str):
    """Internal marker for markup built from a source-code template."""


def text(value: object) -> str:
    """Escape a supplied value exactly once, preserving generated markup."""
    if isinstance(value, _Markup):
        return value
    return _Markup(escape("" if value is None else str(value), quote=True))


class _TextFormatter(Formatter):
    def format_field(self, value: object, format_spec: str) -> str:
        if isinstance(value, _Markup) and not format_spec:
            return value
        return text(super().format_field(value, format_spec))


def markup(template: str, *values: object) -> str:
    """Interpolate escaped values into a constant, trusted ReportLab template.

    Callers must supply a source-code literal as the template. Data belongs in
    positional values, never in the template or a markup attribute.
    """
    return _Markup(_TextFormatter().format(template, *values))


def join_markup(separator: str, values: Iterable[object]) -> str:
    """Join escaped fields/generated markup with a trusted static separator."""
    return _Markup(separator.join(text(value) for value in values))


DRAFT_NOTICE = (
    "ASSISTIVE DRAFT — Requires authorized human review. "
    "This document does not issue a statutory notice, certify evidence, "
    "or establish an officer's identity or signature."
)
