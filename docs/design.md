

1. 项目概述

1.1 项目名称





母品牌：Tianji



子项目：tj-datamodel



展示名：Tianji DataModel



Python 包名：tj-datamodel



Python 模块名：tj_datamodel



CLI 命令：无

1.2 项目定位

tj-datamodel 是 Tianji 生态的共享数据模型与类型定义基础包。

一句话定位：

Tianji DataModel provides shared data models and type definitions for the Tianji market research toolkit.

中文定位：

Tianji DataModel 为 Tianji 生态提供共享的数据结构、枚举和类型约定。

1.3 用户感知

tj-datamodel 不是普通用户需要主动安装的入口产品，而是 Tianji 上层包的内部公共依赖。

普通用户安装：

pip install tj-metrics
pip install tj-symbols
pip install tj-backtest

这些包会自动安装：

tj-datamodel

用户通常不需要执行：

pip install tj-datamodel

除非他是开发者，或者只想单独使用 Tianji 的数据模型。



2. 为什么需要 tj-datamodel

随着 Tianji 生态逐步包含：

tj-calendar
tj-symbols
tj-data
tj-metrics
tj-factors
tj-backtest
tj-terminal

多个模块都会用到相同概念：

Symbol
Market
Exchange
AssetType
Frequency
AdjustType
Bar
ReturnPoint
EquityPoint

如果每个包都重复定义，会带来问题：





tj-symbols 的 Symbol 和 tj-data 的 symbol 不一致。



tj-data 的 K 线数据和 tj-factors 的输入不一致。



tj-backtest 的净值曲线和 tj-metrics 的输入不一致。



每个包重复维护枚举和基础类型。



生态整合时需要大量适配层。

因此需要一个小而稳定的公共数据模型包。



3. 核心原则

3.1 只放稳定公共类型

tj-datamodel 只放跨多个模块都会复用、并且相对稳定的数据结构。

例如：

Exchange
Market
AssetType
Symbol
Bar
ReturnPoint
EquityPoint

3.2 不做业务逻辑

tj-datamodel 不应包含：





数据下载。



格式转换。



指标计算。



因子计算。



回测逻辑。



交易执行。



在线更新。

3.3 零重依赖

MVP 阶段不依赖：

pandas
numpy
pydantic
requests
akshare
tushare

建议只使用 Python 标准库：

dataclasses
datetime
enum
typing

3.4 避免变成 tj-core

项目命名为 tj-datamodel，而不是 tj-core，是为了避免它变成大杂烩。

禁止把“暂时不知道放哪”的功能塞进 tj-datamodel。

3.5 上层包依赖它，用户不必主动安装

例如 tj-metrics 的依赖声明：

[project]
name = "tj-metrics"
dependencies = [
  "tj-datamodel>=0.1,<0.2"
]

用户安装 tj-metrics 时，tj-datamodel 会自动安装。

3.6 tj-calendar 暂不依赖 tj-datamodel

tj-calendar 的核心功能只需要：

market 字符串
date
calendar_version
coverage_start / coverage_end

为了保持极轻量、离线优先和独立可用，tj-calendar v0.1.0 暂不强依赖 tj-datamodel。

tj-calendar 可以使用与 tj-datamodel 兼容的字符串标识：

CN_A_SHARE
SSE
SZSE
BSE

但不引入包依赖。

文档约定：

Calendar market identifiers are string-compatible with tj-datamodel Market / Exchange values.

中文：

tj-calendar 使用的市场标识字符串与 tj-datamodel 中的 Market / Exchange 枚举值保持兼容。

3.7 不在 v0.1.0 放 CalendarInfo

因为 tj-calendar v0.1.0 不依赖 tj-datamodel，所以 CalendarInfo 不放入 tj-datamodel v0.1.0。

否则会出现：

datamodel 定义 CalendarInfo
calendar 不使用 CalendarInfo

这会造成边界不清。

未来如果多个包确实都需要日历元信息，再考虑迁移。



4. 生态依赖关系

推荐依赖关系：

tj-datamodel
  ↑
  ├── tj-symbols
  ├── tj-data
  ├── tj-factors
  ├── tj-backtest
  └── tj-metrics

更细分：

强依赖：
  tj-symbols
  tj-data
  tj-factors
  tj-backtest

可选或轻依赖：
  tj-metrics

暂不依赖：
  tj-calendar

4.1 tj-symbols

tj-symbols 使用：





Symbol



Exchange



Market



AssetType

但 SymbolFormatInfo 不放在 tj-datamodel，因为它属于 tj-symbols 的格式注册表。

4.2 tj-data

tj-data 使用：





Symbol



Bar



Frequency



