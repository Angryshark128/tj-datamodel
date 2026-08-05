"""Shared enums for the Tianji market research toolkit."""

from __future__ import annotations

from enum import Enum


class Market(str, Enum):
    """Market-level grouping of securities."""

    CN_A_SHARE = "CN_A_SHARE"


class Exchange(str, Enum):
    """Chinese stock exchanges covered by the Tianji ecosystem."""

    SSE = "SSE"
    SZSE = "SZSE"
    BSE = "BSE"


class AssetType(str, Enum):
    """Asset class of a security."""

    STOCK = "stock"
    ETF = "etf"
    INDEX = "index"
    FUND = "fund"
    BOND = "bond"
    CONVERTIBLE_BOND = "convertible_bond"
    UNKNOWN = "unknown"


class Currency(str, Enum):
    """Currencies the ecosystem may carry."""

    CNY = "CNY"
    HKD = "HKD"
    USD = "USD"


class Frequency(str, Enum):
    """Bar data frequency."""

    TICK = "tick"
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    MINUTE_60 = "60m"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "1mo"


class AdjustType(str, Enum):
    """Adjustment applied to price data."""

    NONE = "none"
    FORWARD = "forward"
    BACKWARD = "backward"
