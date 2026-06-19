import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

import chromadb
from chromadb.config import Settings as ChromaSettings

print("=" * 60)
print("测试 ChromaDB 距离计算")
print("=" * 60)

client = chromadb.PersistentClient(
    path="e:/sgg1/shuyixiao-agent/data/chroma",
    settings=ChromaSettings(anonymized_telemetry=False)
)

collection = client.get_collection("product_knowledge")

# 使用 query_texts 查询
results = collection.query(
    query_texts=["续航时间", "蓝牙音箱", "防水等级"],
    n_results=3,
    include=['documents', 'metadatas', 'distances']
)

print("\n查询结果:")
for i, query in enumerate(["续航时间", "蓝牙音箱", "防水等级"]):
    print(f"\n查询: {query}")
    ids = results['ids'][i]
    distances = results['distances'][i]
    docs = results['documents'][i]
    for j, doc_id in enumerate(ids):
        print(f"  文档: {docs[j][:50]}...")
        print(f"  距离: {distances[j]:.4f}")
        print(f"  相似度(1-distance): {1-distances[j]:.4f}")

print("\n" + "=" * 60)