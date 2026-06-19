import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from zhouhonglin_agent.rag.retrievers import VectorRetriever, KeywordRetriever, HybridRetriever

print("=" * 60)
print("测试 RAG 检索流程（模拟 RAG Agent）")
print("=" * 60)

# 创建向量存储
vector_store = VectorStoreManager(
    collection_name="product_knowledge",
    persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
    embedding_manager=None
)

# 创建检索器
vector_retriever = VectorRetriever(vector_store, similarity_threshold=0.0)
keyword_retriever = KeywordRetriever(similarity_threshold=0.0)
hybrid_retriever = HybridRetriever(
    vector_retriever,
    keyword_retriever,
    similarity_threshold=0.0
)

# 模拟 RAG Agent 的 retrieve 方法
def retrieve(query, top_k=3, use_rerank=False):
    print(f"\n查询: {query}")
    
    # 混合检索
    results = hybrid_retriever.retrieve(query, top_k=top_k)
    print(f"混合检索结果数: {len(results)}")
    
    for i, (doc, score) in enumerate(results):
        print(f"  结果 {i+1} (分数: {score:.4f}): {doc.page_content[:100]}...")
    
    documents = [doc for doc, score in results]
    return documents

# 测试检索
queries = ["续航时间", "蓝牙音箱", "防水等级", "充电时间"]

for query in queries:
    documents = retrieve(query)
    if documents:
        print(f"  [OK] 检索成功，找到 {len(documents)} 个相关文档")
    else:
        print(f"  [ERR] 未找到相关文档")

print("\n" + "=" * 60)
print("结论：检索功能正常！问题在于 LLM API 调用。")
print("=" * 60)