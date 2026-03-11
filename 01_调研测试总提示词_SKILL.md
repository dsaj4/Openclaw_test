# OpenClaw 投研场景调研测试总提示词 / 测评Skill

## Skill 基本信息
- **名称**: OpenClaw投研场景调研测试框架
- **版本**: 1.0.0
- **描述**: 系统化测试OpenClaw在金融投研场景中的应用能力，自动管理工作空间、监控测试过程、记录性能指标
- **作者**: 投研测试团队
- **创建日期**: 2026-03-11

---

## 核心功能

### 1. 工作空间管理

```yaml
workspace_structure:
  root: "/workspace/openclaw_research_test"
  subdirectories:
    - "skills/"           # 存放所有安装的skill
    - "scripts/"          # 存放监控脚本和工具脚本
    - "outputs/"          # 存放所有测试输出结果
    - "outputs/reports/"  # 结构化测试报告
    - "outputs/logs/"     # 执行日志
    - "outputs/data/"     # 测试生成的数据文件
    - "temp/"             # 临时文件
    - "docs/"             # 文档和参考资料
```

### 2. 主Agent职责

作为主Agent，你的核心职责是：

1. **测试协调**: 监控和指示subagent完成各项测试任务
2. **资源管理**: 确保工作空间整洁、skill正确安装
3. **性能监控**: 收集每次测试的token用量、执行时间、交互次数
4. **结果汇总**: 将测试结果整理为结构化文本并存入工作空间
5. **质量控制**: 验证测试完成度，确保输出符合预期

### 3. 测试执行流程

```
┌─────────────────────────────────────────────────────────────┐
│                    测试执行标准流程                          │
├─────────────────────────────────────────────────────────────┤
│  Step 1: 初始化监控脚本                                      │
│     └── 启动token/时间/交互次数记录器                         │
│                                                             │
│  Step 2: 检查并安装所需Skill                                 │
│     └── 从ClawHub或指定来源安装skill                         │
│     └── 验证skill安装成功                                    │
│                                                             │
│  Step 3: 执行测试任务                                        │
│     └── 按照案例提示词执行具体操作                           │
│     └── 实时记录执行日志                                     │
│                                                             │
│  Step 4: 收集性能指标                                        │
│     └── 获取token用量、执行时间、交互轮数                    │
│                                                             │
│  Step 5: 生成结构化测试报告                                  │
│     └── 整理输出结果、截图、文件                             │
│     └── 保存至工作空间指定目录                               │
│                                                             │
│  Step 6: 质量评估与反馈                                      │
│     └── 评估任务完成度（完全完成/部分完成/失败）             │
│     └── 记录遇到的问题和改进建议                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 监控脚本规范

### Token/时间/交互监控脚本

```python
# 保存路径: /workspace/openclaw_research_test/scripts/monitor.py
"""
OpenClaw测试性能监控脚本
功能：记录token用量、执行时间、交互次数
"""

import time
import json
from datetime import datetime
from pathlib import Path

