#!/usr/bin/env python3
"""直接测试 GiteeAI 客户端"""

import sys
import os
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zhouhonglin_agent.gitee_ai_client import GiteeAIClient

print("=" * 60)
print("测试 GiteeAI 客户端")
print("=" * 60)

try:
    client = GiteeAIClient()
    print(f"[OK] 客户端初始化成功")
    print(f"   API Key: {client.api_key[:10]}...")
    print(f"   Base URL: {client.base_url}")
    print(f"   Model: {client.model}")
    
    # 测试简单对话
    messages = [{"role": "user", "content": "你好"}]
    print(f"\n[INFO] 发送测试消息...")
    
    response = client.chat_completion(messages, temperature=0.7)
    
    if "choices" in response:
        content = response["choices"][0]["message"]["content"]
        # 移除emoji字符
        safe_content = content.replace('\U0001f60a', '').replace('\U0001f44d', '')
        print(f"[OK] 收到回复: {safe_content[:100]}...")
        
        if "usage" in response:
            usage = response["usage"]
            print(f"[INFO] Token使用: prompt={usage['prompt_tokens']}, completion={usage['completion_tokens']}, total={usage['total_tokens']}")
    else:
        print(f"[ERR] 响应格式异常: {response}")
        
except Exception as e:
    print(f"[ERR] 测试失败: {e}")

print("\n" + "=" * 60)