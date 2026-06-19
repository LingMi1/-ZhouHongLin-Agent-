import sys
sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.rag_agent import RAGAgent

print("=" * 60)
print("测试 RAG Agent 检索功能（不调用 LLM）")
print("=" * 60)

# 创建 RAG Agent（禁用查询优化）
agent = RAGAgent(
    collection_name="product_knowledge",
    system_message="你是一个有帮助的AI助手。",
    use_reranker=True,
    retrieval_mode="hybrid",
    enable_query_optimization=False,
    enable_context_expansion=False
)

# 测试检索
query = "续航时间"
print(f"\n查询: {query}")

# 直接调用 retrieve 方法
documents = agent.retrieve(query, top_k=3, use_rerank=False)
print(f"检索到 {len(documents)} 个文档")

for i, doc in enumerate(documents):
    print(f"\n文档 {i+1}:")
    print(f"  内容: {doc.page_content[:150]}...")
    print(f"  元数据: {doc.metadata}")

print("\n" + "=" * 60)