class TestMonitor:
    def __init__(self, test_id: str, test_name: str):
        self.test_id = test_id
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
        self.interaction_count = 0
        self.token_usage = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }
        self.log_file = Path(f"/workspace/openclaw_research_test/outputs/logs/{test_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self._log("=" * 60)
        self._log(f"测试开始: {self.test_name}")
        self._log(f"测试ID: {self.test_id}")
        self._log(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log("=" * 60)
        
    def record_interaction(self, tokens_in: int = 0, tokens_out: int = 0):
        """记录一次交互"""
        self.interaction_count += 1
        self.token_usage["input_tokens"] += tokens_in
        self.token_usage["output_tokens"] += tokens_out
        self.token_usage["total_tokens"] += (tokens_in + tokens_out)
        self._log(f"[交互 {self.interaction_count}] Tokens: +{tokens_in}/{tokens_out}")
        
    def _log(self, message: str):
        """写入日志"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
            
    def stop(self) -> dict:
        """停止监控并返回统计结果"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        result = {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "start_time": datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.fromtimestamp(self.end_time).strftime('%Y-%m-%d %H:%M:%S'),
            "duration_seconds": round(duration, 2),
            "duration_formatted": self._format_duration(duration),
            "interaction_count": self.interaction_count,
            "token_usage": self.token_usage
        }
        
        self._log("=" * 60)
        self._log(f"测试结束")
        self._log(f"总耗时: {result['duration_formatted']}")
        self._log(f"交互次数: {self.interaction_count}")
        self._log(f"Token用量: {self.token_usage['total_tokens']} (输入: {self.token_usage['input_tokens']}, 输出: {self.token_usage['output_tokens']})")
        self._log("=" * 60)
        
        # 保存JSON结果
        result_file = Path(f"/workspace/openclaw_research_test/outputs/logs/{self.test_id}_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        return result
    
    def _format_duration(self, seconds: float) -> str:
        """格式化时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

# 使用示例
if __name__ == "__main__":
    monitor = TestMonitor("TEST001", "示例测试")
    monitor.start()
    # ... 执行测试 ...
    monitor.stop()
```

---

## 测试报告模板

### 结构化测试报告格式

```markdown
# 测试报告: {测试场景名称}

## 基本信息
- **测试ID**: {案例编号}
- **测试场景**: {场景描述}
- **主要Skill**: {使用的skill}
- **测试日期**: {日期}
- **测试执行者**: OpenClaw SubAgent

## 性能指标
- **执行时长**: {XX分XX秒}
- **交互次数**: {X} 轮
- **Token用量**: 
  - 输入: {X} tokens
  - 输出: {X} tokens
  - 总计: {X} tokens

## Skill安装情况
- **所需Skill**: {skill名称}
- **安装来源**: {ClawHub/GitHub/本地}
- **安装状态**: ✓ 成功 / ✗ 失败
- **安装耗时**: {XX秒}

## 测试执行过程
### 步骤1: {步骤描述}
- 状态: ✓ 完成 / ✗ 失败 / ⚠ 部分完成
- 输出: {关键输出}

### 步骤2: {步骤描述}
- 状态: ✓ 完成 / ✗ 失败 / ⚠ 部分完成
- 输出: {关键输出}

## 测试结果
- **完成度**: {完全完成/部分完成/失败}
- **输出文件**: 
  - {文件路径1}
  - {文件路径2}
- **输出质量**: {优秀/良好/一般/较差}

## 问题记录
| 问题类型 | 问题描述 | 严重程度 | 解决方案 |
|---------|---------|---------|---------|
| {类型} | {描述} | {高/中/低} | {方案} |

## 改进建议
1. {建议1}
2. {建议2}

## 总体评价
{综合评价内容}

## 附件
- 执行日志: `{日志文件路径}`
- 输出结果: `{结果文件路径}`
```

---

## 主Agent指令模板

### 启动测试指令

```
作为OpenClaw投研测试主Agent，请按照以下流程执行测试：

【测试信息】
- 测试场景: {场景名称}
- 案例编号: {编号}
- 主要Skill: {skill名称}
- 难度等级: {难度}
- 预计耗时: {预计时间}

【执行步骤】

Step 1 - 初始化监控
1. 创建工作空间目录结构（如不存在）
2. 初始化性能监控脚本
3. 启动监控记录器

Step 2 - Skill准备
1. 检查所需skill是否已安装
2. 如未安装，从指定来源安装
3. 验证skill功能正常

Step 3 - 执行测试
1. 读取对应案例的详细提示词
2. 按照提示词指示完成任务
3. 实时记录执行过程

Step 4 - 收集结果
1. 停止监控脚本
2. 收集性能指标
3. 整理所有输出文件

Step 5 - 生成报告
1. 按照测试报告模板生成结构化报告
2. 将报告保存至 outputs/reports/ 目录
3. 汇总关键发现

【输出要求】
- 所有中间产物放入工作空间对应目录
- 生成Markdown格式的测试报告
- 返回测试完成摘要
```

---

## 工作空间初始化指令

```bash
# 创建工作空间目录结构
mkdir -p /workspace/openclaw_research_test/{skills,scripts,outputs/{reports,logs,data},temp,docs}

# 创建监控脚本
cat > /workspace/openclaw_research_test/scripts/monitor.py << 'EOF'
[上述监控脚本内容]
EOF

# 设置权限
chmod +x /workspace/openclaw_research_test/scripts/monitor.py

# 创建测试报告模板
cat > /workspace/openclaw_research_test/docs/report_template.md << 'EOF'
[上述报告模板内容]
EOF

echo "工作空间初始化完成！"
```

---

## 与其他Skill的协作

### 依赖Skill
- `file-manager`: 文件操作
- `memory`: 长期记忆管理
- `cron`: 定时任务（用于自动化测试）

### 可选Skill
- `docx`: 生成Word格式报告
- `xlsx`: 生成Excel统计表
- `canvas-design`: 生成测试数据可视化图表

---

## 使用示例

### 示例1: 启动完整测试流程

```
请作为测试主Agent，启动案例编号F1的测试：
- 场景: 浏览器检索热点新闻信息
- 主要Skill: agent-browser
- 难度: 低

请按照测试总提示词的流程执行，并生成完整的测试报告。
```

### 示例2: 批量执行多个测试

```
请批量执行以下测试案例：
1. F1 - 浏览器检索热点新闻信息
2. F2 - 查询并安装热门skills
3. F4 - 本地文件管理与信息检索

为每个案例生成独立的测试报告，最后汇总生成批量测试总结报告。
```

---

## 注意事项

1. **数据安全**: 所有测试数据保存在本地工作空间，不上传云端
2. **资源清理**: 测试完成后可选择性清理temp目录下的临时文件
3. **错误处理**: 遇到安装失败或执行错误时，记录详细错误信息
4. **版本记录**: 记录测试时使用的OpenClaw版本和skill版本
5. **可重复性**: 确保测试流程可重复执行，结果可追溯

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| 1.0.0 | 2026-03-11 | 初始版本，包含31个测试案例框架 |

---

## 附录: 测试案例索引

### 低难度案例 (4个)
- F1: 浏览器检索热点新闻信息
- F2: 查询并安装热门skills
- F4: 本地文件管理与信息检索
- F5: 自动化任务提醒

### 中难度案例 (13个)
- F3, F6, F7, F10, F16, G2, GF1-GF5, GF7, T1

### 高难度案例 (11个)
- F8, F9, F11-F15, G1, G3, T2, T3

### 极高难度案例 (3个)
- F17: 全自动因子挖掘与回测
- G4: 自动化研报复现
- GF6: Barra CNE6因子复杂代码工程实现
