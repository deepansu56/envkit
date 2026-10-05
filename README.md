# envkit

一个刻意设计的**小型配置 / 缓存 / 校验工具库**，用来真实验证 Fissue 的完整链路：

抓取 → AI 评测 → 生成验证器 → 沙盒 F2P 验证 → 自动修复提 PR。

## 为什么是「第三个领域」

演示用的 GitHub 仓库不应只有一个。`envkit` 与前两套夹具完全独立：

| 夹具 | 领域 | 考什么 |
|---|---|---|
| `textkit` | 文本处理 | 单函数语义 |
| `ratekit` | 金额 / 费率 | 数值边界 |
| **`envkit`** | **配置 / 缓存 / 校验** | **状态与副作用、环境依赖、输入校验** |

它回答的问题是：

> **当缺陷不再是「算错一个数」，而是「取决于调用顺序或历史状态」、
> 「只在特定环境下成立」、「本该拦住的输入没拦住」时，
> Fissue 还能不能构造出稳定的最小复现、并给出正确的定论？**

## 公开 API

| 函数 / 类 | 说明 |
|---|---|
| `Registry.register(key, factory)` | 注册一个按需构建的组件工厂 |
| `Registry.resolve(key, **kwargs)` | 解析组件（首次构建后缓存） |
| `Registry.snapshot()` | 取注册表的只读快照 |
| `TTLCache(ttl, clock=None)` | 带过期时间的缓存 |
| `load_settings(defaults, env=None)` | 按「环境变量 > 默认值」装载配置 |
| `get_bool(name, default, env=None)` | 从环境变量读布尔 |
| `parse_offset(text)` | 解析 `+08:00` 形式的时区偏移（分钟） |
| `split_iso(text)` | 拆解 ISO-8601 时间戳的各字段 |
| `sanitize_filename(name)` | 把用户输入清洗成安全的文件名 |
| `parse_size(text)` | 解析 `"1.5 MB"` 形式的容量 |
| `parse_port(text)` | 解析并校验端口号 |
| `parse_email(text)` | 解析并校验邮箱（非法输入抛异常） |

## 本地自检

```bash
cd demo/envkit/repo
python -m pytest -q            # 基线应全绿
```

> 基线测试**刻意不覆盖**植入的缺陷路径——缺陷藏在没被覆盖的分支上，
> 逼 Fissue 真正去「读代码 → 写验证器 → 跑 F2P」，而不是抄现成测试。

## 目录

```
demo/envkit/
├── repo/           待推送的测试仓库（独立 git 仓库）
├── fixtures/       15 个 Issue 的内容与元数据
├── scripts/        一键建仓库 / 建 Issue / 建 PR
└── README.md       设计意图与期望结果对照表（见上一级目录）
```
