# 🔧 Tool Use Agent 功能完成！

基于 Agentic Design Patterns 的 **Tool Use（工具使用）** 设计模式，为你创建了一个完整的、可用的 Tool Use Agent 系统！

## ✅ 已完成的功能

### 1. 核心实现 🔧

**文件**: `src/zhouhonglin_agent/agents/tool_use_agent.py`

创建了完整的 Tool Use Agent 实现：
- ✅ `ToolUseAgent` 核心类
- ✅ `ToolDefinition` 工具定义类
- ✅ `ToolParameter` 参数定义类
- ✅ `ToolExecutionResult` 执行结果类
- ✅ `ToolType` 工具类型枚举
- ✅ 智能工具选择和参数推理
- ✅ 工具执行结果处理
- ✅ 工具链式调用支持
- ✅ 详细的执行追踪和日志
- ✅ 错误处理和重试机制

### 2. 预定义工具库 🛠️

**文件**: `src/zhouhonglin_agent/tools/predefined_tools.py`

实现了 **6大类20+个实用工具**：

#### 📁 文件操作工具 (FileOperationTools)
1. **read_file** - 读取文件内容
2. **write_file** - 写入文件内容
3. **list_directory** - 列出目录内容
4. **file_exists** - 检查文件是否存在
5. **get_file_info** - 获取文件详细信息
6. **delete_file** - 删除文件

#### 🌐 网络请求工具 (NetworkTools)
1. **http_get** - 发送HTTP GET请求
2. **http_post** - 发送HTTP POST请求
3. **ping_host** - Ping网络主机

#### 📊 数据处理工具 (DataProcessingTools)
1. **parse_json** - 解析JSON字符串
2. **parse_csv** - 解析CSV内容
3. **filter_data** - 过滤数据
4. **sort_data** - 排序数据
5. **aggregate_data** - 聚合数据统计

#### 💻 系统信息工具 (SystemInfoTools)
1. **get_system_info** - 获取系统基本信息
2. **get_cpu_info** - 获取CPU信息
3. **get_memory_info** - 获取内存信息
4. **get_disk_info** - 获取磁盘信息
5. **get_process_list** - 获取进程列表

#### 🧮 计算工具 (CalculationTools)
1. **basic_math** - 基础数学计算
2. **statistics_calc** - 统计计算
3. **unit_conversion** - 单位转换

#### 📝 文本处理工具 (TextProcessingTools)
1. **text_analysis** - 文本分析
2. **text_search_replace** - 文本搜索替换
3. **text_extract_pattern** - 提取文本模式
4. **text_hash** - 计算文本哈希
5. **text_format** - 文本格式化

### 3. Web API 接口 🌐

**文件**: `src/zhouhonglin_agent/web_app.py`

添加了完整的 API 端点：

#### POST `/api/tool-use/execute`
执行Tool Use请求
- 智能分析用户需求
- 自动选择合适工具
- 支持多轮工具调用
- 返回完整执行结果

#### POST `/api/tool-use/execute/stream`
流式执行Tool Use请求
- 实时返回执行进度
- Server-Sent Events (SSE) 格式
- 更好的用户体验

#### POST `/api/tool-use/execute-tool`
执行单个工具
- 直接调用指定工具
- 传入具体参数
- 适合精确控制

#### GET `/api/tool-use/tools`
获取可用工具列表
- 支持按工具类型过滤
- 返回工具详细信息
- 包含参数和示例

#### GET `/api/tool-use/history`
获取工具执行历史
- 详细执行记录
- 统计分析数据
- 性能监控信息

#### DELETE `/api/tool-use/history`
清除工具执行历史

#### GET `/api/tool-use/scenarios`
获取Tool Use场景信息
- 预定义使用场景
- 工具类型说明
- 功能特性介绍

### 4. 前端界面 🎨

**文件**: `src/zhouhonglin_agent/static/index.html`

添加了 Tool Use Agent 可视化界面：

