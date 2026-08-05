# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 首个 MVP 版本：Tianji 生态共享数据模型。

## [0.1.0] - 2026-08-04

### Added
- 不可变数据模型：`Symbol` / `Bar` / `ReturnPoint` / `EquityPoint`。
- 6 个共享枚举：`Market` / `Exchange` / `AssetType` / `Currency` / `Frequency` / `AdjustType`。
- 异常体系：`TianjiDataModelError` / `ValidationError`。
- 校验函数：`validate_symbol` / `validate_bar` / `validate_point_date`。
- 零外部运行时依赖。

[Unreleased]: https://github.com/Angryshark128/tj-datamodel/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Angryshark128/tj-datamodel/releases/tag/v0.1.0
