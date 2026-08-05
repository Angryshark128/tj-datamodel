"""Test suite for tj-datamodel."""

from dataclasses import FrozenInstanceError
from datetime import date, datetime

import pytest

from tj_datamodel import (
    AdjustType,
    AssetType,
    Bar,
    Currency,
    EquityPoint,
    Exchange,
    Frequency,
    Market,
    ReturnPoint,
    Symbol,
    TianjiDataModelError,
    ValidationError,
    __version__,
)
from tj_datamodel.validators import validate_bar, validate_point_date, validate_symbol


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_enums_are_str_subclass() -> None:
    # str-subclass enums compare and coerce to their value
    assert Exchange.SSE == "SSE"
    assert Exchange.SSE.value == "SSE"
    assert Market.CN_A_SHARE == "CN_A_SHARE"
    assert AssetType.STOCK == "stock"
    assert Currency.CNY == "CNY"
    assert Frequency.DAILY == "1d"
    assert AdjustType.NONE == "none"
    assert f"{Exchange.SSE}" == "SSE"


def test_symbol_construction() -> None:
    symbol = Symbol(
        code="600519",
        exchange=Exchange.SSE,
        suffix="SH",
        market=Market.CN_A_SHARE,
        asset_type=AssetType.STOCK,
        normalized="600519.SH",
    )
    assert symbol.normalized == "600519.SH"


def test_bar_construction_with_defaults() -> None:
    bar = Bar(
        symbol="600519.SH",
        trade_date=date(2026, 8, 4),
        open=1800.0,
        high=1820.0,
        low=1780.0,
        close=1810.0,
    )
    assert bar.frequency == Frequency.DAILY
    assert bar.adjust == AdjustType.NONE
    assert bar.volume is None
    assert bar.timestamp is None


def test_return_point_construction() -> None:
    point = ReturnPoint(trade_date=date(2026, 8, 4), value=0.0123, symbol="600519.SH")
    assert point.value == 0.0123


def test_equity_point_construction() -> None:
    point = EquityPoint(trade_date=date(2026, 8, 4), value=1.0235)
    assert point.value == 1.0235


def test_models_are_frozen() -> None:
    symbol = Symbol(
        code="600519",
        exchange=Exchange.SSE,
        suffix="SH",
        market=Market.CN_A_SHARE,
        asset_type=AssetType.STOCK,
        normalized="600519.SH",
    )
    with pytest.raises(FrozenInstanceError):
        symbol.code = "000001"  # type: ignore[misc]


def test_validate_symbol_ok() -> None:
    symbol = Symbol(
        code="600519",
        exchange=Exchange.SSE,
        suffix="SH",
        market=Market.CN_A_SHARE,
        asset_type=AssetType.STOCK,
        normalized="600519.SH",
    )
    validate_symbol(symbol)


def test_validate_symbol_bad_code() -> None:
    symbol = Symbol(
        code="abc",
        exchange=Exchange.SSE,
        suffix="SH",
        market=Market.CN_A_SHARE,
        asset_type=AssetType.STOCK,
        normalized="abc.SH",
    )
    with pytest.raises(ValidationError):
        validate_symbol(symbol)


def test_validate_bar_ok() -> None:
    bar = Bar(
        symbol="600519.SH",
        trade_date=date(2026, 8, 4),
        open=1800.0,
        high=1820.0,
        low=1780.0,
        close=1810.0,
    )
    validate_bar(bar)


def test_validate_bar_bad_ohlc() -> None:
    bar = Bar(
        symbol="600519.SH",
        trade_date=date(2026, 8, 4),
        open=1900.0,
        high=1820.0,
        low=1780.0,
        close=1810.0,
    )
    with pytest.raises(ValidationError):
        validate_bar(bar)


def test_validate_point_date() -> None:
    point = ReturnPoint(trade_date=date(2026, 8, 4), value=0.01)
    validate_point_date(point)
    with pytest.raises(ValidationError):
        validate_point_date(ReturnPoint(trade_date=datetime(2026, 8, 4), value=0.01))


def test_base_error_hierarchy() -> None:
    assert issubclass(ValidationError, TianjiDataModelError)
