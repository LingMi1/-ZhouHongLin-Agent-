# 电商智能客服知识库Agent系统

<div align="center">

**基于 RAG 检索增强与 LangGraph Agent 的智能化客服解决方案**

面向电商店铺、品牌官网的智能问答与工具调用客服系统

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com/)

</div>

---

## 📖 项目简介

**电商智能客服知识库Agent系统** 是一款面向电商店铺场景的智能化客服解决方案，基于 RAG（检索增强生成）技术与 LangGraph Agent 框架构建。系统能够自动理解并回答顾客关于商品咨询、售后服务、物流配送、促销活动等高频问题，有效降低人工客服工作量，提升咨询响应效率与用户满意度。

系统支持灵活的知识库管理，商家可上传商品资料、售后政策、物流规则、常见问题等文档，AI 客服即可基于这些资料精准答复。同时，系统内置运费计算、订单时效预估等工具化能力，可处理需要实时计算的复杂咨询场景。

---

## ✨ 核心功能

### 1. 📚 知识库问答

- **多类型文档支持**：支持上传商品介绍、售后政策、物流规则、活动说明、FAQ 等各类文档
- **语义检索**：基于向量数据库的语义检索，理解用户意图，精准匹配相关内容
- **智能分块**：带重叠的语义分块技术，保留文档上下文完整性
- **相似度过滤**：默认 0.7 相似度阈值过滤，过滤低质量检索结果
- **结果去重**：自动去除重复片段，避免信息冗余
- **查询优化**：自动重写用户 query，提升检索准确性

### 2. 🛠️ Agent 工具调用

- **运费计算**：根据目的地、重量、快递类型自动计算运费
- **订单时效预估**：基于物流数据预估包裹到达时间
- **智能推理**：ReAct 框架实现推理与行动协同，支持复杂任务分解
- **多轮对话**：基于 LangGraph 状态机管理对话上下文，支持多轮交互
- **工具扩展**：开放的工具注册机制，支持自定义业务工具接入

### 3. 🎨 可视化管理后台

- **一体化 Web 界面**：文档上传、知识库管理、参数配置、对话测试一站式完成
- **实时对话**：流式输出响应，Markdown 渲染，支持代码高亮
- **知识库管理**：文档上传、列表查看、单篇删除、一键清空
- **参数调节**：模型温度、检索数量、对话轮次等参数可视化配置
- **历史记录**：完整的对话记录管理，支持会话切换

### 4. 🤖 多模型兼容

- **统一 API 封装**：符合 OpenAI 接口规范的客户端封装
- **模型无缝切换**：支持 DeepSeek、Qwen、GLM-4 等主流大模型
- **嵌入模型**：支持 bge-large-zh-v1.5、bge-small-zh-v1.5 等中文嵌入模型
- **重排序模型**：支持 bge-reranker-base、bge-reranker-large 等重排序模型
- **云端/本地灵活切换**：支持云端 API 与本地模型两种部署方式

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层                              │
│              FastAPI + HTML/CSS/JavaScript                  │
│                   (响应式 Web 管理界面)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                        Agent 层                             │
│                    LangGraph 框架                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 简单对话 │  │ 工具调用 │  │ RAG 检索 │  │ 提示链   │  │
│  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                        检索层                              │
│               Chroma 向量库 + BM25 检索                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 向量检索 │  │ 关键词   │  │ 混合检索 │  │ 查询优化 │  │
│  │          │  │ 检索     │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      大模型 API 层                          │
│                  OpenAI 协议接口封装                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ DeepSeek │  │  Qwen   │  │  GLM-4  │  │ Embedding│  │
│  │   系列    │  │   系列   │  │   系列   │  │   模型   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 技术栈

### 核心框架

| 技术 | 版本要求 | 说明 |
|------|----------|------|
| **Python** | 3.12+ | 主要开发语言 |
| **LangGraph** | 0.2+ | Agent 状态图与推理框架 |
| **LangChain** | 0.3+ | LLM 应用开发框架 |
| **FastAPI** | 0.115+ | 高性能 Web 框架 |
| **Uvicorn** | 0.32+ | ASGI 服务器 |

### RAG 检索组件

| 技术 | 说明 |
|------|------|
| **Chroma** | 向量数据库，存储文档向量表示 |
| **BM25** | 关键词检索算法 |
| **Sentence Transformers** | 文本嵌入模型 |
| **Cross-Encoder** | 结果重排序模型 |
| **jieba** | 中文分词工具 |

### AI 模型

| 技术 | 说明 |
|------|------|
| **DeepSeek-V3** | 主对话模型 |
| **Qwen 系列** | 阿里通义千问模型 |
| **GLM-4 系列** | 智谱 AI 模型 |
| **bge-large-zh-v1.5** | 中文嵌入模型 |

### 工具与数据处理

| 技术 | 说明 |
|------|------|
| **Pydantic** | 数据验证与配置管理 |
| **python-dotenv** | 环境变量管理 |
| **requests** | HTTP 请求库 |
| **Poetry** | Python 依赖管理 |
| **pytest** | 单元测试框架 |

---

## 🚀 快速部署

### 环境要求

- **Python**: 3.12 或更高版本
- **操作系统**: Windows / Linux / macOS
- **内存**: 推荐 4GB 以上
- **磁盘**: 推荐 2GB 以上可用空间

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/your-repo/ecommerce-agent-system.git
cd ecommerce-agent-system

# 使用 Poetry 安装（推荐）
poetry install
poetry shell

# 或使用 pip 安装
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 配置文件
```

**核心配置项说明**：

```bash
# 必填：API 密钥
GITEE_AI_API_KEY=your_api_key_here

# 主对话模型（推荐 DeepSeek-V3）
GITEE_AI_MODEL=DeepSeek-V3

