#!/usr/bin/env python3
"""简单测试上传功能"""

import sys
import io
import requests
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_BASE = "http://localhost:8001"

time.sleep(1)

# 上传文件到 test 库
print("1. 上传文件:")
url = f"{API_BASE}/api/rag/upload/files"

test_content = "商品名称：测试商品A\n价格：¥100\n库存：100"
temp_file = "e:/sgg1/test.txt"
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

with open(temp_file, 'rb') as f:
    files = {'files': ('test.txt', f, 'text/plain')}
    data = {'collection_name': 'test'}
    response = requests.post(url, files=files, data=data, timeout=60)

print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 查看集合
print("\n2. 查看集合:")
url = f"{API_BASE}/api/rag/collections"
response = requests.get(url, timeout=10)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 清理
import os
os.remove(temp_file)

print("\n完成")