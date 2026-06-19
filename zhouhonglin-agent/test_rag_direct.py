import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 设置环境变量，禁用云端嵌入（避免网络问题）
os.environ['USE_CLOUD_EMBEDDING'] = 'false'

from zhouhonglin_agent.rag.rag_agent import RAGAgent
from zhouhonglin_agent.config import settings

print("=" * 60)
print("直接测试 RAG Agent 的 add_texts 方法")
print("=" * 60)

# 强制使用本地嵌入模型
settings.use_cloud_embedding = False
settings.embedding_model = "BAAI/bge-small-zh-v1.5"

print(f"\n配置:")
print(f"  use_cloud_embedding: {settings.use_cloud_embedding}")
print(f"  embedding_model: {settings.embedding_model}")
print(f"  vector_db_path: {settings.vector_db_path}")

# 创建 RAG Agent
print("\n创建 RAG Agent...")
try:
    agent = RAGAgent(
        collection_name="test_direct",
        use_reranker=False
    )
    print("RAG Agent 创建成功")
except Exception as e:
    print(f"RAG Agent 创建失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 测试文本
test_text = """
商品名称：智能蓝牙音箱Pro版
商品型号：BT-SPK-2024-PRO
商品规格：黑色/白色/蓝色三种颜色可选
商品尺寸：150mm x 80mm x 60mm
商品重量：净重350g，包装重量450g

商品特点：
1. 支持蓝牙5.0连接，传输距离可达10米
2. 内置2000mAh锂电池，续航时间8小时
3. IPX7防水等级，可浸泡水下1米深30分钟
"""

# 添加文本
print("\n添加文本...")
try:
    chunks = agent.add_texts([test_text])
    print(f"添加完成，返回片段数: {chunks}")
except Exception as e:
    print(f"添加文本失败: {e}")
    import traceback
    traceback.print_exc()

# 检查文档数量
print("\n检查文档数量...")
try:
    count = agent.get_document_count()
    print(f"文档数量: {count}")
except Exception as e:
    print(f"获取文档数量失败: {e}")

# 列出文档
print("\n列出文档...")
try:
    docs = agent.list_documents()
    print(f"文档列表: {docs}")
except Exception as e:
    print(f"列出文档失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)