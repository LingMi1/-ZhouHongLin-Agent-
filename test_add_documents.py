#!/usr/bin/env python3
"""测试 VectorStoreManager.add_documents 返回值"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from langchain_core.documents import Document

# 创建 VectorStoreManager（不传入 embedding_manager，使用默认嵌入）
vs = VectorStoreManager(
    collection_name="test_add_docs",
    embedding_manager=None
)

# 创建测试文档
docs = [
    Document(page_content="商品名称：测试商品A\n价格：¥100", metadata={"source": "test.txt"})
]

print(f"测试文档数量: {len(docs)}")
print(f"文档内容: {docs[0].page_content}")

# 调用 add_documents
print("\n调用 add_documents...")
doc_ids = vs.add_documents(docs)
print(f"返回的文档ID列表: {doc_ids}")
print(f"返回列表长度: {len(doc_ids)}")

# 检查集合中文档数量
count = vs.get_document_count()
print(f"\n集合中文档数量: {count}")

# 清理测试集合
vs.clear()
print("\n测试完成")