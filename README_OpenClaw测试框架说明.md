# OpenClaw 真实投研场景测试框架说明

版本：2.0.0  
更新日期：2026-03-11

本说明文件已按最新任务清单同步清理。当前系统仅保留任务清单中仍存在的 20 个案例。

## 当前有效案例数

- 中难度：6 个
- 高难度：12 个
- 极高难度：3 个
- 总计：21 个

## 当前有效案例

### 中难度

| 案例编号 | 场景 | 主要 skill | 预计耗时 |
|---|---|---|---|
| F16 | 股票分析 Skills 个股深度分析 | stock-analysis | 15-20分钟 |
| G2 | 迭代投研框架 | framework-iterator | 20-30分钟 |
| GF1 | PDF 财报读取 + Word 报告生成 | pdf/docx/canvas-design | 15-20分钟 |
| GF2 | PDF 材料自动生成路演 PPT | pdf/pptx | 15-20分钟 |
| GF3 | 金融数据接入 Stock Watcher | stock-watcher | 10-15分钟 |
| GF7 | 技术分析与 K 线图分析 | technical-analyst | 15-20分钟 |

### 高难度

| 案例编号 | 场景 | 主要 skill | 预计耗时 |
|---|---|---|---|
| F8 | Agent 深度研究 | deep-research | 30-60分钟 |
| F9 | 麦肯锡顾问式深度研究 PPT 制作 | mckinsey-consultant | 30-45分钟 |
| F11 | 同花顺 API 接口配置与公告数据提取 | 10jqka-api | 20-30分钟 |
| F12 | 米筐 API 接口配置与高频数据提取 | rqdata-api | 20-30分钟 |
| F13 | Wind API 连接与数据提取 | wind-api | 20-30分钟 |
| F14 | PB-ROE 选股策略构建 | strategy-builder | 30-45分钟 |
| F15 | 杯柄形态选股策略构建 | pattern-recognition | 30-45分钟 |
| G1 | 每日 A 股公告信息汇总及定时发送 | announcement-aggregator | 30-45分钟 |
| G3 | 个股投研分析助手 | stock-research-assistant | 30-45分钟 |
| G5 | 阿里巴巴专属自动化监控早报 | stock-analysis/agent-browser/email/cron | 20-35分钟 |
| T2 | 量化跟盘及盘前预警盘后总结 | market-monitor | 30-45分钟 |
| T3 | 数据库自动更新 | db-updater | 20-30分钟 |

### 极高难度

| 案例编号 | 场景 | 主要 skill | 预计耗时 |
|---|---|---|---|
| F17 | 全自动因子挖掘与回测 | factor-mining | 60-90分钟 |
| G4 | 自动化研报复现 | report-reproduction | 60-90分钟 |
| GF6 | Barra CNE6 因子复杂代码工程实现 | code-engineering | 60-90分钟 |

## 使用方式

```powershell
py -m pip install -e .
py -m openclaw_eval.cli init
py -m openclaw_eval.cli list-cases
py -m openclaw_eval.cli show-case F16
py -m openclaw_eval.cli run F16 --dry-run
```

## 说明

如任务清单再次更新，应以 Excel 中的案例编号为准，同步维护：

- `openclaw_eval/data/cases.json`
- 本说明文件
- `01_调研测试总提示词_SKILL.md`
- 各难度案例提示词文档
