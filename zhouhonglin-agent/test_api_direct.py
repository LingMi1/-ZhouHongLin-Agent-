#!/usr/bin/env python3
"""测试 DeepSeek API 连通性"""

import sys
import os
import requests
import json

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zhouhonglin_agent.config import settings

print("=" * 60)
print("DeepSeek API 连通性测试")
print("=" * 60)

print("\n1. 配置信息:")
print(f"   API Key: {settings.gitee_ai_api_key}")
print(f"   Base URL: {settings.gitee_ai_base_url}")
print(f"   Model: {settings.gitee_ai_model}")

print("\n2. 执行测试请求:")
url = f"{settings.gitee_ai_base_url}/chat/completions"
headers = {
    "Authorization": f"Bearer {settings.gitee_ai_api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": settings.gitee_ai_model,
    "messages": [{"role": "user", "content": "你好"}]
}

print(f"   请求URL: {url}")
print(f"   请求头: Authorization: Bearer {settings.gitee_ai_api_key[:10]}...")
print(f"   请求体: {json.dumps(data, ensure_ascii=False)}")

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"\n3. 响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        print("   [OK] API 连通性测试成功！")
        result = response.json()
        print(f"\n4. 响应内容:")
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]
            print(f"   回答: {content}")
        if "usage" in result:
            usage = result["usage"]
            print(f"   Token使用: prompt={usage['prompt_tokens']}, completion={usage['completion_tokens']}, total={usage['total_tokens']}")
    else:
        print("   [ERR] API 连通性测试失败！")
        print(f"\n4. 错误详情:")
        try:
            error = response.json()
            print(f"   错误类型: {error.get('error', {}).get('type', 'unknown')}")
            print(f"   错误消息: {error.get('error', {}).get('message', response.text)}")
        except:
            print(f"   响应内容: {response.text}")
            
except Exception as e:
    print(f"\n   [ERR] 请求异常: {e}")

print("\n" + "=" * 60)