"""
向量存储管理器

提供向量数据库的统一接口，支持 ChromaDB
使用原生 ChromaDB API 直接写入，避免 LangChain 封装层问题
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import uuid
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_core.documents import Document

from ..config import settings

_chroma_clients = {}


class VectorStoreManager:
    """
    向量存储管理器
    
    封装 ChromaDB 的操作，使用原生 API 直接写入向量
    当嵌入模型无法加载时，使用 Chroma 默认嵌入模型
    """
    
    def __init__(
        self,
        collection_name: str = "default",
        persist_directory: Optional[str] = None,
        embedding_manager: Optional[Any] = None,
        original_name: Optional[str] = None
    ):
        """
        初始化向量存储管理器
        
        Args:
            collection_name: 集合名称（规范化后的名称）
            persist_directory: 持久化目录
            embedding_manager: 嵌入模型管理器（可选，不传则使用 Chroma 默认嵌入）
            original_name: 原始名称（用户输入的名称，用于映射恢复）
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory or settings.vector_db_path
        self.embedding_manager = embedding_manager
        self.use_default_embedding = False
        
        print(f"\n{'='*60}")
        print(f"[VectorStore] 初始化向量存储")
        print(f"[VectorStore] 集合名称: {collection_name}")
        print(f"[VectorStore] 持久化目录: {self.persist_directory}")
        print(f"{'='*60}")
        
        # 确保持久化目录存在
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # 使用全局客户端缓存，避免重复创建
        if self.persist_directory not in _chroma_clients:
            _chroma_clients[self.persist_directory] = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
        
        self.client = _chroma_clients[self.persist_directory]
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
            )
            doc_count = self.collection.count()
            print(f"[VectorStore] 已加载现有集合: {collection_name}, 当前文档数: {doc_count}")
        except Exception:
            # 创建集合时保存原始名称到metadata
            collection_metadata = {"hnsw:space": "cosine"}
            
            if original_name and original_name != collection_name:
                collection_metadata["original_name"] = original_name
                print(f"[VectorStore] 已创建新集合: {collection_name} (原始名称: {original_name})")
            else:
                print(f"[VectorStore] 已创建新集合: {collection_name}")
            
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata=collection_metadata
            )
        
        # 检查嵌入模型
        if self.embedding_manager is None:
            print(f"[VectorStore] 未传入嵌入模型，将使用 Chroma 默认嵌入模型")
            self.use_default_embedding = True
        else:
            print(f"[VectorStore] 嵌入模型类型: {type(self.embedding_manager).__name__}")
        
        print(f"[VectorStore] 初始化完成")
        print(f"{'='*60}\n")
    
    def _generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        生成文本嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量列表，如果使用 Chroma 默认嵌入则返回 None
        """
        # 如果使用 Chroma 默认嵌入，返回 None（让 Chroma 自己生成）
        if self.use_default_embedding or self.embedding_manager is None:
            print(f"[VectorStore] 使用 Chroma 默认嵌入模型，文本数量: {len(texts)}")
            return None
        
        print(f"[VectorStore] 开始生成嵌入向量，文本数量: {len(texts)}")
        
        try:
            embeddings = self.embedding_manager.embed_documents(texts)
            print(f"[VectorStore] 嵌入向量生成成功，向量数量: {len(embeddings)}")
            if embeddings:
                print(f"[VectorStore] 向量维度: {len(embeddings[0])}")
            return embeddings
        except Exception as e:
            print(f"[VectorStore] 嵌入向量生成失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 嵌入失败时，使用 Chroma 默认嵌入
            print(f"[VectorStore] 切换到 Chroma 默认嵌入模型...")
            self.use_default_embedding = True
            return None
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        添加文档到向量存储（使用原生 ChromaDB API）
        
        Args:
            documents: 文档列表
            ids: 文档 ID 列表
            
        Returns:
            文档 ID 列表
        """
        if not documents:
            print(f"[VectorStore] 警告: 没有文档需要添加")
            return []
        
        print(f"\n{'='*60}")
        print(f"[VectorStore] 开始添加文档")
        print(f"[VectorStore] 文档数量: {len(documents)}")
        print(f"{'='*60}")
        
        # 提取文本和元数据
        texts = []
        metadatas = []
        doc_ids = []
        
        for i, doc in enumerate(documents):
            text = doc.page_content
            if not text or not text.strip():
                print(f"[VectorStore] 跳过第 {i} 个空文档")
                continue
            
            texts.append(text)
            # 确保 metadata 是非空字典（ChromaDB 要求）
            metadata = doc.metadata if (doc.metadata and len(doc.metadata) > 0) else {"source": f"doc_{i}"}
            metadatas.append(metadata)
            
            # 生成唯一 ID
            if ids and i < len(ids):
                doc_ids.append(ids[i])
            else:
                doc_ids.append(str(uuid.uuid4()))
        
        if not texts:
            print(f"[VectorStore] 所有文档内容为空，无法添加")
            return []
        
        print(f"[VectorStore] 有效文本数量: {len(texts)}")
        
        # 打印前几个文本预览
        for i, text in enumerate(texts[:3]):
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"[VectorStore] 文本 {i+1} 预览: {preview}")
        
        # 生成嵌入向量（可能返回 None，表示使用 Chroma 默认嵌入）
        embeddings = self._generate_embeddings(texts)
        
        # 使用原生 ChromaDB API 写入
        print(f"[VectorStore] 开始写入 ChromaDB...")
        try:
            # 如果 embeddings 为 None，Chroma 会使用默认嵌入模型
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=doc_ids
            )
            
            # 验证写入结果
            final_count = self.collection.count()
            print(f"[VectorStore] 写入完成，集合当前文档总数: {final_count}")
            print(f"[VectorStore] 本次添加文档数: {len(doc_ids)}")
            print(f"[VectorStore] 返回 ID 数: {len(doc_ids)}")
            print(f"{'='*60}\n")
            
            return doc_ids
        except Exception as e:
            print(f"[VectorStore] ChromaDB 写入失败: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        添加文本到向量存储
        
        Args:
            texts: 文本列表
            metadatas: 元数据列表
            ids: 文档 ID 列表
            
        Returns:
            文档 ID 列表
        """
        if not texts:
            return []
        
        # 转换为 Document 对象
        documents = []
        for i, text in enumerate(texts):
            if not text or not text.strip():
                continue
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))
        
        return self.add_documents(documents, ids)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            filter: 元数据过滤条件
            
        Returns:
            相关文档列表
        """
        # 使用 Chroma 默认嵌入进行查询
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=filter
        )
        
        # 转换为 Document 对象
        documents = []
        if results and results.get('ids'):
            ids = results['ids'][0]
            texts = results['documents'][0] if results.get('documents') else []
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            
            for i, doc_id in enumerate(ids):
                documents.append(Document(
                    page_content=texts[i] if i < len(texts) else '',
                    metadata=metadatas[i] if i < len(metadatas) else {}
                ))
        
        return documents
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        相似度搜索并返回分数
        
        Args:
            query: 查询文本
            k: 返回结果数量
            filter: 元数据过滤条件
            
        Returns:
            (文档, 相似度分数) 元组列表
        """
        # 使用 Chroma 默认嵌入进行查询
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=filter,
            include=['documents', 'metadatas', 'distances']
        )
        
        # 转换为 (Document, score) 元组
        doc_score_pairs = []
        if results and results.get('ids'):
            ids = results['ids'][0]
            texts = results['documents'][0] if results.get('documents') else []
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            distances = results['distances'][0] if results.get('distances') else []
            
            for i, doc_id in enumerate(ids):
                doc = Document(
                    page_content=texts[i] if i < len(texts) else '',
                    metadata=metadatas[i] if i < len(metadatas) else {}
                )
                score = 1 - distances[i] if i < len(distances) else 0  # 转换距离为相似度
                doc_score_pairs.append((doc, score))
        
        return doc_score_pairs
    
    def delete_documents(self, ids: List[str]) -> None:
        """
        删除文档
        
        Args:
            ids: 要删除的文档 ID 列表
        """
        if not ids:
            return
        
        self.collection.delete(ids=ids)
        print(f"[VectorStore] 已删除 {len(ids)} 个文档")
    
    def get_document_count(self) -> int:
        """获取文档数量"""
        count = self.collection.count()
        print(f"[VectorStore] 集合 {self.collection_name} 文档数量: {count}")
        return count
    
    def list_documents(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        列出集合中的文档
        
        Args:
            limit: 返回文档数量限制
            offset: 偏移量
            
        Returns:
            文档列表，每个文档包含 id, text, metadata
        """
        try:
            print(f"[VectorStore] 列出文档，limit={limit}, offset={offset}")
            
            # 获取文档
            results = self.collection.get(
                limit=limit,
                offset=offset,
                include=['documents', 'metadatas']
            )
            
            documents = []
            ids = results.get('ids', [])
            texts = results.get('documents', [])
            metadatas = results.get('metadatas', [])
            
            print(f"[VectorStore] 获取到 {len(ids)} 个文档")
            
            for i, doc_id in enumerate(ids):
                documents.append({
                    'id': doc_id,
                    'text': texts[i] if i < len(texts) else '',
                    'metadata': metadatas[i] if i < len(metadatas) else {}
                })
            
            return documents
        except Exception as e:
            print(f"[VectorStore] 列出文档时出错: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取单个文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            文档信息字典，包含 id, text, metadata
        """
        try:
            results = self.collection.get(
                ids=[doc_id],
                include=['documents', 'metadatas']
            )
            
            if results and results.get('ids'):
                return {
                    'id': results['ids'][0],
                    'text': results['documents'][0] if results.get('documents') else '',
                    'metadata': results['metadatas'][0] if results.get('metadatas') else {}
                }
            return None
        except Exception as e:
            print(f"[VectorStore] 获取文档时出错: {e}")
            return None
    
    def delete_document_by_id(self, doc_id: str) -> bool:
        """
        根据 ID 删除单个文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            是否删除成功
        """
        try:
            self.collection.delete(ids=[doc_id])
            print(f"[VectorStore] 已删除文档: {doc_id}")
            return True
        except Exception as e:
            print(f"[VectorStore] 删除文档时出错: {e}")
            return False
    
    def batch_delete_documents(self, doc_ids: List[str]) -> Tuple[int, List[str]]:
        """
        批量删除文档
        
        Args:
            doc_ids: 要删除的文档ID列表
            
        Returns:
            (成功删除数量, 失败的文档ID列表)
        """
        success_count = 0
        failed_ids = []
        
        try:
            self.collection.delete(ids=doc_ids)
            success_count = len(doc_ids)
            print(f"[VectorStore] 已批量删除 {success_count} 个文档")
        except Exception as e:
            print(f"[VectorStore] 批量删除失败: {e}，尝试逐个删除...")
            for doc_id in doc_ids:
                if self.delete_document_by_id(doc_id):
                    success_count += 1
                else:
                    failed_ids.append(doc_id)
        
        return success_count, failed_ids
    
    def clear(self) -> None:
        """清空集合"""
        try:
            self.client.delete_collection(name=self.collection_name)
            
            # 重新创建空集合
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            print(f"[VectorStore] 已清空集合: {self.collection_name}")
        except Exception as e:
            print(f"[VectorStore] 清空集合时出错: {e}")
    
    def get_retriever(self, **kwargs):
        """获取检索器（兼容旧接口）"""
        from langchain_community.vectorstores import Chroma
        
        vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_manager
        )
        return vectorstore.as_retriever(**kwargs)
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        生成文本嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量列表，如果使用 Chroma 默认嵌入则返回 None
        """
        print(f"[VectorStore] 开始生成嵌入向量，文本数量: {len(texts)}")
        
        # 如果嵌入模型为 None，返回 None（让 Chroma 使用默认嵌入）
        if self.embedding_manager is None:
            print(f"[VectorStore] 使用 Chroma 默认嵌入模型，返回 None")
            return None
        
        try:
            embeddings = self.embedding_manager.embed_documents(texts)
            print(f"[VectorStore] 嵌入向量生成成功，向量数量: {len(embeddings)}")
            if embeddings:
                print(f"[VectorStore] 向量维度: {len(embeddings[0])}")
            return embeddings
        except Exception as e:
            print(f"[VectorStore] 嵌入向量生成失败: {e}")
            
            # 嵌入失败时，使用 Chroma 默认嵌入
            print(f"[VectorStore] 切换到 Chroma 默认嵌入模型...")
            self.embedding_manager = None
            return None
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        添加文档到向量存储（使用原生 ChromaDB API）
        
        Args:
            documents: 文档列表
            ids: 文档 ID 列表
            
        Returns:
            文档 ID 列表
        """
        if not documents:
            print(f"[VectorStore] 警告: 没有文档需要添加")
            return []
        
        print(f"\n{'='*60}")
        print(f"[VectorStore] 开始添加文档")
        print(f"[VectorStore] 文档数量: {len(documents)}")
        print(f"{'='*60}")
        
        # 提取文本和元数据
        texts = []
        metadatas = []
        doc_ids = []
        
        for i, doc in enumerate(documents):
            text = doc.page_content
            if not text or not text.strip():
                print(f"[VectorStore] 跳过第 {i} 个空文档")
                continue
            
            texts.append(text)
            # 确保 metadata 是非空字典（ChromaDB 要求）
            metadata = doc.metadata if (doc.metadata and len(doc.metadata) > 0) else {"source": f"doc_{i}"}
            metadatas.append(metadata)
            
            # 生成唯一 ID
            if ids and i < len(ids):
                doc_ids.append(ids[i])
            else:
                doc_ids.append(str(uuid.uuid4()))
        
        if not texts:
            print(f"[VectorStore] 所有文档内容为空，无法添加")
            return []
        
        print(f"[VectorStore] 有效文本数量: {len(texts)}")
        
        # 打印前几个文本预览
        for i, text in enumerate(texts[:3]):
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"[VectorStore] 文本 {i+1} 预览: {preview}")
        
        # 生成嵌入向量（可能返回 None，表示使用 Chroma 默认嵌入）
        embeddings = self._generate_embeddings(texts)
        
        # 如果 embeddings 为 None，Chroma 会使用默认嵌入模型
        # 如果 embeddings 不为 None，需要检查数量是否匹配
        if embeddings is not None and len(embeddings) != len(texts):
            print(f"[VectorStore] 错误: 嵌入向量数量与文本数量不匹配")
            print(f"[VectorStore] 文本数量: {len(texts)}, 向量数量: {len(embeddings)}")
            return []
        
        # 使用原生 ChromaDB API 写入
        print(f"[VectorStore] 开始写入 ChromaDB...")
        if embeddings is None:
            print(f"[VectorStore] 不传入嵌入向量，让 Chroma 使用默认嵌入模型")
        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=doc_ids
            )
            
            # 验证写入结果
            final_count = self.collection.count()
            print(f"[VectorStore] 写入完成，集合当前文档总数: {final_count}")
            print(f"[VectorStore] 本次添加文档数: {len(doc_ids)}")
            print(f"[VectorStore] 返回 ID 数: {len(doc_ids)}")
            print(f"{'='*60}\n")
            
            return doc_ids
        except Exception as e:
            print(f"[VectorStore] ChromaDB 写入失败: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        添加文本到向量存储
        
        Args:
            texts: 文本列表
            metadatas: 元数据列表
            ids: 文档 ID 列表
            
        Returns:
            文档 ID 列表
        """
        if not texts:
            return []
        
        # 转换为 Document 对象
        documents = []
        for i, text in enumerate(texts):
            if not text or not text.strip():
                continue
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))
        
        return self.add_documents(documents, ids)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            filter: 元数据过滤条件
            
        Returns:
            相关文档列表
        """
        # 如果有嵌入模型，使用 query_embeddings；否则使用 query_texts（Chroma 默认嵌入）
        if self.embedding_manager is not None:
            query_embedding = self.embedding_manager.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter
            )
        else:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=filter
            )
        
        # 转换为 Document 对象
        documents = []
        if results and results.get('ids'):
            ids = results['ids'][0]
            texts = results['documents'][0] if results.get('documents') else []
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            
            for i, doc_id in enumerate(ids):
                documents.append(Document(
                    page_content=texts[i] if i < len(texts) else '',
                    metadata=metadatas[i] if i < len(metadatas) else {}
                ))
        
        return documents
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        相似度搜索并返回分数
        
        Args:
            query: 查询文本
            k: 返回结果数量
            filter: 元数据过滤条件
            
        Returns:
            (文档, 相似度分数) 元组列表
        """
        # 如果有嵌入模型，使用 query_embeddings；否则使用 query_texts（Chroma 默认嵌入）
        if self.embedding_manager is not None:
            query_embedding = self.embedding_manager.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter,
                include=['documents', 'metadatas', 'distances']
            )
        else:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=filter,
                include=['documents', 'metadatas', 'distances']
            )
        
        # 转换为 (Document, score) 元组
        doc_score_pairs = []
        if results and results.get('ids'):
            ids = results['ids'][0]
            texts = results['documents'][0] if results.get('documents') else []
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            distances = results['distances'][0] if results.get('distances') else []
            
            for i, doc_id in enumerate(ids):
                doc = Document(
                    page_content=texts[i] if i < len(texts) else '',
                    metadata=metadatas[i] if i < len(metadatas) else {}
                )
                score = 1 - distances[i] if i < len(distances) else 0  # 转换距离为相似度
                doc_score_pairs.append((doc, score))
        
        return doc_score_pairs
    
    def delete_documents(self, ids: List[str]) -> None:
        """
        删除文档
        
        Args:
            ids: 要删除的文档 ID 列表
        """
        if not ids:
            return
        
        self.collection.delete(ids=ids)
        print(f"[VectorStore] 已删除 {len(ids)} 个文档")
    
    def get_document_count(self) -> int:
        """获取文档数量"""
        count = self.collection.count()
        print(f"[VectorStore] 集合 {self.collection_name} 文档数量: {count}")
        return count
    
    def list_documents(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        列出集合中的文档
        
        Args:
            limit: 返回文档数量限制
            offset: 偏移量
            
        Returns:
            文档列表，每个文档包含 id, text, metadata
        """
        try:
            print(f"[VectorStore] 列出文档，limit={limit}, offset={offset}")
            
            # 获取文档
            results = self.collection.get(
                limit=limit,
                offset=offset,
                include=['documents', 'metadatas']
            )
            
            documents = []
            ids = results.get('ids', [])
            texts = results.get('documents', [])
            metadatas = results.get('metadatas', [])
            
            print(f"[VectorStore] 获取到 {len(ids)} 个文档")
            
            for i, doc_id in enumerate(ids):
                documents.append({
                    'id': doc_id,
                    'text': texts[i] if i < len(texts) else '',
                    'metadata': metadatas[i] if i < len(metadatas) else {}
                })
            
            return documents
        except Exception as e:
            print(f"[VectorStore] 列出文档时出错: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取单个文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            文档信息字典，包含 id, text, metadata
        """
        try:
            results = self.collection.get(
                ids=[doc_id],
                include=['documents', 'metadatas']
            )
            
            if results and results.get('ids'):
                return {
                    'id': results['ids'][0],
                    'text': results['documents'][0] if results.get('documents') else '',
                    'metadata': results['metadatas'][0] if results.get('metadatas') else {}
                }
            return None
        except Exception as e:
            print(f"[VectorStore] 获取文档时出错: {e}")
            return None
    
    def delete_document_by_id(self, doc_id: str) -> bool:
        """
        根据 ID 删除单个文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            是否删除成功
        """
        try:
            self.collection.delete(ids=[doc_id])
            print(f"[VectorStore] 已删除文档: {doc_id}")
            return True
        except Exception as e:
            print(f"[VectorStore] 删除文档时出错: {e}")
            return False
    
    def batch_delete_documents(self, doc_ids: List[str]) -> Tuple[int, List[str]]:
        """
        批量删除文档
        
        Args:
            doc_ids: 要删除的文档ID列表
            
        Returns:
            (成功删除数量, 失败的文档ID列表)
        """
        success_count = 0
        failed_ids = []
        
        try:
            self.collection.delete(ids=doc_ids)
            success_count = len(doc_ids)
            print(f"[VectorStore] 已批量删除 {success_count} 个文档")
        except Exception as e:
            print(f"[VectorStore] 批量删除失败: {e}，尝试逐个删除...")
            for doc_id in doc_ids:
                if self.delete_document_by_id(doc_id):
                    success_count += 1
                else:
                    failed_ids.append(doc_id)
        
        return success_count, failed_ids
    
    def clear(self) -> None:
        """清空集合"""
        try:
            self.client.delete_collection(name=self.collection_name)
            
            # 重新创建空集合
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            print(f"[VectorStore] 已清空集合: {self.collection_name}")
        except Exception as e:
            print(f"[VectorStore] 清空集合时出错: {e}")
    
    def get_retriever(self, **kwargs):
        """获取检索器（兼容旧接口）"""
        from langchain_community.vectorstores import Chroma
        
        vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_manager
        )
        return vectorstore.as_retriever(**kwargs)