- 🔧 **工具类型过滤**：按类型筛选可用工具
- ⚙️ **迭代次数控制**：设置最大执行轮次
- 🚀 **快速场景选择**：预设常用任务模板
- 📝 **任务输入区域**：描述需要完成的任务
- ⚡ **执行模式选择**：支持同步和流式执行
- 📊 **进度可视化**：实时显示执行进度
- 📋 **执行历史**：详细记录每个步骤
- ✅ **结果展示**：美观展示执行结果
- 🛠️ **工具浏览器**：查看所有可用工具
- 📈 **统计面板**：工具使用统计分析

### 5. 使用示例 💡

**文件**: `examples/15_tool_use_agent_demo.py`

创建了完整的使用示例：
- ✅ 基础工具使用演示
- ✅ 复杂任务链式执行演示
- ✅ 不同类型工具演示
- ✅ 统计信息展示
- ✅ 交互式体验模式

## 🚀 如何使用

### 方式1: Python 代码使用

```python
from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.tool_use_agent import ToolUseAgent
from src.zhouhonglin_agent.tools.predefined_tools import PredefinedToolsRegistry

# 初始化
llm_client = GiteeAIClient()
agent = ToolUseAgent(llm_client=llm_client, verbose=True)

# 注册所有预定义工具
PredefinedToolsRegistry.register_all_tools(agent)

# 执行任务
result = await agent.process_request("读取README.md文件内容")

if result["success"]:
    print(f"任务完成！执行了 {result['total_iterations']} 轮")
    for step in result["results"]:
        print(f"- {step['tool_name']}: {step['result']}")
```

### 方式2: Web 界面（推荐）

```bash
python run_web.py
# 访问 http://localhost:8001
# 点击 "🔧 Tool Use Agent" 标签页
```

### 方式3: 命令行演示

```bash
python examples/15_tool_use_agent_demo.py
```

### 方式4: API 调用

```bash
# 执行任务
curl -X POST http://localhost:8001/api/tool-use/execute \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "计算 2^10 + sqrt(144)",
    "max_iterations": 3
  }'

# 获取可用工具
curl http://localhost:8001/api/tool-use/tools

# 获取执行历史
curl http://localhost:8001/api/tool-use/history
```

## 📊 核心优势

### 1. 智能工具选择 🎯
- **自动分析**：智能理解用户需求
- **最优匹配**：选择最合适的工具
- **参数推理**：自动推断工具参数
- **置信度评估**：提供选择理由

### 2. 丰富工具生态 🛠️
- **20+预定义工具**：覆盖6大常用领域
- **易于扩展**：简单添加自定义工具
- **类型分类**：按功能类型组织
- **详细文档**：每个工具都有完整说明

### 3. 强大执行能力 ⚡
- **链式调用**：支持多工具协作
- **异步执行**：高效的并发处理
- **错误恢复**：智能错误处理机制
- **性能监控**：详细的执行统计

### 4. 完整可观测性 📈
- **执行追踪**：记录每个步骤
- **性能分析**：统计执行时间
- **使用统计**：工具使用频率
- **历史记录**：完整执行历史

### 5. 灵活集成方式 🔄
- **Python API**：直接代码调用
- **Web界面**：可视化操作
- **REST API**：HTTP接口调用
- **流式处理**：实时进度反馈

## 🎓 设计模式详解

### Tool Use 模式的核心思想

Tool Use（工具使用）模式的核心是**让AI智能体能够调用外部工具来扩展其能力**，就像人类使用工具来完成复杂任务一样。

#### 传统方式 vs Tool Use 模式

**传统方式**：
```
用户请求 → AI模型 → 文本回复
问题：AI只能生成文本，无法执行实际操作
```

**Tool Use 模式**：
```
用户请求 → 需求分析 → 工具选择 → 工具执行 → 结果整合 → 智能回复
          ↓          ↓         ↓         ↓
      理解意图    选择工具   实际操作   处理结果
```

### 适用场景

✅ **适合使用 Tool Use 的情况**：
- 需要执行实际操作（文件、网络、计算）
- 需要获取实时数据
- 需要与外部系统交互
- 需要执行复杂计算或数据处理
- 需要多步骤任务协作

❌ **不适合使用 Tool Use 的情况**：
- 纯文本生成任务
- 创意写作
- 简单问答
- 不需要外部数据的推理

