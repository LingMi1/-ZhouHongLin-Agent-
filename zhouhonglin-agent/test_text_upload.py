#!/usr/bin/env python3
"""测试文本上传功能"""

import sys
import io
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8001"

print("测试文本上传功能")
print("=" * 40)

# 测试1：10行文本上传
print("\n1. 10行文本上传测试:")
url = f"{API_BASE}/api/rag/upload/texts"

test_texts = [
    "商品名称：测试商品A|价格：¥100|库存：100",
    "商品名称：测试商品B|价格：¥200|库存：200",
    "商品名称：测试商品C|价格：¥300|库存：300",
    "商品名称：测试商品D|价格：¥400|库存：400",
    "商品名称：测试商品E|价格：¥500|库存：500",
    "商品名称：测试商品F|价格：¥600|库存：600",
    "商品名称：测试商品G|价格：¥700|库存：700",
    "商品名称：测试商品H|价格：¥800|库存：800",
    "商品名称：测试商品I|价格：¥900|库存：900",
    "商品名称：测试商品J|价格：¥1000|库存：1000"
]

try:
    data = {"texts": test_texts, "collection_name": "product_knowledge"}
    response = requests.post(url, json=data, timeout=60)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] 上传成功")
        print(f"片段数: {result.get('chunks_added', 0)}")
        print(f"总行数: {result.get('total_lines', 0)}")
        print(f"总文档数: {result.get('total_documents', 0)}")
    else:
        print(f"[ERR] {response.text}")
except Exception as e:
    print(f"[ERR] {e}")

# 测试2：空内容校验
print("\n2. 空内容校验测试:")
try:
    data = {"texts": ["", "   ", "\n"], "collection_name": "test"}
    response = requests.post(url, json=data, timeout=10)
    print(f"状态码: {response.status_code}")
    if response.status_code == 400:
        print(f"[OK] 正确拦截空内容")
    else:
        print(f"[ERR] 未正确拦截")
except Exception as e:
    print(f"[ERR] {e}")

print("\n测试完成")