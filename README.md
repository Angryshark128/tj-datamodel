[![PyPI version](https://img.shields.io/pypi/v/tj-datamodel?color=4b6ef5&label=pypi)](https://pypi.org/project/tj-datamodel/)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/tj-datamodel?color=4b6ef5)](https://pypi.org/project/tj-datamodel/)
[![CI](https://github.com/Angryshark128/tj-datamodel/actions/workflows/ci.yml/badge.svg)](https://github.com/Angryshark128/tj-datamodel/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# Tianji DataModel

Tianji 生态的共享数据模型，零外部运行时依赖。

Tianji DataModel 是 [Tianji](https://github.com/tianji-dev/tianji) 开源市场研究工具生态的基础约定层，被 tj-symbols / tj-data 等模块复用，保证各包之间的数据格式一致。

## 特性

- 不可变数据模型：`Symbol` / `Bar` / `ReturnPoint` / `EquityPoint`
- 6 个共享枚举：`Market` / `Exchange` / `AssetType` / `Currency` / `Frequency` / `AdjustType`
- 统一异常体系：`TianjiDataModelError` / `ValidationError`
- 校验函数：`validate_symbol` / `validate_bar` / `validate_point_date`
- 离线优先，零外部数据依赖

## 安装

```bash
pip install tj-datamodel
```

## 快速开始

```python
from datetime import date
from tj_datamodel import Exchange, Market, AssetType, Symbol, Bar

s = Symbol(
    code="600519",
    exchange=Exchange.SSE,
    suffix="SH",
    market=Market.CN_A_SHARE,
    asset_type=AssetType.STOCK,
    normalized="600519.SH",
)
s.normalized  # "600519.SH"

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
```

## 开发

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest -q
```

## Tianji 生态

Tianji 是一套面向市场研究的可组合开源工具生态。每个子项目都可以独立使用，也可以组合成完整的市场研究工作流。

- tj-calendar: 离线优先的交易日历
- tj-symbols: 证券代码标准化与格式转换
- tj-data: 市场数据适配与本地缓存
- tj-factors: 技术指标与因子
- tj-metrics: 绩效指标
- tj-backtest: 轻量回测
- tj-research: AI 辅助研究
- tj-terminal: 综合研究工作台

## Disclaimer / 免责声明

This project is for research and educational purposes only.
It does not provide investment advice, trading signals, or financial recommendations.

本项目仅用于研究和教育目的，不构成投资建议、交易信号或金融建议。
