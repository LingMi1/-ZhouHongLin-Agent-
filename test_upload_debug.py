#!/usr/bin/env python3
"""调试上传功能"""

import sys
import io
import requests
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8001"

print("调试上传功能")
print("=" * 40)

time.sleep(2)

# 创建测试文件
test_content = "商品名称：测试商品A\n价格：¥100\n库存：100\n\n商品名称：测试商品B\n价格：¥200\n库存：200"
temp_file = "e:/sgg1/test_upload.txt"
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

# 上传测试文件到 test 库
print("\n1. 上传文件到 test 库:")
url = f"{API_BASE}/api/rag/upload/files"

try:
    with open(temp_file, 'rb') as f:
        files = {'files': ('test_upload.txt', f, 'text/plain')}
        data = {'collection_name': 'test'}
        response = requests.post(url, files=files, data=data, timeout=120)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] 上传成功")
        print(f"文件数: {result.get('total_files', 0)}")
        print(f"片段数: {result.get('total_chunks', 0)}")
        print(f"总文档数: {result.get('total_documents', 0)}")
        print(f"collection_name: {result.get('collection_name', '')}")
    else:
        print(f"[ERR] {response.text}")
        
except Exception as e:
    print(f"[ERR] {e}")

# 查看所有集合
print("\n2. 查看所有集合:")
url = f"{API_BASE}/api/rag/collections"
try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        collections = response.json()
        print(f"集合数量: {len(collections)}")
        for coll in collections:
            print(f"  - {coll.get('name', '')}: {coll.get('document_count', 0)} 个文档")
    else:
        print(f"[ERR] {response.text}")
except Exception as e:
    print(f"[ERR] {e}")

# 查看 test 库文档列表
print("\n3. 查看 test 库文档列表:")
url = f"{API_BASE}/api/rag/documents/test?limit=10"
try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        docs = response.json()
        print(f"文档数量: {len(docs)}")
        for doc in docs[:3]:
            print(f"  ID: {doc.get('id', '')}")
            print(f"  Content: {doc.get('content', '')[:50]}...")
    else:
        print(f"[ERR] {response.text}")
except Exception as e:
    print(f"[ERR] {e}")

# 清理临时文件
import os
os.remove(temp_file)

print("\n测试完成")