# 真实 OpenClaw Skill 接入规范

为了让这个评测系统更接近真实 OpenClaw skill 生态，建议所有 skill 都遵循以下最小结构：

```text
workspace/skills/<slug>/
  SKILL.md
  manifest.json
  examples/
```

## manifest.json 建议字段

```json
{
  "slug": "agent-browser",
  "name": "Agent Browser",
  "version": "1.0.0",
  "entry_type": "instructional",
  "install_source": "ClawHub",
  "config_required": false,
  "capabilities": ["search_web", "open_page", "extract_content"],
  "dependencies": []
}
```

## SKILL.md 建议结构

1. 适用场景
2. 输入要求
3. 执行步骤
4. 输出格式
5. 错误处理
6. 示例

## 与当前评测系统的映射关系

- `skills.json` 是平台级注册表
- `workspace/skills/<slug>/manifest.json` 是实例安装信息
- `cases.json` 通过 `required_skills` 声明依赖
- `run` 会同时检查案例依赖和本地安装状态

## 后续可扩展字段

- `auth`
- `pricing`
- `rate_limits`
- `provider`
- `healthcheck`
- `test_prompts`
