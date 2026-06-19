# 🔗 Prompt Chaining Agent - 快速开始

基于 [Agentic Design Patterns](https://github.com/ginobefun/agentic-design-patterns-cn) 中的 Prompt Chaining 模式实现的智能代理。

## ⚡ 5分钟快速体验

### 1. 最简单的方式 - 运行示例

```bash
# 进入项目目录
cd /Users/zhouhonglin/PycharmProjects/zhouhonglin-agent

# 确保依赖已安装
poetry install

# 运行简单示例（3个场景）
python examples/11_prompt_chaining_simple.py
```

选择一个示例体验：
- **示例1**: 翻译改进链 - 演示基础的链式处理
- **示例2**: 博客文章生成链 - 从标题到完整文章
- **示例3**: 问题解决链 - 系统化的问题分析

### 2. 完整功能体验

```bash
# 运行完整演示（5个实用场景）
python examples/10_prompt_chaining_demo.py
```

可选场景：
- 📄 **文档生成链** - 自动生成技术文档
- 🔍 **代码审查链** - 系统化代码审查
- 🔬 **研究规划链** - 研究问题到计划
- 📖 **故事创作链** - 创意写作工作流
- 💡 **产品分析链** - 产品需求分析

### 3. Web 界面体验

```bash
# 启动 Web 服务
python run_web.py

# 浏览器访问
open http://localhost:8001
```

## 🎯 什么是 Prompt Chaining？

**Prompt Chaining（提示链）** 是一种将复杂任务分解为多个简单步骤的 AI 设计模式。

### 核心理念

```
复杂任务 = 步骤1 → 步骤2 → 步骤3 → ... → 最终结果
```

- 每个步骤专注于一个具体目标
- 前一步的输出是下一步的输入
- 模块化、可控、高质量

### 为什么使用 Prompt Chaining？

| 传统方式 | Prompt Chaining |
|---------|----------------|
| ❌ 一个复杂提示词 | ✅ 多个简单提示词 |
| ❌ 输出质量不稳定 | ✅ 每步都可优化 |
| ❌ 难以调试和改进 | ✅ 清晰的步骤追踪 |
| ❌ 出错就要重来 | ✅ 可从失败步骤继续 |

## 📚 使用示例

### Python 代码示例

```python
from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.prompt_chaining_agent import (
    PromptChainingAgent,
    ChainStep,
    DocumentGenerationChain
)

# 1. 初始化
llm_client = GiteeAIClient()
agent = PromptChainingAgent(llm_client, verbose=True)

# 2. 使用预定义的链
agent.create_chain("doc_gen", DocumentGenerationChain.get_steps())
result = agent.run_chain("doc_gen", "Python 异步编程入门")

# 3. 查看结果
if result.success:
    print(result.final_output)  # 生成的文档
    print(f"耗时: {result.execution_time:.2f}秒")
    
    # 查看每个步骤的输出
    for step in result.intermediate_results:
        print(f"\n步骤 {step['step']}: {step['name']}")
```

### 自定义提示链

```python
# 定义你自己的提示链
steps = [
    ChainStep(
        name="理解需求",
        description="深入理解用户需求",
        prompt_template="请分析以下需求并提取关键要点：{input}"
    ),
    ChainStep(
        name="设计方案",
        description="基于需求设计解决方案",
        prompt_template="基于以下需求分析，设计详细的解决方案：{input}"
    ),
    ChainStep(
        name="实施计划",
        description="制定具体的实施步骤",
        prompt_template="为以下方案制定详细的实施计划：{input}"
    )
]

# 创建并运行
agent.create_chain("custom", steps)
result = agent.run_chain("custom", "我需要一个任务管理系统")
```

## 🛠️ API 使用

### 获取可用链类型

```bash
curl http://localhost:8001/api/prompt-chaining/types
```

### 执行提示链

```bash
curl -X POST http://localhost:8001/api/prompt-chaining/run \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Python 装饰器详解",
    "chain_type": "document_gen",
    "save_result": true
  }'
```

### 流式执行（实时查看进度）

```bash
curl -X POST http://localhost:8001/api/prompt-chaining/run/stream \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "分析这段代码...",
    "chain_type": "code_review",
    "save_result": true
  }'
```

## 🎨 预定义的提示链场景

### 1. 文档生成链 (document_gen)

**用途**: 自动生成专业的技术文档

**步骤**:
1. 生成大纲 - 构建文档结构
2. 撰写内容 - 填充详细内容
3. 添加示例 - 插入代码和案例
4. 优化润色 - 最终优化

**适合**: 技术文档、教程、API文档

### 2. 代码审查链 (code_review)

**用途**: 系统化的代码审查流程

**步骤**:
1. 理解代码 - 分析功能和结构
2. 检查问题 - 识别 bug、性能、安全问题
3. 提出建议 - 具体改进方案
4. 生成报告 - 完整审查报告

**适合**: 代码 Review、质量评估

### 3. 研究规划链 (research)

**用途**: 将研究问题转化为系统化计划

**步骤**:
1. 问题分析 - 深入分析研究问题
2. 文献综述 - 规划调研方向
3. 研究方法 - 设计方法和实验
4. 时间规划 - 制定时间线

**适合**: 学术研究、技术调研、市场分析

### 4. 故事创作链 (story)

**用途**: 创意写作工作流

**步骤**:
1. 构思情节 - 设计故事框架
2. 角色塑造 - 深化角色设定
3. 撰写初稿 - 完成故事初稿
4. 润色完善 - 优化语言表达

**适合**: 创意写作、剧本创作、营销内容

### 5. 产品分析链 (product)

**用途**: 系统化的产品需求分析

**步骤**:
1. 需求理解 - 分析用户痛点
2. 功能设计 - 规划产品功能
3. 技术方案 - 提出技术实现
4. 实施计划 - 制定项目计划

**适合**: 产品规划、需求分析、项目策划

## 📖 完整文档

详细使用指南请查看: [docs/prompt_chaining_guide.md](Prompt Chaining Agent 使用指南.md)

包含：
- ✅ 详细的使用教程
- ✅ 最佳实践建议
- ✅ 实际应用案例
- ✅ 高级功能说明
- ✅ 常见问题解答

## 🎓 学习资源

- **设计模式原理**: [Agentic Design Patterns - Prompt Chaining](https://github.com/ginobefun/agentic-design-patterns-cn/blob/main/07-Chapter-01-Prompt-Chaining.md)
- **示例代码**: 
  - `examples/11_prompt_chaining_simple.py` - 3个简单示例
  - `examples/10_prompt_chaining_demo.py` - 5个完整场景
- **核心实现**: `src/zhouhonglin_agent/agents/prompt_chaining_agent.py`

## 💡 实际应用场景

### 内容创作
- 博客文章生成
- 技术文档撰写
- 营销文案创作

### 代码开发
- 代码审查和改进
- API 文档生成
- 测试用例设计

### 研究分析
- 研究计划制定
- 文献综述生成
- 数据分析报告

### 产品设计
- 需求分析
- 功能规划
- 技术方案设计

## 🚀 开始使用

选择最适合你的方式：

```bash
# 方式1: 快速体验 (推荐新手)
python examples/11_prompt_chaining_simple.py

# 方式2: 完整功能
python examples/10_prompt_chaining_demo.py

# 方式3: Web 界面
python run_web.py
```

## 🤝 反馈和贡献

遇到问题或有建议？欢迎：
- 提交 Issue
- 创建 Pull Request
- 分享你的使用案例

---

**享受 Prompt Chaining 的强大能力！** 🎉

