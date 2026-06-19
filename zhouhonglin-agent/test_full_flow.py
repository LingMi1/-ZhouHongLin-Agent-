import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.rag_agent import RAGAgent
from zhouhonglin_agent.config import settings

print("=" * 60)
print("完整链路测试：上传 -> 查询")
print("=" * 60)

# 设置配置
settings.use_cloud_embedding = False

# 创建 RAG Agent（禁用查询优化，避免需要 API Key）
print("\n1. 创建 RAG Agent...")
agent = RAGAgent(
    collection_name="product_knowledge",
    use_reranker=False,
    retrieval_mode="vector",
    enable_query_optimization=False,
    enable_context_expansion=False
)

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
print("\n2. 添加文本到知识库...")
chunks = agent.add_texts([test_text])
print(f"添加完成，片段数: {chunks}")

# 检查文档数量
print("\n3. 检查文档数量...")
count = agent.get_document_count()
print(f"文档数量: {count}")

# 查询测试
print("\n4. 查询测试...")
question = "这个蓝牙音箱的续航时间是多少？"
print(f"问题: {question}")
answer = agent.query(question, top_k=3, optimize_query=False)
print(f"回答: {answer}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)