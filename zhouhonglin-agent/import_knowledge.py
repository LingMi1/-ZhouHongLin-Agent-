#!/usr/bin/env python
"""
批量导入电商知识库文档到product_knowledge资料库
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.zhouhonglin_agent.rag.vector_store import VectorStoreManager

def main():
    # 文档目录
    docs_dir = os.path.join(os.path.dirname(__file__), "docs", "ecommerce_kb")
    
    # 要导入的文档
    documents = {
        "goods_intro.txt": "商品介绍文档",
        "after_sale_policy.txt": "售后政策文档",
        "logistics_rules.txt": "物流配送文档",
        "promotion_rules.txt": "促销活动文档",
        "faq.txt": "常见问题FAQ文档"
    }
    
    print("=" * 60)
    print("批量导入电商知识库文档")
    print("=" * 60)
    print()
    
    # 初始化向量存储管理器
    collection_name = "product_knowledge"
    print(f"[INFO] 初始化资料库: {collection_name}")
    print()
    
    try:
        # 创建向量存储实例
        vector_store = VectorStoreManager(
            collection_name=collection_name,
            original_name=collection_name
        )
        print(f"[OK] 资料库初始化成功")
        
        total_chunks = 0
        
        for filename, description in documents.items():
            filepath = os.path.join(docs_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"[WARN] 文件不存在: {filepath}")
                continue
            
            print(f"[INFO] 正在导入: {description} ({filename})")
            
            # 读取文件内容
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"[WARN] 文件内容为空: {filename}")
                continue
            
            # 添加到向量存储
            chunks = vector_store.add_texts([content])
            chunk_count = len(chunks) if chunks else 1
            total_chunks += chunk_count
            
            print(f"[OK] {description} 导入成功，生成 {chunk_count} 个文档片段")
        
        print()
        print("=" * 60)
        print("导入完成！")
        print("=" * 60)
        print(f"资料库名称: {collection_name}")
        print(f"文档总数: {len(documents)} 个文件")
        print(f"文档片段: {total_chunks} 个")
        print(f"资料库路径: {vector_store.persist_directory}")
        
    except Exception as e:
        print(f"[ERROR] 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
