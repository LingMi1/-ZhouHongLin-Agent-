import requests

# 上传文件测试
url = "http://localhost:8001/api/rag/upload/files"
files = {"files": open("e:/sgg1/shuyixiao-agent/test_goods_intro.txt", "rb")}
data = {"collection_name": "product_knowledge"}

print("正在上传文件...")
response = requests.post(url, files=files, data=data)
print(f"响应状态码: {response.status_code}")
print(f"响应内容: {response.json()}")

# 检查集合列表
print("\n检查集合列表...")
collections_url = "http://localhost:8001/api/rag/collections"
collections_response = requests.get(collections_url)
print(f"集合列表: {collections_response.json()}")

# 检查文档列表
print("\n检查文档列表...")
docs_url = "http://localhost:8001/api/rag/documents/product_knowledge"
docs_response = requests.get(docs_url)
print(f"文档列表: {docs_response.json()}")