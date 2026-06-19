#!/usr/bin/env python3
"""测试包含特殊字符的文档处理"""

import sys
import os
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zhouhonglin_agent.rag.context_manager import ContextManager
from zhouhonglin_agent.rag.vector_store import VectorStoreManager
from langchain_core.documents import Document
import json

print("=" * 60)
print("测试包含特殊字符的文档处理")
print("=" * 60)

# 测试文档内容（包含各种特殊字符）
test_docs = [
    Document(
        page_content='商品名称：智能蓝牙音箱"Pro版"\n'
                    '特性：支持"蓝牙5.3"、"WiFi6"\n'
                    '价格：¥299.00\n'
                    '描述：这款音箱拥有"卓越音质"和"超长续航"',
        metadata={"source": "test1.txt"}
    ),
    Document(
        page_content='产品参数：\n'
                    '- 尺寸：10" x 5" x 3"\n'
                    '- 重量：500g\n'
                    '- 功率：20W\n'
                    '警告：请勿在"高温环境"下使用',
        metadata={"source": "test2.txt"}
    ),
    Document(
        page_content='用户评价：\n'
                    '"非常棒！" - 用户A\n'
                    '"物超所值" - 用户B\n'
                    '注意：产品包含"锂电池"，运输时需注意',
        metadata={"source": "test3.txt"}
    ),
    Document(
        page_content='多换行测试\n\n\n'
                    '段落1\n\n'
                    '段落2\n\n'
                    '段落3',
        metadata={"source": "test4.txt"}
    )
]

# 测试1：上下文管理器格式化
print("\n1. 测试上下文管理器格式化:")
context_manager = ContextManager()

try:
    prompt = context_manager.format_documents_for_prompt(
        test_docs,
        query="这款音箱的价格是多少？",
        instruction="请基于以下文档内容回答问题。"
    )
    print("[OK] 格式化成功")
    
    # 验证JSON序列化
    messages = [{"role": "user", "content": prompt}]
    json_str = json.dumps(messages, ensure_ascii=False)
    print("[OK] JSON序列化成功")
    print(f"  JSON长度: {len(json_str)}")
    
    # 验证JSON解析
    parsed = json.loads(json_str)
    print("[OK] JSON解析成功")
    
except Exception as e:
    print(f"[ERR] 格式化失败: {e}")

# 测试2：测试截断功能
print("\n2. 测试截断功能:")
long_text = '商品名称：智能蓝牙音箱"Pro版"\n' * 50
doc = Document(page_content=long_text, metadata={"source": "test.txt"})

try:
    # 截断到100个token
    truncated = context_manager.truncate_text(long_text, max_tokens=100)
    print(f"[OK] 截断成功")
    print(f"  原长度: {len(long_text)}, 截断后长度: {len(truncated)}")
    
    # 验证截断后的文本可以正常JSON序列化
    messages = [{"role": "user", "content": truncated}]
    json_str = json.dumps(messages, ensure_ascii=False)
    print("[OK] 截断后JSON序列化成功")
    
except Exception as e:
    print(f"[ERR] 截断失败: {e}")

# 测试3：测试向量存储
print("\n3. 测试向量存储:")
try:
    vector_store = VectorStoreManager(
        collection_name="test_special_chars",
        persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
        embedding_manager=None
    )
    
    # 添加测试文档
    doc_ids = vector_store.add_documents(test_docs)
    print(f"[OK] 添加文档成功，ID数: {len(doc_ids)}")
    print(f"[OK] 文档总数: {vector_store.get_document_count()}")
    
    # 查询测试
    question = '这款音箱的价格是多少？'
    print(f"[INFO] 查询: {question}")
    
    results = vector_store.similarity_search_with_score(question, k=3)
    print(f"[OK] 检索到 {len(results)} 个文档")
    
    for i, (doc, score) in enumerate(results):
        print(f"  结果 {i+1}: {doc.page_content[:50]}...")
    
except Exception as e:
    print(f"[ERR] 向量存储失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)