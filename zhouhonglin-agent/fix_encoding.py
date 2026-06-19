import re

# 读取文件
with open('e:/sgg1/shuyixiao-agent/src/zhouhonglin_agent/rag/rag_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换特殊字符
content = content.replace('✓ ', '[OK] ')
content = content.replace('⚠️  ', '[WARN] ')
content = content.replace('✗ ', '[ERR] ')

# 写回文件
with open('e:/sgg1/shuyixiao-agent/src/zhouhonglin_agent/rag/rag_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("编码修复完成")