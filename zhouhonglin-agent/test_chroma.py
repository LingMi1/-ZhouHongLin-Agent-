import chromadb
from chromadb.config import Settings as ChromaSettings

# 测试 ChromaDB 是否能正常工作
print("测试 ChromaDB...")

client = chromadb.PersistentClient(
    path="e:/sgg1/shuyixiao-agent/data/chroma",
    settings=ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# 创建集合
print("创建集合...")
collection = client.create_collection(
    name="test_collection",
    metadata={"hnsw:space": "cosine"}
)

# 添加文档
print("添加文档...")
collection.add(
    documents=["这是测试文档1", "这是测试文档2"],
    ids=["doc1", "doc2"]
)

# 检查文档数量
print(f"文档数量: {collection.count()}")

# 查询文档
print("查询文档...")
results = collection.get()
print(f"文档列表: {results}")

# 删除测试集合
client.delete_collection(name="test_collection")
print("测试完成！")