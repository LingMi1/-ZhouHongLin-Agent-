# SimpleAgent 工具调用功能说明

## 概述

SimpleAgent 现在支持工具调用功能，可以让大模型自动识别用户意图并调用预定义的工具完成任务。

## 核心功能

### 1. 计算器工具

提供了四个基础计算工具：

- **calculator_add**: 加法运算
- **calculator_subtract**: 减法运算
- **calculator_multiply**: 乘法运算
- **calculator_divide**: 除法运算

### 2. 工具调用链路

完整的工具调用流程：

1. **意图识别**: 大模型分析用户输入，识别是否需要调用工具
2. **工具选择**: 根据工具描述选择合适的工具
3. **参数提取**: 从用户输入中提取工具所需的参数
4. **工具执行**: 执行选定的工具，获取结果
5. **结果回传**: 将工具执行结果重新送入大模型
6. **自然语言生成**: 大模型基于工具结果生成最终的自然语言回答

### 3. 防止死循环

- 默认最大工具调用次数：10 次
- 可通过 `max_iterations` 参数自定义
- 超过最大次数后自动终止工具调用

## 使用方法

### 基础用法（不启用工具）

```python
from src.zhouhonglin_agent import SimpleAgent

# 创建不启用工具的 Agent（向后兼容）
agent = SimpleAgent(
    system_message="你是一个有帮助的AI助手。"
)

# 进行对话
response = agent.chat("你好！")
print(response)
```

### 启用工具调用

```python
from src.zhouhonglin_agent import SimpleAgent
from src.zhouhonglin_agent.agents.tools import get_calculator_tools

# 创建启用工具的 Agent
agent = SimpleAgent(
    system_message="你是一个有帮助的AI助手。当用户需要进行数学计算时，请使用提供的计算器工具。",
    enable_tools=True,
    max_iterations=5
)

# 注册计算器工具
calculator_tools = get_calculator_tools()
for tool in calculator_tools:
    agent.register_tool(
        name=tool["name"],
        func=tool["func"],
        description=tool["description"],
        parameters=tool["parameters"]
    )

# 进行对话（会自动调用工具）
response = agent.chat("请帮我计算 123 加 456 等于多少？")
print(response)
```

### 自定义工具

```python
from src.zhouhonglin_agent import SimpleAgent

# 创建启用工具的 Agent
agent = SimpleAgent(enable_tools=True)

# 定义自定义工具函数
def custom_tool(param1: str, param2: int) -> str:
    """自定义工具"""
    return f"处理结果: {param1} x {param2}"

# 注册自定义工具
agent.register_tool(
    name="custom_tool",
    func=custom_tool,
    description="这是一个自定义工具，用于处理特定任务。",
    parameters={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "第一个参数"
            },
            "param2": {
                "type": "integer",
                "description": "第二个参数"
            }
        },
        "required": ["param1", "param2"]
    }
)

# 使用工具
response = agent.chat("请使用 custom_tool 处理 'hello' 和 42")
print(response)
```

## API 参考

### SimpleAgent 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | None | 码云 AI API Key |
| `model` | str | None | 使用的模型名称 |
| `system_message` | str | "你是一个有帮助的AI助手..." | 系统提示词 |
| `enable_tools` | bool | False | 是否启用工具调用 |
| `max_iterations` | int | 10 | 最大工具调用次数 |

### register_tool 方法

```python
agent.register_tool(
    name: str,           # 工具名称
    func: Callable,      # 工具函数
    description: str,    # 工具描述（用于大模型理解）
    parameters: Dict     # 工具参数定义（JSON Schema 格式）
)
```

## 测试

### 运行计算器工具测试

```bash
python tests/test_calculator_tool.py
```

### 运行向后兼容性测试

```bash
python tests/test_simple_agent_compatibility.py
```

### 运行工具调用示例

```bash
python examples/02_simple_agent_with_tools.py
```

## 文件结构

```
src/zhouhonglin_agent/
├── agents/
│   ├── tools/
│   │   ├── __init__.py
│   │   └── calculator_tool.py      # 计算器工具实现
│   └── simple_agent.py              # SimpleAgent 实现（已增强）
examples/
├── 01_simple_chat.py                # 基础对话示例（向后兼容）
└── 02_simple_agent_with_tools.py    # 工具调用示例
tests/
├── test_calculator_tool.py          # 计算器工具测试
└── test_simple_agent_compatibility.py  # 向后兼容性测试
```

## 技术实现

### 状态定义

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_action: str
    iterations: int
```

### LangGraph 节点

1. **agent 节点**: 调用大模型，决定是否需要调用工具
2. **tools 节点**: 执行工具调用，返回结果

### 工具调用流程

```
用户输入
    ↓
agent 节点（大模型分析）
    ↓
是否需要工具？
    ├─ 是 → tools 节点（执行工具）
    │        ↓
    │     agent 节点（处理结果）
    │        ↓
    │   是否还需要工具？
    │        ├─ 是 → 循环
    │        └─ 否 → 结束
    └─ 否 → 结束
```

## 注意事项

1. **向后兼容**: 默认不启用工具调用，保持与原有代码的兼容性
2. **API Key**: 需要配置有效的码云 AI API Key 才能使用
3. **工具描述**: 工具描述要清晰准确，帮助大模型理解工具用途
4. **参数验证**: 工具函数内部应该进行参数验证
5. **错误处理**: 工具执行错误会被捕获并传递给大模型

## 扩展建议

1. **添加更多工具**: 可以添加更多类型的工具（如时间、天气、搜索等）
2. **工具组合**: 支持多个工具的组合调用
3. **工具缓存**: 对相同参数的工具调用结果进行缓存
4. **异步工具**: 支持异步工具调用
5. **工具权限**: 添加工具调用权限控制