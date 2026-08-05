"""Base exceptions for the Tianji data model."""

from __future__ import annotations


class TianjiDataModelError(Exception):
    """Base error for tj-datamodel."""


class ValidationError(TianjiDataModelError):
    """Raised by optional validation helpers."""
