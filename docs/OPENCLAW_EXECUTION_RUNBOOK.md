# OpenClaw 执行运行手册

本手册是给 OpenClaw 和操作者共同使用的标准流程。目标不是“理解大意”，而是“按顺序执行，不跳步，不漏检”。

## 一、总原则

1. 先初始化，再选案例，再查 skill，再跑 dry-run。
2. 没有 `SKILL.md` 和 `manifest.json` 的 skill，一律视为未完整安装。
3. 没有 dry-run 报告，不允许声称案例已具备执行条件。
4. 案例是否能真实执行，以报告中的 skill readiness 为准，而不是主观判断。

## 二、标准执行顺序

### Step 1：安装系统

```powershell
py -m pip install -e .
```

成功标准：
- CLI 可以被 `py -m openclaw_eval.cli` 调用。

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
- 明确选择一个案例 ID，例如 `F1`、`GF4`、`G4`

### Step 4：查看案例要求

```powershell
py -m openclaw_eval.cli show-case F1
```

必须读清楚：
- `required_skills`
- `success_criteria`
- `output_artifacts`
- `prompt_source`

### Step 5：检查 skill 是否完整安装

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

如需补齐，可复制模板：

```text
workspace/docs/skill_template/SKILL.md
workspace/docs/skill_template/manifest.json
```

### Step 6：运行就绪性评测

```powershell
py -m openclaw_eval.cli run F1 --dry-run
```

成功标准：
- 生成 JSON 报告
- 生成 Markdown 报告

输出位置：
- `workspace/outputs/reports/f1.json`
- `workspace/outputs/reports/f1.md`

### Step 7：读取报告并做决策

如果报告中出现以下情况：

- `available: false`
  说明 skill 未安装或安装不完整
- `status: dry-run`
  说明本次是准备度检查，不是实际任务执行
- `skill_readiness < 100`
  说明当前不应直接进入真实执行

决策规则：
- skill 不完整：先补 skill
- skill 完整：进入真实任务执行阶段

## 三、OpenClaw 必须遵守的口径

OpenClaw 在回答“能否执行某案例”时，必须按以下口径：

1. 先说明是否已经完成 `init`
2. 再说明案例依赖了哪些 skill
3. 再说明这些 skill 是否完整安装
4. 最后引用 dry-run 报告给出结论

不允许直接跳到“可以执行”。

## 四、推荐命令顺序

```powershell
py -m pip install -e .
py -m openclaw_eval.cli init
py -m openclaw_eval.cli list-cases
py -m openclaw_eval.cli show-case F1
py -m openclaw_eval.cli run F1 --dry-run
```
