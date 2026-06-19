import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from zhouhonglin_agent.rag.document_loader import DocumentLoader
from langchain_core.documents import Document

# 测试向量存储
print("=" * 60)
print("测试向量存储功能")
print("=" * 60)

# 1. 创建向量存储（不传入嵌入模型，使用 Chroma 默认嵌入）
print("\n1. 创建向量存储...")
vector_store = VectorStoreManager(
    collection_name="test_collection",
    persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
    embedding_manager=None  # 不传入嵌入模型，使用 Chroma 默认嵌入
)

# 2. 创建文档
print("\n2. 创建文档...")
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

# 3. 文本切分
print("\n3. 文本切分...")
doc_loader = DocumentLoader()
chunks = doc_loader.split_text(test_text)
print(f"切分后片段数: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"片段 {i+1}: {chunk.page_content[:50]}...")

# 4. 写入向量库
print("\n4. 写入向量库...")
doc_ids = vector_store.add_documents(chunks)
print(f"写入成功，返回 ID 数: {len(doc_ids)}")

# 5. 检查文档数量
print("\n5. 检查文档数量...")
count = vector_store.get_document_count()
print(f"文档数量: {count}")

# 6. 列出文档
print("\n6. 列出文档...")
docs = vector_store.list_documents()
print(f"文档列表: {docs}")

# 7. 搜索测试
print("\n7. 搜索测试...")
results = vector_store.similarity_search("蓝牙音箱", k=3)
print(f"搜索结果: {len(results)} 个文档")
for i, doc in enumerate(results):
    print(f"结果 {i+1}: {doc.page_content[:50]}...")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)