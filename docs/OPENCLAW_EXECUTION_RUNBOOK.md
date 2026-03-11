# OpenClaw 执行运行手册

本手册的目标不是“让 OpenClaw 大概知道要做什么”，而是要求它严格按顺序执行，并且不得用 Markdown 说明文档冒充真实 skill 产物。

## 一、强制原则

1. 先初始化，再选案例，再查 skill，再跑 dry-run。
2. 没有 `SKILL.md` 和 `manifest.json` 的 skill，一律视为未完整安装。
3. skill 需要配置时，未配置完成前一律视为不可执行。
4. 没有 dry-run 报告，不允许声称案例已具备执行条件。
5. 报告、摘要、说明文档都不能替代真实产物。
6. 案例要求 `docx/pptx/xlsx/mp4/csv/json` 时，必须产出对应格式文件，不能降级成 `md`。
7. 未安装 skill 时，必须先安装 skill；不得用通用文本能力模拟 skill 执行。
8. 未配置 skill 时，必须先完成配置；不得跳过配置直接声称“可执行”。

## 二、标准执行顺序

### Step 1：安装系统

```powershell
py -m pip install -e .
```

成功标准：
- CLI 可以被 `py -m openclaw_eval.cli` 调用

### Step 2：初始化工作区

```powershell
py -m openclaw_eval.cli init
```

成功标准：
- 已创建 `workspace/skills/`
- 已创建 `workspace/outputs/reports/`
- 已创建 `workspace/docs/skill_template/`

### Step 3：查看案例列表

```powershell
py -m openclaw_eval.cli list-cases
```

动作要求：
- 明确选择一个案例 ID，例如 `F16`、`GF2`、`G4`

### Step 4：查看案例要求

```powershell
py -m openclaw_eval.cli show-case F16
```

必须读清楚：
- `required_skills`
- `success_criteria`
- `output_artifacts`
- `prompt_source`
- `output_rules`

### Step 5：检查 skill 是否完整安装并确认配置

对每个 `required_skills` 执行检查：

```text
workspace/skills/<slug>/
  SKILL.md
  manifest.json
```

判定规则：
- 三者齐全：已安装
- 只有目录：未完整安装
- 缺目录：未安装
- 有目录也有文件，但缺必要配置：未就绪

对每个 skill 继续执行：

```powershell
py -m openclaw_eval.cli show-skill <slug>
```

必须确认：
- `config_required`
- `required_config`

如需补齐，可复制模板：

```text
workspace/docs/skill_template/SKILL.md
workspace/docs/skill_template/manifest.json
```

### Step 6：运行就绪性评测

```powershell
py -m openclaw_eval.cli run F16 --dry-run
```

成功标准：
- 生成 JSON 报告
- 生成 Markdown 报告

输出位置：
- `workspace/outputs/reports/f16.json`
- `workspace/outputs/reports/f16.md`

### Step 7：读取报告并做决策

如报告中出现以下情况：

- `available: false`
  说明 skill 未安装或安装不完整
- `config_required: true` 且配置未完成
  说明 skill 未就绪
- `status: dry-run`
  说明本次是准备度检查，不是实际任务执行
- `skill_readiness < 100`
  说明当前不应直接进入真实执行
- 案例目标产物是 `pptx/docx/xlsx/mp4/csv/json`，但实际只生成了 `md`
  说明任务失败或被降级执行，不能算完成

决策规则：
- skill 不完整：先安装或补齐 skill
- skill 未配置：先补配置
- skill 完整且已配置：进入真实任务执行阶段

## 三、真实产物强制规则

1. 如果案例目标是 `DOCX`，必须生成 `.docx` 文件。
2. 如果案例目标是 `PPTX`，必须生成 `.pptx` 文件。
3. 如果案例目标是 `XLSX`，必须生成 `.xlsx` 文件。
4. 如果案例目标是 `MP4`，必须生成 `.mp4` 文件。
5. 如果案例目标是 `CSV/JSON`，必须生成对应数据文件。
6. `Markdown` 仅能作为辅助说明、执行记录或摘要，不能冒充主产物。
7. “我本来可以生成”不算完成，“我写了一个说明文件”也不算完成。
8. 未调用真实 skill、未安装 skill、未配置 skill 时，不允许用通用文本能力替代。

## 四、安装与配置要求

OpenClaw 对案例进行真实执行前，必须先给出：

1. 需要安装的 skills 列表
2. 每个 skill 是否已安装
3. 每个 skill 的配置要求
4. 哪些配置尚未完成
5. 安装完成后才能进入真实执行

结论格式必须是二选一：
- `可进入真实执行`
- `需先补齐 skill / 配置`

## 五、推荐命令顺序

```powershell
py -m pip install -e .
py -m openclaw_eval.cli init
py -m openclaw_eval.cli list-cases
py -m openclaw_eval.cli show-case F16
py -m openclaw_eval.cli show-skill stock-analysis
py -m openclaw_eval.cli run F16 --dry-run
```
