# Contributing to Tianji DataModel

感谢您对 Tianji DataModel 的关注！我们欢迎任何形式的贡献：报告问题、改进文档、修复 bug、新增特性。

## 开发环境

```bash
# 克隆并进入项目
git clone https://github.com/Angryshark128/tj-datamodel.git
cd tj-datamodel

# 安装依赖（含 dev 组：ruff / pyright / pytest）
uv sync --group dev

# 安装 pre-commit 钩子
uv run pre-commit install
```

## 本地开发

```bash
# 代码检查（CI 中失败会阻断）
uv run ruff check .

# 代码格式化
uv run ruff format --check .

# 类型检查
uv run pyright

# 测试
uv run pytest -q
```

提交前请确保以上四项全部通过。pre-commit 钩子会按 `ruff check → ruff format → pyright` 顺序执行。

## 代码规范

- Python >= 3.10
- 单行最大长度 120 字符（ruff 默认）
- 核心包保持轻量：不默认安装 pandas / numpy / pyarrow / akshare / LLM SDK
- 数据模型用 `frozen=True` 的 dataclass，保持不可变
- 枚举使用 `str, Enum` 双重继承，便于字符串直用与序列化

## 如何提 issue

- Bug 报告：请包含环境信息（Python 版本、包版本、系统）、复现步骤、期望行为与实际行为。
- 特性请求：请描述使用场景和目标，说明为什么需要。

## 如何提 PR

1. 从 `main` 分支新建自己的功能分支。
2. 完成改动并补充测试。
3. 本地通过全部检查（见上文）。
4. 提交 PR，描述变更内容、测试情况。

## 设计约束

- 本包定义生态共享约定（枚举、模型、异常），上游依赖只允许标准库，避免拖入重依赖。
- 变更枚举值或模型字段属于破坏性变更，需走 minor 版本升级并同步 tj-symbols / tj-data 等下游。
- 新增模型请复用现有 `Exchange` / `Frequency` / `AdjustType` 等枚举，不重复定义。

## License

本项目以 [MIT](LICENSE) 协议开源。
