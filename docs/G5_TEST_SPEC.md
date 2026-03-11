# G5 测试规范

## 测试名称

G5 阿里巴巴专属自动化监控早报

## 测试目标

验证 OpenClaw 能否为阿里巴巴建立一个完整的自动化监控任务，并在测试模式下于 2026 年 3 月 11 日 18:18（Asia/Shanghai）自动完成以下流程：

1. 盘面数据监控
2. 定向网络搜索
3. Markdown 早报生成
4. 邮件发送

## 任务定义

OpenClaw 必须建立一个专属自动化任务，执行频率为：

- 测试模式
- 一次性执行
- 触发时间：2026-03-11 18:18（Asia/Shanghai）

## 必要依赖

- `stock-analysis`
- `agent-browser`
- `email`
- `cron`

## 配置要求

至少需要以下运行时配置：

- `recipient_email`
- `email_username`
- `email_password`
- `smtp_host`
- `smtp_port`
- `schedule_timezone`

## 强制执行步骤

### Step 1：盘面数据监控

抓取以下任一标的：

- 美股 `BABA`
- 或港股 `09988`

必须提取：

- 最新收盘价
- 成交量
- 涨跌幅

保存到：

- `outputs/data/G5_market_snapshot.json`

特殊规则：

- 如果涨跌幅绝对值大于 3%，则最终 Markdown 报告开头必须出现显著异动警报

### Step 2：定向网络搜索

必须使用联网浏览器在过去 24 小时范围内检索以下主题：

1. `阿里云` 或 `Alibaba Cloud`
2. `通义千问`
3. `AI Agent` 或 `智能体应用`

要求：

- 去重
- 排除自媒体八卦
- 排除纯重复通稿
- 最终仅保留 3 条最有战略价值的资讯

每条资讯必须包含：

- 标题
- 原始链接
- 50 字以内技术或商业洞察

保存到：

- `outputs/data/G5_news_digest.json`

### Step 3：生成极简早报

生成 Markdown 格式早报：

- 标题格式必须严格为：
  `【阿里早报】YYYY-MM-DD：BABA盘面追踪与云/AI生态动态`

报告必须包含：

1. 盘面摘要
2. 异动警报（如触发）
3. 三条核心资讯
4. 每条资讯的原始链接
5. 每条资讯的简短洞察

保存到：

- `outputs/data/G5_aliyun_morning_brief.md`

### Step 4：邮件发送

使用 email skill 将最终早报发送到运行时配置中的目标邮箱。

保存发送结果到：

- `outputs/data/G5_email_send_log.json`

发送成功后，任务的标准回复为：

`老板，今日阿里专属早报已发送。`

## 通过标准

1. 2026-03-11 18:18（Asia/Shanghai）的一次性自动化任务已配置
2. 市场快照文件存在
3. 新闻摘要文件存在
4. Markdown 早报存在
5. 邮件发送日志存在且显示成功

## 失败标准

1. 未创建 2026-03-11 18:18（Asia/Shanghai）的一次性调度
2. 只生成 Markdown，没有独立结构化数据文件
3. 没有发送邮件
4. 保留了低价值八卦或重复通稿
5. 没有给出原始链接
