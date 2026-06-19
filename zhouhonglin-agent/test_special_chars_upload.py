#!/usr/bin/env python3
"""测试上传包含特殊字符的文档"""

import sys
import os
import io
import requests

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("测试上传包含特殊字符的文档")
print("=" * 60)

# 创建测试文档
test_content = '''商品名称：智能蓝牙音箱"Pro版"
特性：支持"蓝牙5.3"、"WiFi6"、"NFC连接"
价格：¥299.00
描述：这款音箱拥有"卓越音质"和"超长续航"

产品参数：
- 尺寸：10" x 5" x 3"
- 重量：500g
- 功率：20W
- 续航时间：20小时

警告：请勿在"高温环境"下使用

用户评价：
"非常棒！音质很好" - 用户A
"物超所值，推荐购买" - 用户B
注意：产品包含"锂电池"，运输时需注意'''

# 写入临时文件
temp_file = "e:/sgg1/shuyixiao-agent/test_special.txt"
with open(temp_file, 'w', encoding='utf-8') as f:
    f.write(test_content)

print("\n1. 上传测试文件:")
url = "http://localhost:8001/api/rag/upload/files"

try:
    with open(temp_file, 'rb') as f:
        files = {'files': ('test_special.txt', f, 'text/plain')}
        data = {'collection_name': 'product_knowledge'}
        response = requests.post(url, files=files, data=data, timeout=60)
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   [OK] 上传成功")
        print(f"   文件数: {result.get('total_files', 0)}")
        print(f"   片段数: {result.get('total_chunks', 0)}")
    else:
        print(f"   [ERR] 上传失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 上传异常: {e}")

# 查询测试
print("\n2. 查询测试:")
url = "http://localhost:8001/api/rag/query"
data = {
    "question": '这款音箱的价格是多少？包含哪些特性？',
    "collection_name": "product_knowledge",
    "session_id": "test",
    "top_k": 3,
    "use_history": False,
    "optimize_query": False
}

try:
    response = requests.post(url, json=data, timeout=60)
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        answer = result.get('answer', '')
        print(f"   [OK] 查询成功")
        print(f"   回答: {answer[:300]}...")
    else:
        print(f"   [ERR] 查询失败: {response.text}")
        
except Exception as e:
    print(f"   [ERR] 查询异常: {e}")

# 清理临时文件
os.remove(temp_file)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)