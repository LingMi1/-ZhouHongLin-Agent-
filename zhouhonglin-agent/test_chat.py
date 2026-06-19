import requests
import json

# 测试智能对话检索功能
url = "http://localhost:8001/api/rag/query"

# 测试查询商品参数
payload = {
    "question": "这个蓝牙音箱的续航时间是多少？",
    "collection_name": "product_knowledge",
    "top_k": 3
}

print("=" * 60)
print("测试智能对话检索功能")
print("=" * 60)

print(f"\n查询: {payload['question']}")

try:
    response = requests.post(url, json=payload, timeout=300)
    print(f"\n响应状态码: {response.status_code}")
    result = response.json()
    print(f"\n响应内容:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if "answer" in result and result["answer"]:
        print(f"\n[OK] 查询成功，返回了回答")
    else:
        print(f"\n[WARNING] 未返回回答")
        
except Exception as e:
    print(f"\n请求失败: {e}")

print("\n" + "=" * 60)