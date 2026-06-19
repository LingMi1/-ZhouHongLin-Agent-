"""
Tool Use Agent - 基于 Agentic Design Patterns 的工具使用智能体

实现了完整的工具调用框架，支持：
- 动态工具注册和发现
- 智能工具选择和参数推理
- 工具执行结果处理
- 工具链式调用
- 错误处理和重试机制
"""

import json
import logging
import traceback
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import inspect
import asyncio
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolType(Enum):
    """工具类型枚举"""
    FILE_OPERATION = "file_operation"      # 文件操作
    NETWORK_REQUEST = "network_request"    # 网络请求
    DATA_PROCESSING = "data_processing"    # 数据处理
    SYSTEM_INFO = "system_info"           # 系统信息
    CALCULATION = "calculation"           # 计算工具
    TEXT_PROCESSING = "text_processing"   # 文本处理
    CUSTOM = "custom"                     # 自定义工具


@dataclass
class ToolParameter:
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum_values: Optional[List[str]] = None


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    description: str
    function: Callable
    parameters: List[ToolParameter]
    tool_type: ToolType = ToolType.CUSTOM
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    async_support: bool = False


@dataclass
class ToolExecutionResult:
    """工具执行结果"""
    success: bool
    result: Any = None
    error_message: str = ""
    execution_time: float = 0.0
    tool_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolCallPlan:
    """工具调用计划"""
    tool_name: str
    parameters: Dict[str, Any]
    reasoning: str = ""
    confidence: float = 1.0


