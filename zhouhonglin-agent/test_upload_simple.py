import requests
import json

# 上传文件测试
url = "http://localhost:8001/api/rag/upload/files"

# 创建测试文件内容
test_content = """
商品名称：智能蓝牙音箱Pro版
商品型号：BT-SPK-2024-PRO
商品规格：黑色/白色/蓝色三种颜色可选
商品尺寸：150mm x 80mm x 60mm
商品重量：净重350g，包装重量450g

商品特点：
1. 支持蓝牙5.0连接，传输距离可达10米
2. 内置2000mAh锂电池，续航时间8小时
3. IPX7防水等级，可浸泡水下1米深30分钟
"""

# 使用 files 参数上传
files = {
    'files': ('test_goods.txt', test_content.encode('utf-8'), 'text/plain')
}
data = {'collection_name': 'product_knowledge'}

print("正在上传文件...")
try:
    response = requests.post(url, files=files, data=data, timeout=120)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"上传失败: {e}")

# 检查集合列表
print("\n检查集合列表...")
try:
    collections_url = "http://localhost:8001/api/rag/collections"
    collections_response = requests.get(collections_url, timeout=30)
    print(f"集合列表: {json.dumps(collections_response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"获取集合列表失败: {e}")

# 检查文档列表
print("\n检查文档列表...")
try:
    docs_url = "http://localhost:8001/api/rag/documents/product_knowledge"
    docs_response = requests.get(docs_url, timeout=30)
    print(f"文档列表: {json.dumps(docs_response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"获取文档列表失败: {e}")