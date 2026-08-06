# tj-datamodel API

> 共享数据模型与枚举，零外部运行时依赖。构造时不校验，校验函数由上层包按需调用。

## 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [数据模型](#数据模型)
  - [Symbol](#symbol)
  - [Bar](#bar)
  - [ReturnPoint](#returnpoint)
  - [EquityPoint](#equitypoint)
- [枚举](#枚举)
  - [Exchange](#exchange)
  - [Market](#market)
  - [AssetType](#assettype)
  - [Currency](#currency)
  - [Frequency](#frequency)
  - [AdjustType](#adjusttype)
- [校验函数](#校验函数)
- [异常](#异常)

## 安装

```bash
pip install tj-datamodel
```

## 快速开始

```python
from datetime import date

from tj_datamodel import AssetType, Bar, Exchange, Market, Symbol

# 构造一个证券标识
s = Symbol(
    code="600519",
    exchange=Exchange.SSE,
    suffix="SH",
    market=Market.CN_A_SHARE,
    asset_type=AssetType.STOCK,
    normalized="600519.SH",
)
s.normalized  # "600519.SH"

# 构造一根日 K
bar = Bar(
    symbol="600519.SH",
    trade_date=date(2026, 8, 6),
    open=1450.0,
    high=1488.0,
    low=1440.0,
    close=1472.0,
    volume=3_200_000,
    amount=4_700_000_000,
)
bar.close  # 1472.0
```

## 数据模型

所有模型都是 `frozen=True` 的不可变 dataclass：字段只能在构造时设置，之后不可修改。

### Symbol

证券唯一标识。由 tj-symbols 等上层包生成并填充。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `str` | 6 位数字代码，如 `"600519"` |
| `exchange` | [`Exchange`](#exchange) | 交易所枚举 |
| `suffix` | `str` | 交易所后缀，如 `"SH"` / `"SZ"` / `"BJ"` |
| `market` | [`Market`](#market) | 市场分组枚举 |
| `asset_type` | [`AssetType`](#assettype) | 资产类型枚举 |
| `normalized` | `str` | 标准格式字符串，如 `"600519.SH"` |

### Bar

单根 OHLCV K 线。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `symbol` | `str` | — | 证券标识（建议标准格式） |
| `trade_date` | `date` | — | 交易日期 |
| `open` / `high` / `low` / `close` | `float` | — | 开高低收 |
| `volume` | `float \| None` | `None` | 成交量 |
| `amount` | `float \| None` | `None` | 成交额 |
| `frequency` | [`Frequency`](#frequency) | `Frequency.DAILY` | 周期 |
| `adjust` | [`AdjustType`](#adjusttype) | `AdjustType.NONE` | 复权方式 |
| `timestamp` | `datetime \| None` | `None` | 时间戳（tick/分钟级） |

### ReturnPoint

带日期的收益率点，小数值（`0.0123` 表示 1.23%）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trade_date` | `date` | — | 日期 |
| `value` | `float` | — | 收益率小数值 |
| `symbol` | `str \| None` | `None` | 可选证券标识 |

### EquityPoint

带日期的净值/权益点。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trade_date` | `date` | — | 日期 |
| `value` | `float` | — | 净值 |
| `symbol` | `str \| None` | `None` | 可选证券标识 |

## 枚举

全部继承 `(str, Enum)`：可用 `== "SSE"` 直接比较，也能 `Exchange.SSE.value` 取值。注意 `str(Exchange.SSE)` 在 Python 3.11+ 返回 `"Exchange.SSE"` 而非 `"SSE"`，取值请用 `.value`。

### Exchange

| 成员 | 值 | 含义 |
| --- | --- | --- |
| `Exchange.SSE` | `"SSE"` | 上交所 |
| `Exchange.SZSE` | `"SZSE"` | 深交所 |
| `Exchange.BSE` | `"BSE"` | 北交所 |

### Market

| 成员 | 值 | 含义 |
| --- | --- | --- |
| `Market.CN_A_SHARE` | `"CN_A_SHARE"` | A 股市场 |

### AssetType

| 成员 | 值 | 含义 |
| --- | --- | --- |
| `AssetType.STOCK` | `"stock"` | 股票 |
| `AssetType.ETF` | `"etf"` | ETF |
| `AssetType.INDEX` | `"index"` | 指数 |
| `AssetType.FUND` | `"fund"` | 基金 |
| `AssetType.BOND` | `"bond"` | 债券 |
| `AssetType.CONVERTIBLE_BOND` | `"convertible_bond"` | 可转债 |
| `AssetType.UNKNOWN` | `"unknown"` | 未知 |

### Currency

| 成员 | 值 |
| --- | --- |
| `Currency.CNY` | `"CNY"` |
| `Currency.HKD` | `"HKD"` |
| `Currency.USD` | `"USD"` |

### Frequency

| 成员 | 值 |
| --- | --- |
| `Frequency.TICK` | `"tick"` |
| `Frequency.MINUTE_1` | `"1m"` |
| `Frequency.MINUTE_5` | `"5m"` |
| `Frequency.MINUTE_15` | `"15m"` |
| `Frequency.MINUTE_30` | `"30m"` |
| `Frequency.MINUTE_60` | `"60m"` |
| `Frequency.DAILY` | `"1d"` |
| `Frequency.WEEKLY` | `"1w"` |
| `Frequency.MONTHLY` | `"1mo"` |

### AdjustType

| 成员 | 值 |
| --- | --- |
| `AdjustType.NONE` | `"none"` |
| `AdjustType.FORWARD` | `"forward"` |
| `AdjustType.BACKWARD` | `"backward"` |

## 校验函数

构造时**不**校验。数据从外部进入生态边界时，可调用这些函数显式校验；不通过抛 [`ValidationError`](#异常)。

```python
from tj_datamodel import AssetType, Exchange, Market, Symbol
from tj_datamodel.validators import validate_symbol

s = Symbol("000001", Exchange.SZSE, "SZ", Market.CN_A_SHARE, AssetType.STOCK, "000001.SZ")
validate_symbol(s)  # 通过

bad = Symbol("00X", Exchange.SZSE, "SZ", Market.CN_A_SHARE, AssetType.STOCK, "00X.SZ")
validate_symbol(bad)  # ValidationError: code must be numeric
```

| 函数 | 签名 | 校验内容 |
| --- | --- | --- |
| `validate_symbol` | `(symbol: Symbol) -> None` | code 为纯数字；suffix 与 normalized 后缀一致 |
| `validate_bar` | `(bar: Bar) -> None` | OHLC 顺序：`low <= open/close <= high` |
| `validate_point_date` | `(point: ReturnPoint \| EquityPoint) -> None` | `trade_date` 必须是纯 `date`（拒绝 `datetime`） |

## 异常

| 异常 | 父类 | 说明 |
| --- | --- | --- |
| `TianjiDataModelError` | `Exception` | 本包异常基类 |
| `ValidationError` | `TianjiDataModelError` | 校验不通过 |
