import chromadb
from chromadb.config import Settings as ChromaSettings
from pathlib import Path

# 直接测试 ChromaDB 基本功能
print("=" * 60)
print("直接测试 ChromaDB 基本功能")
print("=" * 60)

# 1. 创建客户端
print("\n1. 创建 ChromaDB 客户端...")
persist_dir = "e:/sgg1/shuyixiao-agent/data/chroma"
Path(persist_dir).mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(
    path=persist_dir,
    settings=ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# 2. 创建集合
print("\n2. 创建集合...")
try:
    collection = client.get_collection(name="product_knowledge")
    print(f"已加载现有集合，文档数: {collection.count()}")
except:
    collection = client.create_collection(
        name="product_knowledge",
        metadata={"hnsw:space": "cosine"}
    )
    print(f"已创建新集合")

# 3. 添加文档（使用 Chroma 默认嵌入）
print("\n3. 添加文档...")
test_docs = [
    "商品名称：智能蓝牙音箱Pro版，支持蓝牙5.0连接",
    "商品型号：BT-SPK-2024-PRO，尺寸150mm x 80mm x 60mm",
    "商品特点：内置2000mAh锂电池，续航时间8小时，IPX7防水"
]

collection.add(
    documents=test_docs,
    ids=["doc1", "doc2", "doc3"]
)

print(f"添加完成，文档数: {collection.count()}")

# 4. 查询文档
print("\n4. 查询文档...")
results = collection.get()
print(f"查询结果: {results}")

# 5. 搜索测试
print("\n5. 搜索测试...")
search_results = collection.query(
    query_texts=["蓝牙音箱"],
    n_results=2
)
print(f"搜索结果: {search_results}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)