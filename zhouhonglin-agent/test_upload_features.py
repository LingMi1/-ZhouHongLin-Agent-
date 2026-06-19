#!/usr/bin/env python3
"""测试上传功能优化"""

import sys
import os
import io
import requests
import json

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8001"

print("=" * 60)
print("测试上传功能优化")
print("=" * 60)

# 测试1：文件上传测试
print("\n1. 文件上传测试:")
url = f"{API_BASE}/api/rag/upload/files"

try:
    with open("e:/sgg1/shuyixiao-agent/sample_data/goods_catalog_1.txt", 'rb') as f:
        files = {'files': ('goods_catalog_1.txt', f, 'text/plain')}
        data = {'collection_name': 'product_knowledge'}
        response = requests.post(url, files=files, data=data, timeout=60)
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 上传成功")
        print(f"   文件数: {result.get('total_files', 0)}")
        print(f"   片段数: {result.get('total_chunks', 0)}")
        print(f"   总文档数: {result.get('total_documents', 0)}")
    else:
        print(f"   [ERR] 上传失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 上传异常: {e}")

# 测试2：文本粘贴上传测试（10行）
print("\n2. 文本粘贴上传测试（10行）:")
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
    data = {
        "texts": test_texts,
        "collection_name": "product_knowledge"
    }
    response = requests.post(url, json=data, timeout=60)
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 上传成功")
        print(f"   片段数: {result.get('chunks_added', 0)}")
        print(f"   总行数: {result.get('total_lines', 0)}")
        print(f"   总文档数: {result.get('total_documents', 0)}")
    else:
        print(f"   [ERR] 上传失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 上传异常: {e}")

# 测试3：空内容校验测试
print("\n3. 空内容校验测试:")

try:
    data = {
        "texts": ["", "   ", "\n"],
        "collection_name": "product_knowledge"
    }
    response = requests.post(url, json=data, timeout=60)
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 400:
        result = response.json()
        print(f"   [OK] 正确拦截空内容")
        print(f"   错误信息: {result.get('detail', '')}")
    else:
        print(f"   [ERR] 未正确拦截空内容")
        
except Exception as e:
    print(f"   [ERR] 请求异常: {e}")

# 测试4：批量文档上传测试（两份文档）
print("\n4. 批量文档上传测试（两份文档）:")
url = f"{API_BASE}/api/rag/upload/files"

try:
    files = []
    with open("e:/sgg1/shuyixiao-agent/sample_data/goods_catalog_1.txt", 'rb') as f1:
        with open("e:/sgg1/shuyixiao-agent/sample_data/goods_catalog_2.txt", 'rb') as f2:
            files = [
                ('files', ('goods_catalog_1.txt', f1, 'text/plain')),
                ('files', ('goods_catalog_2.txt', f2, 'text/plain'))
            ]
            data = {'collection_name': 'batch_test'}
            response = requests.post(url, files=files, data=data, timeout=60)
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 批量上传成功")
        print(f"   文件数: {result.get('total_files', 0)}")
        print(f"   片段数: {result.get('total_chunks', 0)}")
        print(f"   总文档数: {result.get('total_documents', 0)}")
    else:
        print(f"   [ERR] 上传失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 上传异常: {e}")

# 测试5：验证资料库列表同步更新
print("\n5. 验证资料库列表同步更新:")
url = f"{API_BASE}/api/rag/collections"

try:
    response = requests.get(url, timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        collections = response.json()
        print(f"   [OK] 获取成功")
        print(f"   资料库数量: {len(collections)}")
        for coll in collections:
            print(f"   - {coll.get('name', '')}: {coll.get('document_count', 0)} 个文档")
    else:
        print(f"   [ERR] 获取失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 请求异常: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)