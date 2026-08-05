"""Shared immutable data models for the Tianji market research toolkit."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from tj_datamodel.enums import AdjustType, AssetType, Exchange, Frequency, Market


@dataclass(frozen=True)
class Symbol:
    """A canonical security identifier."""

    code: str
    exchange: Exchange
    suffix: str
    market: Market
    asset_type: AssetType
    normalized: str


@dataclass(frozen=True)
class Bar:
    """A single OHLCV bar."""

    symbol: str
    trade_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None
    amount: float | None = None
    frequency: Frequency = Frequency.DAILY
    adjust: AdjustType = AdjustType.NONE
    timestamp: datetime | None = None


@dataclass(frozen=True)
class ReturnPoint:
    """A dated return value, decimal (0.0123 == 1.23%)."""

    trade_date: date
    value: float
    symbol: str | None = None


@dataclass(frozen=True)
class EquityPoint:
    """A dated equity or net-value point."""

    trade_date: date
    value: float
    symbol: str | None = None
