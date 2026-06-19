"""
电商智能客服知识库Agent系统: 基于 RAG 检索增强与 LangGraph Agent 的智能化客服解决方案
"""

__version__ = "1.0.0"
__author__ = "ecommerce-agent"

from .gitee_ai_client import GiteeAIClient
from .agents.simple_agent import SimpleAgent
from .config import settings

# RAG Agent 使用延迟导入，避免阻塞启动
# from .rag.rag_agent import RAGAgent

__all__ = [
    "GiteeAIClient",
    "SimpleAgent",
    # "RAGAgent",  # 延迟导入
    "settings",
]


def lazy_import_rag_agent():
    """延迟导入 RAG Agent"""
    from .rag.rag_agent import RAGAgent
    return RAGAgent