## 📈 功能对比

### Tool Use Agent vs 其他 Agent

| 特性 | Simple Agent | Tool Agent | RAG Agent | Prompt Chaining | Routing Agent | **Tool Use Agent** |
|------|--------------|------------|-----------|-----------------|---------------|--------------------|
| 工具调用 | ❌ 无 | ✅ 基础 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **智能化** |
| 工具选择 | ❌ 无 | ⚠️ 手动 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **自动化** |
| 多工具协作 | ❌ 无 | ⚠️ 有限 | ❌ 无 | ⚠️ 间接 | ❌ 无 | ✅ **完整支持** |
| 执行追踪 | ❌ 无 | ⚠️ 基础 | ❌ 无 | ✅ 有 | ✅ 有 | ✅ **详细** |
| 工具生态 | ❌ 无 | ⚠️ 有限 | ❌ 无 | ❌ 无 | ❌ 无 | ✅ **丰富** |
| 适用场景 | 简单对话 | 基础工具 | 知识查询 | 复杂流程 | 任务分发 | **实际操作** |

### Tool Use vs Tool Agent 的区别

| 维度 | Tool Agent | Tool Use Agent |
|------|------------|----------------|
| 核心思想 | 预定义工具调用 | 智能工具选择和执行 |
| 工具选择 | 手动指定 | AI自动选择 |
| 参数处理 | 手动提供 | AI自动推理 |
| 执行方式 | 单一工具 | 多工具协作 |
| 适用复杂度 | 简单任务 | 复杂任务链 |
| 示例 | 调用天气API | 分析需求→选择工具→执行→整合结果 |

## 🔥 实际应用场景

### 场景1: 数据分析助手

```python
# 用户：分析sales.csv文件中的销售数据
# 系统自动执行：
agent.process_request("分析sales.csv文件中的销售数据")
# 1. read_file - 读取CSV文件
# 2. parse_csv - 解析CSV数据
# 3. aggregate_data - 按产品聚合销售额
# 4. statistics_calc - 计算平均值和总和
```

### 场景2: 系统运维助手

```python
# 用户：检查服务器状态并生成报告
# 系统自动执行：
agent.process_request("检查服务器状态并生成报告")
# 1. get_system_info - 获取系统信息
# 2. get_cpu_info - 获取CPU状态
# 3. get_memory_info - 获取内存状态
# 4. write_file - 生成状态报告
```

### 场景3: 文档处理助手

```python
# 用户：统计所有.md文件的字数
# 系统自动执行：
agent.process_request("统计当前目录所有.md文件的字数")
# 1. list_directory - 列出目录文件
# 2. read_file - 逐个读取.md文件
# 3. text_analysis - 分析每个文件字数
# 4. statistics_calc - 计算总字数
```

### 场景4: 网络监控助手

```python
# 用户：检查网站列表的可用性
# 系统自动执行：
agent.process_request("检查百度、谷歌、GitHub的网站可用性")
# 1. ping_host - 测试百度连通性
# 2. http_get - 检查谷歌HTTP状态
# 3. ping_host - 测试GitHub连通性
# 4. aggregate_data - 汇总可用性报告
```

## 💡 最佳实践

### 1. 工具设计原则

✅ **单一职责**：
- 每个工具只做一件事
- 功能边界清晰
- 避免工具重叠

✅ **参数简洁**：
- 必需参数尽量少
- 提供合理默认值
- 参数类型明确

✅ **错误处理**：
- 详细的错误信息
- 优雅的失败处理
- 提供恢复建议

### 2. 任务描述技巧

```python
# ✅ 好的任务描述
"读取config.json文件并解析其中的数据库配置"
"计算数组 [1,2,3,4,5] 的平均值和标准差"
"获取系统CPU使用率并检查是否超过80%"

# ❌ 不好的任务描述
"处理文件"  # 太模糊
"做计算"    # 不明确
"检查系统"  # 范围太广
```

### 3. 性能优化

