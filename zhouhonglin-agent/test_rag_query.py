#!/usr/bin/env python3
"""测试 RAG 查询功能"""

import sys
import os
import requests
import json

print("=" * 60)
print("测试 RAG 查询功能")
print("=" * 60)

# 测试普通查询
url = "http://localhost:8001/api/rag/query"
data = {
    "question": "这个蓝牙音箱的续航时间是多少？",
    "collection_name": "product_knowledge",
    "session_id": "test",
    "top_k": 3,
    "use_history": False,
    "optimize_query": False
}

print(f"\n1. 测试 RAG 查询:")
print(f"   URL: {url}")
print(f"   问题: {data['question']}")

try:
    response = requests.post(url, json=data, timeout=60)
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 查询成功")
        print(f"   回答: {result.get('answer', '')[:200]}...")
    else:
        print(f"   [ERR] 查询失败")
        print(f"   错误: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 请求异常: {e}")

# 测试简单聊天
url2 = "http://localhost:8001/api/chat"
data2 = {
    "message": "你好",
    "agent_type": "simple",
    "session_id": "test"
}

print(f"\n2. 测试简单聊天:")
print(f"   URL: {url2}")
print(f"   问题: {data2['message']}")

try:
    response = requests.post(url2, json=data2, timeout=60)
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 聊天成功")
        print(f"   回答: {result.get('response', '')[:200]}...")
    else:
        print(f"   [ERR] 聊天失败")
        print(f"   错误: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 请求异常: {e}")

print("\n" + "=" * 60)