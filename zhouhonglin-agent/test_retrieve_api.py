import requests
import json

# 测试检索功能（不调用 LLM）
url = "http://localhost:8001/api/rag/documents/product_knowledge"

print("=" * 60)
print("测试文档列表接口")
print("=" * 60)

try:
    response = requests.get(url, timeout=60)
    print(f"\n响应状态码: {response.status_code}")
    result = response.json()
    print(f"\n文档总数: {result.get('total_count', 0)}")
    print(f"文档列表:")
    for i, doc in enumerate(result.get('documents', [])[:3]):
        print(f"  文档 {i+1}: {doc['text'][:80]}...")
except Exception as e:
    print(f"\n请求失败: {e}")

print("\n" + "=" * 60)