from sentence_transformers import SentenceTransformer

# 测试本地嵌入模型
print("测试本地嵌入模型...")

model = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")
print(f"模型加载成功，维度: {model.get_sentence_embedding_dimension()}")

# 测试嵌入
texts = ["这是测试文本1", "这是测试文本2"]
embeddings = model.encode(texts)
print(f"嵌入向量数量: {len(embeddings)}")
print(f"向量维度: {len(embeddings[0])}")
print("测试完成！")