class ToolUseAgent:
    """Tool Use Agent - 工具使用智能体"""
    
    def __init__(self, llm_client, verbose: bool = False):
        """
        初始化 Tool Use Agent
        
        Args:
            llm_client: LLM 客户端
            verbose: 是否输出详细日志
        """
        self.llm_client = llm_client
        self.verbose = verbose
        self.tools: Dict[str, ToolDefinition] = {}
        self.execution_history: List[ToolExecutionResult] = []
        
        if self.verbose:
            logger.info("🔧 Tool Use Agent 初始化完成")
    
    def register_tool(self, tool_def: ToolDefinition) -> None:
        """注册工具"""
        self.tools[tool_def.name] = tool_def
        if self.verbose:
            logger.info(f"✅ 注册工具: {tool_def.name} ({tool_def.tool_type.value})")
    
    def register_function_as_tool(
        self, 
        func: Callable, 
        name: Optional[str] = None,
        description: Optional[str] = None,
        tool_type: ToolType = ToolType.CUSTOM,
        examples: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> None:
        """将Python函数注册为工具"""
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"执行函数 {func.__name__}"
        
        # 自动解析函数参数
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # 默认类型
            required = param.default == inspect.Parameter.empty
            default_value = None if required else param.default
            
            # 尝试从类型注解推断类型
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
                elif param.annotation == dict:
                    param_type = "object"
            
            parameters.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=f"参数 {param_name}",
                required=required,
                default=default_value
            ))
        
        tool_def = ToolDefinition(
            name=tool_name,
            description=tool_description,
            function=func,
            parameters=parameters,
            tool_type=tool_type,
            examples=examples or [],
            tags=tags or [],
            async_support=asyncio.iscoroutinefunction(func)
        )
        
        self.register_tool(tool_def)
    
    def get_available_tools(self, tool_type: Optional[ToolType] = None) -> List[Dict[str, Any]]:
        """获取可用工具列表"""
        tools = []
        for tool_name, tool_def in self.tools.items():
            if tool_type is None or tool_def.tool_type == tool_type:
                tools.append({
                    "name": tool_def.name,
                    "description": tool_def.description,
                    "type": tool_def.tool_type.value,
                    "parameters": [
                        {
                            "name": p.name,
                            "type": p.type,
                            "description": p.description,
                            "required": p.required,
                            "default": p.default
                        } for p in tool_def.parameters
                    ],
                    "examples": tool_def.examples,
                    "tags": tool_def.tags
                })
        return tools
    
    def _generate_tool_selection_prompt(self, user_input: str) -> str:
        """生成工具选择提示词"""
        tools_info = []
        for tool_name, tool_def in self.tools.items():
            params_info = []
            for param in tool_def.parameters:
                param_str = f"- {param.name} ({param.type})"
                if param.required:
                    param_str += " [必需]"
                else:
                    param_str += f" [可选, 默认: {param.default}]"
                param_str += f": {param.description}"
                params_info.append(param_str)
            
            tool_info = f"""
工具名称: {tool_name}
类型: {tool_def.tool_type.value}
描述: {tool_def.description}
参数:
{chr(10).join(params_info)}
示例: {', '.join(tool_def.examples) if tool_def.examples else '无'}
"""
            tools_info.append(tool_info)
        
        return f"""
你是一个智能工具选择助手。用户提出了一个需求，你需要分析这个需求并选择最合适的工具来完成任务。

用户需求: {user_input}

可用工具:
{chr(10).join(tools_info)}

请分析用户需求，选择最合适的工具，并推理出需要的参数。

请按以下JSON格式回复:
{{
    "selected_tool": "工具名称",
    "parameters": {{
        "参数名": "参数值"
    }},
    "reasoning": "选择这个工具的原因和参数推理过程",
    "confidence": 0.95
}}

如果需要多个工具配合完成任务，请选择第一个需要执行的工具。
如果无法确定合适的工具，请将selected_tool设为null。
"""
    
    def _select_tool_and_parameters(self, user_input: str) -> Optional[ToolCallPlan]:
        """使用LLM选择工具和参数"""
        try:
            prompt = self._generate_tool_selection_prompt(user_input)
            
            if self.verbose:
                logger.info("🤔 正在分析用户需求并选择工具...")
            
            response = self.llm_client.simple_chat(prompt)
            
            # 尝试解析JSON响应
            try:
                # 提取JSON部分
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = response[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    result = json.loads(response)
                
                if result.get("selected_tool") is None:
                    if self.verbose:
                        logger.warning("❌ 未找到合适的工具")
                    return None
                
                return ToolCallPlan(
                    tool_name=result["selected_tool"],
                    parameters=result.get("parameters", {}),
                    reasoning=result.get("reasoning", ""),
                    confidence=result.get("confidence", 1.0)
                )
                
            except json.JSONDecodeError as e:
                if self.verbose:
                    logger.error(f"❌ JSON解析失败: {e}")
                    logger.error(f"原始响应: {response}")
                return None
                
        except Exception as e:
            if self.verbose:
                logger.error(f"❌ 工具选择失败: {e}")
            return None
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolExecutionResult:
        """执行工具"""
        start_time = datetime.now()
        
        if tool_name not in self.tools:
            return ToolExecutionResult(
                success=False,
                error_message=f"工具 '{tool_name}' 不存在",
                tool_name=tool_name,
                parameters=parameters
            )
        
        tool_def = self.tools[tool_name]
        
        try:
            if self.verbose:
                logger.info(f"🔧 执行工具: {tool_name}")
                logger.info(f"📝 参数: {parameters}")
            
            # 验证和处理参数
            processed_params = {}
            for param_def in tool_def.parameters:
                param_name = param_def.name
                
                if param_name in parameters:
                    processed_params[param_name] = parameters[param_name]
                elif param_def.required:
                    return ToolExecutionResult(
                        success=False,
                        error_message=f"缺少必需参数: {param_name}",
                        tool_name=tool_name,
                        parameters=parameters
                    )
                elif param_def.default is not None:
                    processed_params[param_name] = param_def.default
            
            # 执行工具函数
            if tool_def.async_support:
                result = await tool_def.function(**processed_params)
            else:
                result = tool_def.function(**processed_params)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            execution_result = ToolExecutionResult(
                success=True,
                result=result,
                execution_time=execution_time,
                tool_name=tool_name,
                parameters=processed_params
            )
            
            self.execution_history.append(execution_result)
            
            if self.verbose:
                logger.info(f"✅ 工具执行成功，耗时: {execution_time:.2f}秒")
                logger.info(f"📊 结果: {str(result)[:200]}...")
            
            return execution_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"工具执行失败: {str(e)}"
            
            execution_result = ToolExecutionResult(
                success=False,
                error_message=error_msg,
                execution_time=execution_time,
                tool_name=tool_name,
                parameters=parameters
            )
            
            self.execution_history.append(execution_result)
            
            if self.verbose:
                logger.error(f"❌ {error_msg}")
                logger.error(f"🔍 错误详情: {traceback.format_exc()}")
            
            return execution_result
    
    async def process_request(self, user_input: str, max_iterations: int = 5) -> Dict[str, Any]:
        """处理用户请求，可能涉及多个工具调用"""
        if self.verbose:
            logger.info(f"🚀 开始处理请求: {user_input}")
        
        results = []
        current_input = user_input
        
        for iteration in range(max_iterations):
            if self.verbose:
                logger.info(f"🔄 第 {iteration + 1} 轮工具选择")
            
            # 选择工具和参数
            plan = self._select_tool_and_parameters(current_input)
            
            if plan is None:
                if iteration == 0:
                    return {
                        "success": False,
                        "message": "无法找到合适的工具来处理您的请求",
                        "results": results
                    }
                else:
                    # 如果不是第一轮，说明任务可能已经完成
                    break
            
            if self.verbose:
                logger.info(f"🎯 选择工具: {plan.tool_name}")
                logger.info(f"💭 推理: {plan.reasoning}")
                logger.info(f"📊 置信度: {plan.confidence:.2%}")
            
            # 执行工具
            execution_result = await self.execute_tool(plan.tool_name, plan.parameters)
            results.append({
                "tool_name": plan.tool_name,
                "parameters": plan.parameters,
                "reasoning": plan.reasoning,
                "confidence": plan.confidence,
                "success": execution_result.success,
                "result": execution_result.result,
                "error_message": execution_result.error_message,
                "execution_time": execution_result.execution_time
            })
            
            if not execution_result.success:
                return {
                    "success": False,
                    "message": f"工具执行失败: {execution_result.error_message}",
                    "results": results
                }
            
            # 检查是否需要继续
            if self._is_task_complete(user_input, results):
                break
            
            # 更新输入，包含之前的结果
            current_input = self._update_context_for_next_iteration(user_input, results)
        
        return {
            "success": True,
            "message": "任务完成",
            "results": results,
            "total_iterations": len(results)
        }
    
    def _is_task_complete(self, original_input: str, results: List[Dict[str, Any]]) -> bool:
        """判断任务是否完成（简单实现）"""
        # 简单策略：如果最后一个工具执行成功，认为任务完成
        # 实际应用中可以使用LLM来判断
        return len(results) > 0 and results[-1]["success"]
    
    def _update_context_for_next_iteration(self, original_input: str, results: List[Dict[str, Any]]) -> str:
        """为下一轮迭代更新上下文"""
        context = f"原始请求: {original_input}\n\n已执行的工具:\n"
        for i, result in enumerate(results, 1):
            context += f"{i}. {result['tool_name']}: {result['result']}\n"
        context += "\n请继续完成任务。"
        return context
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取执行历史"""
        return [
            {
                "tool_name": result.tool_name,
                "parameters": result.parameters,
                "success": result.success,
                "result": str(result.result)[:200] if result.result else None,
                "error_message": result.error_message,
                "execution_time": result.execution_time,
                "timestamp": result.timestamp.isoformat()
            }
            for result in self.execution_history
        ]
    
    def clear_history(self) -> None:
        """清除执行历史"""
        self.execution_history.clear()
        if self.verbose:
            logger.info("🧹 执行历史已清除")
    
    def get_tool_statistics(self) -> Dict[str, Any]:
        """获取工具使用统计"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        stats = {
            "total_executions": len(self.execution_history),
            "successful_executions": sum(1 for r in self.execution_history if r.success),
            "failed_executions": sum(1 for r in self.execution_history if not r.success),
            "average_execution_time": sum(r.execution_time for r in self.execution_history) / len(self.execution_history),
            "tool_usage_count": {},
            "most_used_tools": []
        }
        
        # 统计每个工具的使用次数
        for result in self.execution_history:
            tool_name = result.tool_name
            stats["tool_usage_count"][tool_name] = stats["tool_usage_count"].get(tool_name, 0) + 1
        
        # 按使用次数排序
        stats["most_used_tools"] = sorted(
            stats["tool_usage_count"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return stats
