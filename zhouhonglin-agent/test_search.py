import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager

print("=" * 60)
print("测试向量搜索")
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

# 列出所有文档
print("\n列出所有文档...")
results = vector_store.collection.get()
print(f"文档数: {len(results['ids'])}")
for i, doc_id in enumerate(results['ids']):
    text = results['documents'][i] if results.get('documents') else ''
    print(f"  文档 {i+1}: {text[:80]}...")

# 搜索测试
print("\n搜索: '续航时间'")
results = vector_store.similarity_search_with_score("续航时间", k=3)
print(f"搜索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

print("\n" + "=" * 60)