```python
# 1. 合理设置最大迭代次数
agent.process_request(task, max_iterations=3)  # 简单任务
agent.process_request(task, max_iterations=10) # 复杂任务

# 2. 使用工具类型过滤
tools = agent.get_available_tools(tool_type=ToolType.FILE_OPERATION)

# 3. 定期清理历史记录
agent.clear_history()
```

### 4. 错误处理

```python
# 始终检查执行结果
result = await agent.process_request(user_input)
if result["success"]:
    # 处理成功结果
    for step in result["results"]:
        if step["success"]:
            print(f"✅ {step['tool_name']}: {step['result']}")
        else:
            print(f"❌ {step['tool_name']}: {step['error_message']}")
else:
    # 处理失败情况
    print(f"任务失败: {result['message']}")
```

## 🔧 自定义工具

### 添加新工具

```python
# 1. 定义工具函数
def my_custom_tool(param1: str, param2: int = 10) -> str:
    """我的自定义工具"""
    return f"处理 {param1} 使用参数 {param2}"

# 2. 注册为工具
agent.register_function_as_tool(
    func=my_custom_tool,
    name="custom_tool",
    description="执行自定义操作",
    tool_type=ToolType.CUSTOM,
    examples=["处理数据", "自定义操作"],
    tags=["自定义", "示例"]
)

# 3. 使用工具
result = await agent.process_request("使用自定义工具处理数据")
```

### 创建工具类

```python
class MyToolSet:
    @staticmethod
    def tool1(input_data: str) -> str:
        return f"工具1处理: {input_data}"
    
    @staticmethod
    def tool2(value: float) -> float:
        return value * 2

# 批量注册
for method_name in dir(MyToolSet):
    if not method_name.startswith('_'):
        method = getattr(MyToolSet, method_name)
        if callable(method):
            agent.register_function_as_tool(method)
```

## 📝 配置示例

### 工具类型配置

```python
# 只使用文件操作工具
file_tools = agent.get_available_tools(tool_type=ToolType.FILE_OPERATION)

# 只使用计算工具
calc_tools = agent.get_available_tools(tool_type=ToolType.CALCULATION)

# 获取所有工具
all_tools = agent.get_available_tools()
```

### 执行参数配置

```python
# 配置不同复杂度的任务
simple_task = await agent.process_request("计算1+1", max_iterations=1)
complex_task = await agent.process_request("分析数据并生成报告", max_iterations=10)
```

## 🔧 扩展功能

### 可以添加的功能：

- [ ] 工具依赖管理（工具A依赖工具B）
- [ ] 工具权限控制（某些工具需要授权）
- [ ] 工具版本管理（支持工具升级）
- [ ] 工具性能监控（执行时间、成功率）
- [ ] 工具推荐系统（基于历史使用推荐）
- [ ] 工具组合模板（预定义工具组合）
- [ ] 异步工具执行（并行执行多个工具）
- [ ] 工具结果缓存（避免重复执行）
- [ ] 工具执行沙箱（安全隔离）
- [ ] 工具市场（社区贡献工具）

## 📚 相关资源

### 项目文档
- 主文档：`README.md`
- Web 界面指南：`docs/web_interface.md`
- API 参考：`docs/api_reference.md`

### 外部参考
- **原理文章**: [Agentic Design Patterns - Tool Use](https://github.com/ginobefun/agentic-design-patterns-cn/blob/main/11-Chapter-05-Tool-Use.md)

## 🎉 开始使用！

```bash
# 启动 Web 界面体验完整功能
python run_web.py

# 或运行命令行演示
python examples/15_tool_use_agent_demo.py

# 或在你的代码中使用
from src.zhouhonglin_agent.agents.tool_use_agent import ToolUseAgent
```

## 📞 反馈和问题

如有任何问题或建议，欢迎：
- 查看文档: `TOOL_USE_AGENT_FEATURES.md`（本文件）
- 查看示例: `examples/15_tool_use_agent_demo.py`
- 运行演示: `python examples/15_tool_use_agent_demo.py`

---

**🎊 恭喜！你现在拥有了一个功能完整的 Tool Use Agent 系统！**

通过智能工具选择和执行，让你的应用能够完成各种实际操作任务，从简单的文件处理到复杂的数据分析，大大扩展了AI的实用能力！🚀
