#!/usr/bin/env python3
"""完整流程测试：清空 -> 上传 -> 验证"""

import sys
import io
import requests
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8001"

time.sleep(1)

# 1. 查看 test 集合当前状态
print("1. 查看 test 集合当前状态:")
url = f"{API_BASE}/api/rag/collections"
response = requests.get(url, timeout=10)
if response.status_code == 200:
    data = response.json()
    for coll in data.get('collections', []):
        if coll.get('collection_name') == 'test':
            print(f"   当前文档数: {coll.get('document_count', 0)}")

# 2. 清空 test 集合
print("\n2. 清空 test 集合:")
url = f"{API_BASE}/api/rag/collections/test/clear"
response = requests.delete(url, timeout=10)
print(f"   状态码: {response.status_code}")
print(f"   响应: {response.text}")

# 3. 验证清空结果
print("\n3. 验证清空结果:")
url = f"{API_BASE}/api/rag/collections"
response = requests.get(url, timeout=10)
if response.status_code == 200:
    data = response.json()
    for coll in data.get('collections', []):
        if coll.get('collection_name') == 'test':
            print(f"   清空后文档数: {coll.get('document_count', 0)}")

# 4. 上传文件
print("\n4. 上传文件:")
test_content = "商品名称：测试商品A\n价格：¥100\n库存：100"
temp_file = "e:/sgg1/test_upload.txt"
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

url = f"{API_BASE}/api/rag/upload/files"
with open(temp_file, 'rb') as f:
    files = {'files': ('test_upload.txt', f, 'text/plain')}
    data = {'collection_name': 'test'}
    response = requests.post(url, files=files, data=data, timeout=60)

print(f"   状态码: {response.status_code}")
print(f"   响应: {response.text}")

# 5. 验证上传结果
print("\n5. 验证上传结果:")
url = f"{API_BASE}/api/rag/collections"
response = requests.get(url, timeout=10)
if response.status_code == 200:
    data = response.json()
    for coll in data.get('collections', []):
        if coll.get('collection_name') == 'test':
            print(f"   上传后文档数: {coll.get('document_count', 0)}")

# 6. 查看文档列表
print("\n6. 查看 test 库文档列表:")
url = f"{API_BASE}/api/rag/documents/test?limit=10"
response = requests.get(url, timeout=10)
if response.status_code == 200:
    docs = response.json()
    print(f"   文档数量: {len(docs)}")
    for doc in docs[:3]:
        print(f"   ID: {doc.get('id', '')}")
        content = doc.get('content', '')[:100]
        print(f"   Content: {content}")

# 清理
import os
os.remove(temp_file)

print("\n测试完成")