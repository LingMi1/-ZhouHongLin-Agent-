#!/usr/bin/env python3
"""测试文本切分逻辑"""

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

from zhouhonglin_agent.rag.document_loader import DocumentLoader

loader = DocumentLoader()
text = '商品名称：测试商品A\n价格：¥100\n库存：100'
print(f'输入文本长度: {len(text)}')

chunks = loader.split_text(text)
print(f'切分结果: {len(chunks)} 个片段')
for i, chunk in enumerate(chunks):
    content = chunk.page_content.encode('utf-8').decode('utf-8')
    print(f'  片段 {i}: {content}')