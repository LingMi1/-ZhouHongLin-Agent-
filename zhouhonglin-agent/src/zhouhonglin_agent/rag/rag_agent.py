"""
RAG Agent

集成所有 RAG 模块，提供完整的检索增强生成功能
"""

from typing import List, Dict, Any, Optional, Iterator
from pathlib import Path
from langchain_core.documents import Document

from .embeddings import EmbeddingManager, BatchEmbeddingManager
from .cloud_embeddings import CloudEmbeddingManager, BatchCloudEmbeddingManager
from .vector_store import VectorStoreManager
from .document_loader import DocumentLoader
from .retrievers import VectorRetriever, KeywordRetriever, HybridRetriever
from .query_optimizer import QueryOptimizer
from .reranker import Reranker, SimpleReranker, CloudReranker
from .context_manager import ContextManager

from ..gitee_ai_client import GiteeAIClient
from ..config import settings


class RAGAgent:
    """
    RAG Agent
    
    完整的检索增强生成 Agent，支持：
    - 文档加载和向量化
    - 多模态检索（向量、关键词、混合）
    - 查询优化
    - 重排序
    - 上下文管理
    - 流式响应
    - 云端/本地嵌入自动降级
    """
    
    def __init__(
        self,
        collection_name: str = "default",
        system_message: Optional[str] = None,
        use_reranker: bool = True,
        retrieval_mode: str = "hybrid",
        enable_query_optimization: bool = True,
        enable_context_expansion: bool = True,
        original_name: Optional[str] = None
    ):
        """
        初始化 RAG Agent
        
        Args:
            collection_name: 向量数据库集合名称（规范化后的名称）
            system_message: 系统消息
            use_reranker: 是否使用重排序
            retrieval_mode: 检索模式 (vector/keyword/hybrid)
            enable_query_optimization: 是否启用查询优化
            enable_context_expansion: 是否启用上下文扩展
            original_name: 原始名称（用于持久化映射关系）
        """
        self.collection_name = collection_name
        self.system_message = system_message or "你是一个有帮助的AI助手。请基于提供的文档内容回答用户的问题。"
        self.retrieval_mode = retrieval_mode
        
        print(f"正在初始化 RAG Agent (集合: {collection_name})...")
        
        # 1. 嵌入模型（优先使用云端服务，失败自动降级到本地模型）
        self.embedding_manager = None
        self._init_embedding()
        
        # 2. 向量存储
        self.vector_store = VectorStoreManager(
            collection_name=collection_name,
            embedding_manager=self.embedding_manager,
            original_name=original_name
        )
        
        # 3. 文档加载器
        self.document_loader = DocumentLoader()
        
        # 4. 检索器
        self.vector_retriever = VectorRetriever(self.vector_store)
        self.keyword_retriever = KeywordRetriever()
        self.hybrid_retriever = HybridRetriever(
            self.vector_retriever,
            self.keyword_retriever
        )
        
        # 5. 查询优化器
        self.query_optimizer = QueryOptimizer() if enable_query_optimization else None
        
        # 6. 重排序器（根据配置选择，默认不使用本地重排以减少启动时间）
        self._init_reranker(use_reranker)
        
        # 7. 上下文管理器
        self.context_manager = ContextManager(
            enable_expansion=enable_context_expansion
        )
        
        # 8. LLM 客户端
        self.llm_client = GiteeAIClient()
        
        # 对话历史
        self.chat_history: List[Dict[str, str]] = []
        
        print("RAG Agent 初始化完成！")
    
    def _init_embedding(self):
        """初始化嵌入模型，支持云端失败自动降级，最终使用 Chroma 默认嵌入"""
        # 优先尝试云端嵌入
        if settings.use_cloud_embedding:
            print("[OK] 尝试使用云端嵌入服务...")
            try:
                self.embedding_manager = BatchCloudEmbeddingManager(
                    model=settings.cloud_embedding_model
                )
                print("[OK] 云端嵌入服务初始化成功")
                return
            except Exception as e:
                print(f"[WARN] 云端嵌入服务初始化失败: {e}")
                print("[WARN] 将使用 Chroma 默认嵌入模型")
                self.embedding_manager = None
                return
        
        # 如果禁用云端嵌入，直接使用 Chroma 默认嵌入
        print("[OK] 使用 Chroma 默认嵌入模型（无需下载，启动最快）")
        self.embedding_manager = None
    
    def _init_reranker(self, use_reranker: bool):
        """初始化重排序器，根据配置选择合适的重排方式"""
        if not use_reranker:
            print("使用简单重排序器（无需下载模型，启动最快）")
            self.reranker = SimpleReranker()
            return
        
        # 优先使用云端重排序
        if settings.use_cloud_reranker:
            print("[OK] 使用云端重排序服务（无需下载模型，启动更快）")
            try:
                self.reranker = CloudReranker()
            except Exception as e:
                print(f"[WARN] 云端重排序服务初始化失败: {e}")
                print("[WARN] 降级到简单重排序器")
                self.reranker = SimpleReranker()
        # 仅在显式启用时使用本地重排序
        elif settings.use_local_reranker:
            print(f"使用本地重排序模型: {settings.reranker_model}（首次启动会下载模型文件）")
            try:
                self.reranker = Reranker(
                    model_name=settings.reranker_model,
                    device=settings.reranker_device
                )
            except Exception as e:
                print(f"[WARN] 本地重排序器初始化失败: {e}")
                print("[WARN] 降级到简单重排序器")
                self.reranker = SimpleReranker()
        else:
            print("使用简单重排序器（无需下载模型，启动最快）")
            self.reranker = SimpleReranker()
    
    def add_documents_from_file(
        self,
        file_path: str,
        show_progress: bool = True
    ) -> int:
        """
        从文件添加文档
        
        Args:
            file_path: 文件路径
            show_progress: 是否显示进度
            
        Returns:
            添加的文档片段数量
        """
        if show_progress:
            print(f"正在加载文件: {file_path}")
        
        chunks = self.document_loader.load_and_split(file_path)
        
        if show_progress:
            print(f"文档已分割为 {len(chunks)} 个片段")
            print("正在向量化并存储...")
        
        self.vector_store.add_documents(chunks)
        self.keyword_retriever.add_documents(chunks)
        
        if show_progress:
            print(f"成功添加 {len(chunks)} 个文档片段")
        
        return len(chunks)
    
    def add_documents_from_directory(
        self,
        directory_path: str,
        glob_pattern: str = "**/*.*",
        show_progress: bool = True
    ) -> int:
        """
        从目录批量添加文档
        
        Args:
            directory_path: 目录路径
            glob_pattern: 文件匹配模式
            show_progress: 是否显示进度
            
        Returns:
            添加的文档片段数量
        """
        if show_progress:
            print(f"正在加载目录: {directory_path}")
        
        chunks = self.document_loader.load_directory_and_split(
            directory_path,
            glob_pattern,
            show_progress
        )
        
        if show_progress:
            print("正在向量化并存储...")
        
        self.vector_store.add_documents(chunks)
        self.keyword_retriever.update_documents(chunks)
        
        if show_progress:
            print(f"成功添加 {len(chunks)} 个文档片段")
        
        return len(chunks)
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> int:
        """
        直接添加文本，支持嵌入失败自动降级
        
        Args:
            texts: 文本列表
            metadatas: 元数据列表
            
        Returns:
            添加的文档数量
        """
        print(f"\n{'='*60}")
        print(f"[RAGAgent.add_texts] 开始处理 {len(texts)} 个文本")
        print(f"{'='*60}")
        
        # 1. 文本切分
        all_chunks = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            chunks = self.document_loader.split_text(text, metadata)
            print(f"[RAGAgent.add_texts] 第 {i+1} 个文本切分为 {len(chunks)} 个片段")
            for j, chunk in enumerate(chunks):
                preview = chunk.page_content[:50] + "..." if len(chunk.page_content) > 50 else chunk.page_content
                print(f"[RAGAgent.add_texts]   片段 {j+1}: {preview}")
            all_chunks.extend(chunks)
        
        print(f"[RAGAgent.add_texts] 总共获得 {len(all_chunks)} 个文档片段")
        
        if not all_chunks:
            print(f"[RAGAgent.add_texts] 警告: 没有文档片段需要添加")
            return 0
        
        # 2. 批量写入向量库（vector_store 内部会处理嵌入失败降级）
        print(f"[RAGAgent.add_texts] 开始批量写入向量库...")
        
        try:
            doc_ids = self.vector_store.add_documents(all_chunks)
            print(f"[RAGAgent.add_texts] add_documents 返回值类型: {type(doc_ids)}")
            print(f"[RAGAgent.add_texts] add_documents 返回值: {doc_ids}")
            success_count = len(doc_ids) if doc_ids else 0
            print(f"[RAGAgent.add_texts] 批量写入成功，返回 {success_count} 个文档 ID")
        except Exception as e:
            print(f"[RAGAgent.add_texts] 批量写入失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 尝试切换到本地嵌入模型后重试
            error_str = str(e).lower()
            if "402" in str(e) or "余额" in str(e) or "timeout" in error_str or "network" in error_str or "连接" in error_str:
                print(f"[RAGAgent.add_texts] 云端嵌入失败，切换到本地嵌入模型...")
                self._switch_to_local_embedding()
                
                # 重新创建 vector_store
                self.vector_store = VectorStoreManager(
                    collection_name=self.collection_name,
                    embedding_manager=self.embedding_manager
                )
                
                # 重试写入
                try:
                    doc_ids = self.vector_store.add_documents(all_chunks)
                    success_count = len(doc_ids)
                    print(f"[RAGAgent.add_texts] 本地嵌入写入成功，返回 {success_count} 个文档 ID")
                except Exception as local_error:
                    print(f"[RAGAgent.add_texts] 本地嵌入写入也失败: {local_error}")
                    success_count = 0
            else:
                success_count = 0
        
        # 3. 更新关键词检索器
        print(f"[RAGAgent.add_texts] 更新关键词检索器...")
        self.keyword_retriever.add_documents(all_chunks)
        
        # 4. 获取最终文档数量
        final_count = self.vector_store.get_document_count()
        print(f"[RAGAgent.add_texts] 资料库 {self.collection_name} 最终文档总数: {final_count}")
        print(f"[RAGAgent.add_texts] 本次成功写入: {success_count} 个片段")
        print(f"{'='*60}\n")
        
        return success_count
    
    def _switch_to_local_embedding(self):
        """切换到本地嵌入模型"""
        print("正在切换到本地嵌入模型...")
        try:
            self.embedding_manager = BatchEmbeddingManager(
                model_name=settings.embedding_model,
                device=settings.embedding_device
            )
            print("[OK] 成功切换到本地嵌入模型")
        except Exception as e:
            print(f"[ERR] 切换本地嵌入模型失败: {e}")
            raise
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        mode: Optional[str] = None,
        use_rerank: bool = True
    ) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            mode: 检索模式 (vector/keyword/hybrid)
            use_rerank: 是否使用重排序
            
        Returns:
            相关文档列表
        """
        k = top_k or settings.retrieval_top_k
        retrieval_mode = mode or self.retrieval_mode
        
        if retrieval_mode == "vector":
            results = self.vector_retriever.retrieve(query, top_k=k)
        elif retrieval_mode == "keyword":
            results = self.keyword_retriever.retrieve(query, top_k=k)
        else:
            results = self.hybrid_retriever.retrieve(query, top_k=k)
        
        if use_rerank and self.reranker:
            results = self.reranker.rerank_results(
                query,
                results,
                top_k=settings.rerank_top_k
            )
        
        documents = [doc for doc, score in results]
        
        return documents
    
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        use_history: bool = True,
        optimize_query: bool = True,
        expand_context: bool = True,
        stream: bool = False
    ) -> str:
        """
        RAG 查询
        
        Args:
            question: 问题
            top_k: 检索文档数量
            use_history: 是否使用对话历史
            optimize_query: 是否优化查询
            expand_context: 是否扩展上下文
            stream: 是否流式输出
            
        Returns:
            回答文本（非流式）或 None（流式）
        """
        import json
        
        try:
            optimized_query = question
            if optimize_query and self.query_optimizer:
                history = self.chat_history[-5:] if use_history else None
                optimization_result = self.query_optimizer.optimize_query(
                    question,
                    history=history,
                    enable_expansion=False
                )
                optimized_query = optimization_result["rewritten_query"]
                print(f"优化后的查询: {optimized_query}")
            
            documents = self.retrieve(
                optimized_query,
                top_k=top_k,
                use_rerank=True
            )
            
            if not documents:
                no_doc_response = "抱歉，我在知识库中没有找到相关信息来回答您的问题。"
                if not stream:
                    return no_doc_response
                else:
                    return self._stream_response([no_doc_response])
            
            if expand_context:
                all_docs = []
                if hasattr(self.keyword_retriever, 'documents'):
                    all_docs = self.keyword_retriever.documents
                
                if all_docs:
                    documents = self.context_manager.expand_context(
                        documents,
                        all_docs
                    )
            
            prompt = self.context_manager.format_documents_for_prompt(
                documents,
                question,
                instruction="请基于以下文档内容回答问题。如果文档中没有相关信息，请如实说明。"
            )
            
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            if use_history and self.chat_history:
                # 验证对话历史的完整性
                try:
                    # 使用json.dumps验证消息结构是否合法
                    json.dumps(self.chat_history[-6:])
                    messages.extend(self.chat_history[-6:])
                except json.JSONDecodeError:
                    print("[WARN] 对话历史包含非法JSON，已清空")
                    self.clear_history()
            
            messages.append({"role": "user", "content": prompt})
            
            # 验证最终消息结构
            try:
                json.dumps(messages)
            except json.JSONDecodeError as e:
                print(f"[ERR] 消息结构JSON验证失败: {e}")
                print(f"[ERR] 消息内容: {messages}")
                self.clear_history()
                return "对话数据异常，已自动重置上下文。请重新提问。"
            
            if stream:
                return self._generate_stream(messages, question)
            else:
                response = self.llm_client.chat_completion(
                    messages=messages,
                    temperature=0.7
                )
                
                answer = response.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                
                self.chat_history.append({"role": "user", "content": question})
                self.chat_history.append({"role": "assistant", "content": answer})
                
                return answer
                
        except json.JSONDecodeError as e:
            print(f"[ERR] JSON解析异常: {e}")
            self.clear_history()
            return "对话数据异常，已自动重置上下文。请重新提问。"
        except Exception as e:
            print(f"[ERR] 查询异常: {e}")
            return f"查询失败: {str(e)}"
    
    def _generate_stream(
        self,
        messages: List[Dict[str, str]],
        question: str
    ) -> Iterator[str]:
        """
        生成流式响应
        
        Args:
            messages: 消息列表
            question: 问题
            
        Yields:
            响应片段
        """
        full_response = ""
        
        try:
            stream = self.llm_client.chat_completion(
                messages=messages,
                temperature=0.7,
                stream=True
            )
            
            for chunk in stream:
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    
                    if content:
                        full_response += content
                        yield content
            
            self.chat_history.append({"role": "user", "content": question})
            self.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"生成回答时出错: {str(e)}"
            yield error_msg
    
    def _stream_response(self, texts: List[str]) -> Iterator[str]:
        """
        将文本列表转换为流式输出
        
        Args:
            texts: 文本列表
            
        Yields:
            文本片段
        """
        for text in texts:
            yield text
    
    def clear_history(self):
        """清除对话历史"""
        self.chat_history = []
    
    def get_document_count(self) -> int:
        """获取文档数量"""
        return self.vector_store.get_document_count()
    
    def list_documents(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        列出知识库中的文档
        
        Args:
            limit: 返回文档数量限制
            offset: 偏移量
            
        Returns:
            文档列表
        """
        return self.vector_store.list_documents(limit=limit, offset=offset)
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            文档信息
        """
        return self.vector_store.get_document_by_id(doc_id)
    
    def delete_document(self, doc_id: str) -> bool:
        """
        删除指定文档（物理删除）
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            是否删除成功
        """
        success = self.vector_store.delete_document_by_id(doc_id)
        if success:
            all_docs = self.vector_store.list_documents()
            documents = [
                Document(page_content=doc['text'], metadata=doc['metadata'])
                for doc in all_docs
            ]
            self.keyword_retriever.update_documents(documents)
        return success
    
    def batch_delete_documents(self, doc_ids: List[str]) -> tuple:
        """
        批量删除文档（物理删除）
        
        Args:
            doc_ids: 要删除的文档ID列表
            
        Returns:
            (成功删除数量, 失败的文档ID列表)
        """
        success_count, failed_ids = self.vector_store.batch_delete_documents(doc_ids)
        
        all_docs = self.vector_store.list_documents()
        documents = [
            Document(page_content=doc['text'], metadata=doc['metadata'])
            for doc in all_docs
        ]
        self.keyword_retriever.update_documents(documents)
        
        return success_count, failed_ids
    
    def clear_knowledge_base(self):
        """清空知识库"""
        self.vector_store.clear()
        self.keyword_retriever.update_documents([])
        print("知识库已清空")