AdjustType



AssetType

4.3 tj-factors

tj-factors 使用：





Bar



Frequency



未来可能使用 FactorPoint

4.4 tj-backtest

tj-backtest 使用：





Bar



ReturnPoint



EquityPoint



未来可能使用 Order、Trade、Position

4.5 tj-metrics

tj-metrics 可以支持：





ReturnPoint



EquityPoint

但同时应允许用户传入：

list[float]
numpy.ndarray
pandas.Series

即 tj-metrics 不应强迫用户必须构造 datamodel 对象。



5. MVP 支持范围

5.1 v0.1.0 必须支持的枚举

Market
Exchange
AssetType
Currency
Frequency
AdjustType

5.2 v0.1.0 必须支持的模型

Symbol
Bar
ReturnPoint
EquityPoint

5.3 v0.1.0 必须支持的异常

TianjiDataModelError
ValidationError

5.4 v0.1.0 不支持

CalendarInfo
Quote
FactorPoint
Order
Trade
Position
Portfolio
Account
CorporateAction
Dividend
Split
IndexConstituent
FinancialStatement
NewsItem
ResearchReport
Tick
OrderBook

这些模型等具体上层项目需要时再增加。



6. 枚举设计

6.1 Market

class Market(str, Enum):
    CN_A_SHARE = "CN_A_SHARE"

MVP 只定义中国 A 股整体市场。

未来可扩展：

HK_STOCK
US_STOCK
CN_FUTURES

6.2 Exchange

class Exchange(str, Enum):
    SSE = "SSE"
    SZSE = "SZSE"
    BSE = "BSE"

含义：

SSE   上海证券交易所
SZSE  深圳证券交易所
BSE   北京证券交易所

6.3 AssetType

class AssetType(str, Enum):
    STOCK = "stock"
    ETF = "etf"
    INDEX = "index"
    FUND = "fund"
    BOND = "bond"
    CONVERTIBLE_BOND = "convertible_bond"
    UNKNOWN = "unknown"

6.4 Currency

class Currency(str, Enum):
    CNY = "CNY"
    HKD = "HKD"
    USD = "USD"

MVP 主要使用 CNY，但预留 HKD、USD 有助于未来扩展。

6.5 Frequency

class Frequency(str, Enum):
    TICK = "tick"
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    MINUTE_60 = "60m"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "1mo"

6.6 AdjustType

class AdjustType(str, Enum):
    NONE = "none"
    FORWARD = "forward"
    BACKWARD = "backward"

含义：

NONE      不复权
FORWARD   前复权
BACKWARD  后复权



7. 模型设计

7.1 Symbol

Symbol 表示一个证券标识。

@dataclass(frozen=True)
class Symbol:
    code: str
    exchange: Exchange
    suffix: str
    market: Market
    asset_type: AssetType
    normalized: str

示例：

Symbol(
    code="600519",
    exchange=Exchange.SSE,
    suffix="SH",
    market=Market.CN_A_SHARE,
    asset_type=AssetType.STOCK,
    normalized="600519.SH",
)

字段说明：

code        证券代码，例如 600519
exchange    交易所枚举，例如 Exchange.SSE
suffix      Tianji 标准后缀，例如 SH
market      市场枚举，例如 Market.CN_A_SHARE
asset_type  资产类型，例如 AssetType.STOCK
normalized  Tianji 标准格式，例如 600519.SH

7.2 Bar

Bar 表示一根 K 线或 OHLCV 数据。

@dataclass(frozen=True)
class Bar:
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

示例：

Bar(
    symbol="600519.SH",
    trade_date=date(2026, 8, 4),
    open=1800.0,
    high=1820.0,
    low=1780.0,
    close=1810.0,
    volume=1234567,
    amount=2234567890.0,
    frequency=Frequency.DAILY,
    adjust=AdjustType.NONE,
    timestamp=None,
)

字段说明：

symbol      Tianji 标准格式字符串，例如 600519.SH
trade_date  交易日
open        开盘价
high        最高价
low         最低价
close       收盘价
volume      成交量，可为空
amount      成交额，可为空
frequency   数据频率
adjust      复权类型
timestamp   分钟线或实时数据时间戳，日线可为空

为什么 symbol 用字符串

Bar.symbol 使用 Tianji 标准格式字符串，而不是嵌套 Symbol 对象。

原因：





下游使用更简单。



避免对象嵌套过深。



更接近 pandas / CSV / parquet 等表格数据习惯。



便于序列化。

约定：

Bar.symbol 必须使用 Tianji 标准格式，例如 600519.SH。

trade_date 与 timestamp

日线数据主要使用：

trade_date

