import sys
import os

# 设置环境变量
os.environ['USE_CLOUD_EMBEDDING'] = 'false'

sys.path.insert(0, 'e:/sgg1/shuyixiao-agent/src')

print("=" * 60)
print("测试 RAG Agent 初始化")
print("=" * 60)

# 导入模块
print("\n1. 导入模块...")
try:
    from zhouhonglin_agent.config import settings
    print(f"配置加载成功")
    print(f"  use_cloud_embedding: {settings.use_cloud_embedding}")
    
    from zhouhonglin_agent.rag.vector_store import VectorStoreManager
    print(f"VectorStoreManager 导入成功")
    
    from zhouhonglin_agent.rag.document_loader import DocumentLoader
    print(f"DocumentLoader 导入成功")
    
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 创建 VectorStoreManager（不传入嵌入模型）
print("\n2. 创建 VectorStoreManager...")
try:
    vector_store = VectorStoreManager(
        collection_name="test_simple",
        persist_directory="e:/sgg1/shuyixiao-agent/data/chroma",
        embedding_manager=None  # 使用 Chroma 默认嵌入
    )
    print(f"VectorStoreManager 创建成功")
except Exception as e:
    print(f"VectorStoreManager 创建失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 创建 DocumentLoader
print("\n3. 创建 DocumentLoader...")
try:
    doc_loader = DocumentLoader()
    print(f"DocumentLoader 创建成功")
except Exception as e:
    print(f"DocumentLoader 创建失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 测试文本切分
print("\n4. 测试文本切分...")
test_text = """
商品名称：智能蓝牙音箱Pro版
商品型号：BT-SPK-2024-PRO
商品规格：黑色/白色/蓝色三种颜色可选
商品尺寸：150mm x 80mm x 60mm
"""

try:
    chunks = doc_loader.split_text(test_text)
    print(f"切分成功，片段数: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"  片段 {i+1}: {chunk.page_content[:50]}...")
except Exception as e:
    print(f"切分失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 写入向量库
print("\n5. 写入向量库...")
try:
    doc_ids = vector_store.add_documents(chunks)
    print(f"写入成功，返回 ID 数: {len(doc_ids)}")
except Exception as e:
    print(f"写入失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 检查文档数量
print("\n6. 检查文档数量...")
try:
    count = vector_store.get_document_count()
    print(f"文档数量: {count}")
except Exception as e:
    print(f"获取文档数量失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)