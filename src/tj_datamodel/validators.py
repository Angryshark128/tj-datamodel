"""Lightweight validation helpers for Tianji data models.

These are optional: constructors do not validate on creation. Upper-level
packages can opt into validation at their boundaries.
"""

from __future__ import annotations

from datetime import date

from tj_datamodel.errors import ValidationError
from tj_datamodel.models import Bar, EquityPoint, ReturnPoint, Symbol


def validate_symbol(symbol: Symbol) -> None:
    """Check basic internal consistency of a Symbol."""
    if not symbol.code or not symbol.code.isdigit():
        raise ValidationError(f"symbol code must be numeric, got {symbol.code!r}")
    if symbol.suffix != symbol.normalized.split(".")[-1]:
        raise ValidationError(f"suffix {symbol.suffix!r} does not match normalized {symbol.normalized!r}")


def validate_bar(bar: Bar) -> None:
    """Check OHLC ordering of a Bar."""
    if not (bar.low <= bar.open <= bar.high and bar.low <= bar.close <= bar.high):
        raise ValidationError(
            f"OHLC not ordered for {bar.symbol} on {bar.trade_date}: "
            f"open={bar.open} high={bar.high} low={bar.low} close={bar.close}"
        )


def validate_point_date(point: ReturnPoint | EquityPoint) -> None:
    """Check that a point uses a plain date (not a datetime).

    datetime is a date subclass, so isinstance would wrongly accept it.
    """
    if type(point.trade_date) is not date:
        raise ValidationError(f"trade_date must be a plain date, got {point.trade_date!r}")
