import sys
import os

# 加载 .env 文件
from dotenv import load_dotenv
load_dotenv('e:/sgg1/shuyixiao-agent/.env')

sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from zhouhonglin_agent.rag.document_loader import DocumentLoader

print("=" * 60)
print("直接测试向量搜索（无需 API Key）")
print("=" * 60)

# 创建向量存储
vector_store = VectorStoreManager(
    collection_name="product_knowledge",
    persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
    embedding_manager=None
)

# 创建文档加载器
doc_loader = DocumentLoader()

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

# 切分文本
print("\n1. 切分文本...")
chunks = doc_loader.split_text(test_text)
print(f"切分完成，片段数: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"  片段 {i+1}: {chunk.page_content[:50]}...")

# 写入向量库
print("\n2. 写入向量库...")
doc_ids = vector_store.add_documents(chunks)
print(f"写入完成，ID 数: {len(doc_ids)}")

# 检查文档数量
print("\n3. 检查文档数量...")
count = vector_store.get_document_count()
print(f"文档数量: {count}")

# 搜索测试
print("\n4. 搜索测试...")

print("\n搜索: '续航时间'")
results = vector_store.similarity_search_with_score("续航时间", k=3)
print(f"搜索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

print("\n搜索: '蓝牙音箱'")
results = vector_store.similarity_search_with_score("蓝牙音箱", k=3)
print(f"搜索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

print("\n搜索: '防水等级'")
results = vector_store.similarity_search_with_score("防水等级", k=3)
print(f"搜索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)