# RAG 配置
USE_CLOUD_EMBEDDING=true
CLOUD_EMBEDDING_MODEL=bge-large-zh-v1.5
USE_CLOUD_RERANKER=true
CLOUD_RERANKER_MODEL=bge-reranker-base

# 检索优化配置
CHUNK_SIZE=500
CHUNK_OVERLAP=100
SIMILARITY_THRESHOLD=0.7
```

### 3. 启动服务

```bash
# 方式一：自动化启动（推荐）
python run_web_auto.py

# 方式二：标准启动
python run_web.py

# 服务启动后访问
http://localhost:8001
```

### 4. 上传知识库文档

1. 打开 Web 界面，进入「商品资料库管理」标签页
2. 在资料库名称输入 `product_knowledge`（或自定义名称）
3. 选择「上传商品资料/售后规则文档」卡片
4. 粘贴商品资料、售后政策等内容（每行一个文档）
5. 点击「上传商品资料」按钮完成上传

**推荐上传的文档类型**：
- `docs/ecommerce_kb/goods_intro.txt` - 商品介绍
- `docs/ecommerce_kb/after_sale_policy.txt` - 售后政策
- `docs/ecommerce_kb/logistics_rules.txt` - 物流配送规则
- `docs/ecommerce_kb/promotion_rules.txt` - 促销活动规则
- `docs/ecommerce_kb/faq.txt` - 常见问题解答

### 5. 验证部署

```bash
# 运行单元测试
pytest tests/

# 测试对话功能
python examples/01_simple_chat.py

# 测试工具调用
python examples/02_simple_agent_with_tools.py
```

---

## 💡 业务价值

### 适用场景

| 场景 | 说明 |
|------|------|
| **电商店铺客服** | 淘宝、京东、拼多多、Shopee 等平台店铺智能客服 |
| **品牌官网客服** | 品牌官网产品咨询、售后服务自动应答 |
| **跨境电商客服** | 多语言智能客服，支持商品咨询国际化场景 |
| **客服工单分流** | 智能分类客户问题，高频简单问题自动处理 |

### 核心优势

- **降低人工成本**：高频标准化问题自动处理，减少人工客服工作量 60%+
- **提升响应效率**：7×24 小时实时响应，秒级回复速度
- **统一服务标准**：基于知识库标准答案，保证答复一致性
- **快速冷启动**：上传文档即可使用，无需复杂配置
- **灵活扩展**：开放工具接口，支持对接物流、ERP 等业务系统

### 典型问答场景

| 咨询类型 | 示例问题 | 系统能力 |
|----------|----------|----------|
| 商品咨询 | "这件T恤是什么材质的？" | 检索商品资料库回答 |
| 尺码选择 | "175cm 140斤穿什么码？" | 基于尺码表推荐 |
| 售后政策 | "可以7天无理由退货吗？" | 检索售后政策回答 |
| 运费计算 | "发到新疆运费多少？" | 调用运费计算工具 |
| 物流查询 | "订单什么时候能到？" | 调用时效预估工具 |
| 活动咨询 | "优惠券怎么使用？" | 检索活动规则回答 |

---

## 📂 项目结构

```
ecommerce-agent-system/
├── src/ecommerce_agent/              # 核心代码模块
│   ├── agents/                       # Agent 实现
│   │   ├── simple_agent.py          # 简单对话 Agent
│   │   ├── tool_agent.py            # 工具调用 Agent
│   │   ├── rag_agent.py             # RAG 检索 Agent
│   │   └── tools/                   # 工具集
│   │       └── calculator_tool.py   # 计算器工具
│   ├── rag/                         # RAG 检索模块
│   │   ├── embeddings.py            # 嵌入模型
│   │   ├── vector_store.py          # 向量存储
│   │   ├── retrievers.py            # 检索器
│   │   └── document_loader.py       # 文档加载
│   ├── tools/                       # 工具集
│   │   ├── basic_tools.py           # 基础工具（13个）
│   │   └── ai_powered_tools.py      # AI 工具（10个）
│   ├── config.py                    # 配置管理
│   ├── api_client.py                # API 客户端
│   ├── web_app.py                   # Web 应用
│   └── static/                      # 前端资源
│       └── index.html               # Web 管理界面
├── examples/                         # 示例代码
│   ├── 01_simple_chat.py            # 简单对话示例
│   ├── 02_simple_agent_with_tools.py # 工具调用示例
│   └── 07_rag_basic_usage.py        # RAG 基础示例
├── tests/                           # 测试代码
│   ├── test_calculator_tool.py      # 工具测试
│   └── test_rag_optimization.py    # RAG 优化测试
├── docs/ecommerce_kb/              # 电商知识库文档
│   ├── goods_intro.txt              # 商品介绍
│   ├── after_sale_policy.txt        # 售后政策
│   ├── logistics_rules.txt          # 物流规则
│   ├── promotion_rules.txt          # 活动规则
│   └── faq.txt                      # 常见问题
├── run_web.py                       # Web 启动脚本
├── run_web_auto.py                  # 自动启动脚本
├── pyproject.toml                   # 项目配置
├── .env.example                     # 环境变量示例
└── README.md                        # 项目文档
```

---

## 📄 接口文档

服务启动后，可通过以下地址访问接口文档：

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### 主要 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat/stream` | POST | 流式对话接口 |
| `/api/rag/upload/texts` | POST | 上传文本到知识库 |
| `/api/rag/upload/file` | POST | 上传文件到知识库 |
| `/api/rag/query/stream` | POST | RAG 流式查询 |
| `/api/rag/collections` | GET | 获取知识库列表 |
| `/api/rag/clear/{name}` | DELETE | 清空知识库 |
| `/api/history/{session_id}` | GET | 获取对话历史 |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📜 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。
