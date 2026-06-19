import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from zhouhonglin_agent.rag.retrievers import VectorRetriever, KeywordRetriever, HybridRetriever

print("=" * 60)
print("直接测试检索功能")
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

# 创建检索器
vector_retriever = VectorRetriever(vector_store, similarity_threshold=0.0)

# 测试向量检索
print("\n向量检索测试...")
results = vector_retriever.retrieve("续航时间", top_k=3)
print(f"向量检索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

# 测试混合检索
print("\n混合检索测试...")
keyword_retriever = KeywordRetriever(similarity_threshold=0.0)
hybrid_retriever = HybridRetriever(vector_retriever, keyword_retriever, similarity_threshold=0.0)
results = hybrid_retriever.retrieve("续航时间", top_k=3)
print(f"混合检索结果数: {len(results)}")
for i, (doc, score) in enumerate(results):
    print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:80]}...")

print("\n" + "=" * 60)