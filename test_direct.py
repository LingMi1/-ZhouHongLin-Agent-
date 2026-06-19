#!/usr/bin/env python3
"""直接测试RAGAgent核心逻辑"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.rag_agent import RAGAgent

# 创建RAGAgent
print("创建 RAGAgent...")
agent = RAGAgent(
    collection_name="test_direct",
    use_reranker=False
)

# 测试文本
text = "商品名称：测试商品A\n价格：¥100\n库存：100"
print(f"\n测试文本: {text}")
print(f"文本长度: {len(text)}")

# 调用 add_texts
print("\n调用 add_texts...")
result = agent.add_texts([text])
print(f"add_texts 返回值: {result}")
print(f"返回类型: {type(result)}")

# 检查向量库文档数量
count = agent.vector_store.get_document_count()
print(f"\n向量库文档数量: {count}")

# 清理测试集合
agent.vector_store.clear()
print("\n测试完成")