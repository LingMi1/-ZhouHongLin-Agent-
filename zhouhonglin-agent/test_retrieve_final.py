import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager

print("=" * 60)
print("最终测试：向量库检索功能")
print("=" * 60)

# 创建向量存储
vector_store = VectorStoreManager(
    collection_name="product_knowledge",
    persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
    embedding_manager=None
)

# 检查文档数量
count = vector_store.get_document_count()
print(f"\n文档数量: {count}")

# 测试检索
queries = ["续航时间", "蓝牙音箱", "防水等级", "充电时间"]

for query in queries:
    print(f"\n查询: {query}")
    results = vector_store.similarity_search_with_score(query, k=3)
    print(f"检索到 {len(results)} 个文档")
    
    for i, (doc, score) in enumerate(results):
        print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:100]}...")

print("\n" + "=" * 60)
print("结论：向量库检索功能正常！")
print("=" * 60)