分钟线或实时数据可以额外使用：

timestamp

不强制用 timestamp 表达日线日期，避免日线 00:00:00 或收盘时间约定不一致。

7.3 ReturnPoint

ReturnPoint 表示某个日期的收益率点。

@dataclass(frozen=True)
class ReturnPoint:
    trade_date: date
    value: float
    symbol: str | None = None

示例：

ReturnPoint(
    trade_date=date(2026, 8, 4),
    value=0.0123,
    symbol="600519.SH",
)

字段说明：

trade_date  交易日
value       收益率，例如 0.0123 表示 1.23%
symbol      可选；单标的收益可填，组合收益可为空

7.4 EquityPoint

EquityPoint 表示净值或账户权益曲线上的一个点。

@dataclass(frozen=True)
class EquityPoint:
    trade_date: date
    value: float
    symbol: str | None = None

示例：

EquityPoint(
    trade_date=date(2026, 8, 4),
    value=1.0235,
    symbol=None,
)

字段说明：

trade_date  交易日
value       净值或账户权益
symbol      可选；单标的净值可填，组合净值可为空



8. 数值与时间约定

8.1 数值类型

MVP 使用 float，不强制使用 Decimal。

原因：





量化计算普遍使用 float / numpy。



公共模型不应过度约束上层实现。



Decimal 会增加使用复杂度。

未来如果 tj-backtest 涉及精确现金账本，可以在回测模块内部局部使用 Decimal。

8.2 收益率约定

收益率使用小数表示：

0.0123 = 1.23%
-0.02 = -2%

8.3 交易日约定

日频数据使用：

trade_date: date

分钟线、tick 或实时数据额外使用：

timestamp: datetime | None

8.4 时区约定

MVP 不强制在模型中携带时区。

中国市场默认语义为：

Asia/Shanghai

未来如扩展跨市场数据，再考虑统一时区字段或约定。



9. 异常设计

class TianjiDataModelError(Exception):
    pass

class ValidationError(TianjiDataModelError):
    pass

MVP 可以只提供基础异常。

由于 dataclass 本身不做强校验，ValidationError 主要用于未来可选校验函数。



10. 校验策略

10.1 MVP 不做强校验

MVP 模型以轻量为主，不在构造时执行复杂校验。

例如不强制检查：





symbol 是否真实存在。



OHLC 是否满足 low <= open <= high。



volume 是否非负。



trade_date 是否为真实交易日。

这些校验属于上层包或可选校验工具。

10.2 可选轻量校验

未来可以提供：

validate_symbol(symbol: Symbol) -> None
validate_bar(bar: Bar) -> None

但 MVP 不一定实现。



11. 不放入 v0.1.0 的模型

11.1 CalendarInfo

不放入原因：





tj-calendar v0.1.0 暂不依赖 tj-datamodel。



日历元信息主要是 tj-calendar 内部概念。



目前没有多个上层包都需要 CalendarInfo。

11.2 Quote

实时行情快照暂不放入。

原因：





字段设计可能受数据源影响。



tj-data 和 tj-terminal 设计时再决定。

11.3 FactorPoint

因子值模型暂不放入。

原因：





因子可能是单值、横截面、时间序列、矩阵。



需要等 tj-factors 设计时再确定。

11.4 Order / Trade / Position

交易与回测相关模型暂不放入。

原因：





与回测引擎设计强相关。



字段设计牵涉撮合、费用、滑点、账户体系。



不适合在 datamodel MVP 中提前固定。

11.5 Portfolio / Account

组合和账户模型暂不放入。

原因：





设计复杂。



与回测和实盘系统绑定较深。

11.6 CorporateAction / Dividend / Split

公司行为数据暂不放入。

原因：





数据源差异大。



字段复杂。



与复权和行情数据处理关系密切，应等 tj-data 设计。



12. 版本策略

12.1 0.x 阶段

datamodel 是底层包，字段变更会影响多个上层包。

0.x 阶段，上层包应锁定 minor 版本：

dependencies = [
  "tj-datamodel>=0.1,<0.2"
]

如果 tj-datamodel 发布 0.2.0 并包含破坏性变更，上层包应显式适配后再升级依赖范围。

12.2 1.x 阶段

稳定后遵守语义化版本：

dependencies = [
  "tj-datamodel>=1.0,<2.0"
]

12.3 向后兼容原则

尽量避免：





删除字段。



修改字段含义。



修改枚举值字符串。



改变默认值。

新增字段时优先给默认值。



13. 项目结构建议

tj-datamodel/
  README.md
  pyproject.toml
  LICENSE
  src/
    tj_datamodel/
      __init__.py
      enums.py
      models.py
      errors.py
      validators.py
  tests/
    test_enums.py
    test_models.py
    test_imports.py

