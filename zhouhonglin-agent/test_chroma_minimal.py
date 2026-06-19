import chromadb
from chromadb.config import Settings as ChromaSettings
from pathlib import Path

print("=" * 60)
print("最简单的 ChromaDB 测试")
print("=" * 60)

# 创建客户端
persist_dir = "e:/sgg1/shuyixiao-agent/data/chroma"
Path(persist_dir).mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(
    path=persist_dir,
    settings=ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# 创建集合
print("\n创建集合...")
try:
    collection = client.get_collection(name="product_knowledge")
    print(f"已加载现有集合，文档数: {collection.count()}")
except:
    collection = client.create_collection(
        name="product_knowledge",
        metadata={"hnsw:space": "cosine"}
    )
    print(f"已创建新集合")

# 添加文档
print("\n添加文档...")
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

# 查询文档
print("\n查询文档...")
results = collection.get()
print(f"文档数量: {len(results['ids'])}")
print(f"文档内容: {results['documents']}")

print("\n" + "=" * 60)
print("测试完成！ChromaDB 正常工作")
print("=" * 60)