模块职责：

enums.py       公共枚举
models.py      公共 dataclass 模型
errors.py      基础异常
validators.py  可选轻量校验，MVP 可为空或暂不提供



14. Python API 示例

14.1 Symbol

from tj_datamodel import Symbol, Exchange, Market, AssetType

symbol = Symbol(
    code="600519",
    exchange=Exchange.SSE,
    suffix="SH",
    market=Market.CN_A_SHARE,
    asset_type=AssetType.STOCK,
    normalized="600519.SH",
)

14.2 Bar

from datetime import date
from tj_datamodel import Bar, Frequency, AdjustType

bar = Bar(
    symbol="600519.SH",
    trade_date=date(2026, 8, 4),
    open=1800.0,
    high=1820.0,
    low=1780.0,
    close=1810.0,
    volume=1234567,
    amount=2234567890.0,
    frequency=Frequency.DAILY,
    adjust=AdjustType.NONE,
)

14.3 ReturnPoint

from datetime import date
from tj_datamodel import ReturnPoint

point = ReturnPoint(
    trade_date=date(2026, 8, 4),
    value=0.0123,
    symbol="600519.SH",
)

14.4 EquityPoint

from datetime import date
from tj_datamodel import EquityPoint

point = EquityPoint(
    trade_date=date(2026, 8, 4),
    value=1.0235,
)



15. README 建议

README 首屏：

# Tianji DataModel

Shared data models and type definitions for the Tianji market research toolkit.

Tianji DataModel is a lightweight internal foundation package used by Tianji projects such as tj-symbols, tj-data, tj-factors, tj-metrics, and tj-backtest.
Most users do not need to install it directly.

核心说明：

## Design Goals

- Shared data models for Tianji packages
- Lightweight and dependency-free
- Standard-library dataclasses and enums
- No data fetching, no calculations, no business logic
- Stable type contracts for upper-level packages

用户提示：

## Installation

You usually do not need to install this package directly.
It is installed automatically when you install upper-level Tianji packages.



16. 测试策略

16.1 枚举测试





枚举值字符串稳定。



枚举可作为字符串使用。



枚举导入路径稳定。

16.2 模型测试





Symbol 可正常构造。



Bar 可正常构造。



ReturnPoint 可正常构造。



EquityPoint 可正常构造。



dataclass 不可变性生效。

16.3 导入测试

确保用户可以从顶层导入：

from tj_datamodel import Symbol, Bar, ReturnPoint, EquityPoint
from tj_datamodel import Market, Exchange, AssetType, Frequency, AdjustType



17. 后续版本规划

v0.1.0





基础枚举：





Market



Exchange



AssetType



Currency



Frequency



AdjustType



基础模型：





Symbol



Bar



ReturnPoint



EquityPoint



基础异常：





TianjiDataModelError



ValidationError



零重依赖。



无 CLI。

v0.2.0

根据 tj-data、tj-factors、tj-backtest 的实际需要，考虑增加：





Quote



FactorPoint



轻量 validators



序列化辅助方法

v0.3.0+

根据回测模块设计，考虑增加：





Side



OrderType



OrderStatus



Trade



Order



Position

但只有在 tj-backtest 设计稳定后再加入。



18. 最终决策摘要





tj-datamodel 是 Tianji 生态的共享数据模型基础包。



它不是普通用户主动安装的产品，而是上层包的依赖。



用户安装 tj-metrics、tj-symbols、tj-backtest 等包时会自动安装它。



tj-datamodel 不提供 CLI。



MVP 使用标准库 dataclass(frozen=True) 和 Enum，保持零重依赖。



MVP 不依赖 pandas、numpy、pydantic、requests、AkShare、Tushare。



MVP 包含枚举：Market、Exchange、AssetType、Currency、Frequency、AdjustType。



MVP 包含模型：Symbol、Bar、ReturnPoint、EquityPoint。



MVP 不包含 CalendarInfo。



tj-calendar v0.1.0 暂不依赖 tj-datamodel，但 market 字符串与 datamodel 枚举值保持兼容。



SymbolFormatInfo 不放入 tj-datamodel，它属于 tj-symbols 的格式注册表。



Bar.symbol 使用 Tianji 标准格式字符串，例如 600519.SH，不嵌套 Symbol 对象。



ReturnPoint.value 使用小数表示收益率，例如 0.0123 表示 1.23%。



暂不提前设计 Order、Trade、Position、Portfolio、Account 等回测交易模型。



后续模型必须由实际上层项目需求驱动，避免 tj-datamodel 变成大杂烩。


