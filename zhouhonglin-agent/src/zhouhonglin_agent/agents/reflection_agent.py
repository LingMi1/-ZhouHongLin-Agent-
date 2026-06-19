"""
Reflection Agent - 反思代理

这个模块实现了 Agentic Design Pattern 中的 Reflection（反思）模式。
Reflection 模式的核心思想是通过自我批判和迭代改进来提高输出质量。
系统先生成初始响应，然后对其进行批判性反思，基于反思进行改进，可进行多轮迭代。

核心优势：
1. 自我改进：通过反思发现问题并自动改进
2. 质量提升：多轮迭代显著提高输出质量
3. 可控性：可设置反思维度和迭代次数
4. 可追溯：记录完整的反思和改进历史
5. 灵活性：支持多种反思策略和改进方法
"""

from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class ReflectionStrategy(Enum):
    """反思策略枚举"""
    SIMPLE = "simple"              # 简单反思（单一批评者）
    MULTI_ASPECT = "multi_aspect"  # 多维度反思（多个角度）
    DEBATE = "debate"              # 辩论式反思（正反两方）
    EXPERT = "expert"              # 专家反思（特定领域专家）


@dataclass
class ReflectionCriteria:
    """反思标准"""
    name: str                      # 标准名称
    description: str               # 标准描述
    weight: float = 1.0           # 权重（用于评分）
    examples: Optional[List[str]] = None  # 示例


@dataclass
class ReflectionResult:
    """单次反思结果"""
    iteration: int                 # 迭代次数
    content: str                   # 生成的内容
    critique: str                  # 批评/反思内容
    score: float                   # 质量评分（0-1）
    improvements: List[str]        # 改进建议列表
    timestamp: str                 # 时间戳


@dataclass
class ReflectionOutput:
    """完整反思过程的输出"""
    final_content: str             # 最终优化的内容
    reflection_history: List[ReflectionResult]  # 反思历史
    total_iterations: int          # 总迭代次数
    final_score: float            # 最终评分
    improvement_summary: str      # 改进总结
    success: bool                 # 是否成功
    error_message: str = ""       # 错误信息
    total_time: float = 0.0       # 总耗时


class ReflectionAgent:
    """
    反思代理 - 实现 Reflection 设计模式
    
    示例用法:
        agent = ReflectionAgent(llm_client, max_iterations=3)
        
        result = agent.reflect_and_improve(
            task="写一篇关于AI的文章",
            strategy=ReflectionStrategy.MULTI_ASPECT
        )
        
        print(result.final_content)
    """
    
    def __init__(
        self,
        llm_client,
        max_iterations: int = 3,
        score_threshold: float = 0.85,
        verbose: bool = True
    ):
        """
        初始化反思代理
        
        Args:
            llm_client: 大语言模型客户端
            max_iterations: 最大迭代次数
            score_threshold: 分数阈值（达到此分数即停止迭代）
            verbose: 是否打印详细信息
        """
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.score_threshold = score_threshold
        self.verbose = verbose
        
    def reflect_and_improve(
        self,
        task: str,
        initial_content: Optional[str] = None,
        strategy: ReflectionStrategy = ReflectionStrategy.SIMPLE,
        criteria: Optional[List[ReflectionCriteria]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ReflectionOutput:
        """
        执行反思和改进过程
        
        Args:
            task: 任务描述
            initial_content: 初始内容（如果为空则先生成）
            strategy: 反思策略
            criteria: 反思标准列表
            context: 额外上下文
            
        Returns:
            ReflectionOutput 包含最终内容和反思历史
        """
        start_time = datetime.now()
        context = context or {}
        reflection_history = []
        
        try:
            # 1. 生成初始内容（如果没有提供）
            if initial_content is None:
                if self.verbose:
                    print(f"\n{'='*60}")
                    print(f"🎯 反思代理 - 生成初始内容")
                    print(f"策略: {strategy.value}")
                    print(f"{'='*60}\n")
                
                initial_content = self._generate_initial_content(task, context)
                
                if self.verbose:
                    print(f"📝 初始内容:\n{initial_content[:200]}...\n")
            
            current_content = initial_content
            
            # 2. 迭代反思和改进
            for iteration in range(1, self.max_iterations + 1):
                if self.verbose:
                    print(f"\n{'='*60}")
                    print(f"🔄 第 {iteration} 轮反思")
                    print(f"{'='*60}\n")
                
                # 执行反思
                critique, score, improvements = self._reflect(
                    content=current_content,
                    task=task,
                    strategy=strategy,
                    criteria=criteria,
                    context=context
                )
                
                if self.verbose:
                    print(f"💭 反思评价:\n{critique}\n")
                    print(f"📊 质量评分: {score:.2f}/1.0")
                    print(f"💡 改进建议: {len(improvements)} 条\n")
                
                # 记录反思结果
                reflection_result = ReflectionResult(
                    iteration=iteration,
                    content=current_content,
                    critique=critique,
                    score=score,
                    improvements=improvements,
                    timestamp=datetime.now().isoformat()
                )
                reflection_history.append(reflection_result)
                
                # 检查是否达到质量阈值
                if score >= self.score_threshold:
                    if self.verbose:
                        print(f"✅ 已达到质量阈值 ({score:.2f} >= {self.score_threshold})，停止迭代\n")
                    break
                
                # 如果不是最后一轮，进行改进
                if iteration < self.max_iterations:
                    if self.verbose:
                        print(f"🔧 根据反思进行改进...\n")
                    
                    current_content = self._improve(
                        content=current_content,
                        critique=critique,
                        improvements=improvements,
                        task=task,
                        context=context
                    )
                    
                    if self.verbose:
                        print(f"📝 改进后的内容:\n{current_content[:200]}...\n")
            
            # 3. 生成改进总结
            improvement_summary = self._generate_improvement_summary(
                reflection_history,
                task
            )
            
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"✅ 反思过程完成！")
                print(f"总迭代次数: {len(reflection_history)}")
                print(f"最终评分: {reflection_history[-1].score:.2f}")
                print(f"总耗时: {total_time:.2f}秒")
                print(f"{'='*60}\n")
            
            return ReflectionOutput(
                final_content=current_content,
                reflection_history=reflection_history,
                total_iterations=len(reflection_history),
                final_score=reflection_history[-1].score,
                improvement_summary=improvement_summary,
                success=True,
                total_time=total_time
            )
            
        except Exception as e:
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            
            if self.verbose:
                print(f"\n❌ 反思过程失败: {str(e)}\n")
            
            return ReflectionOutput(
                final_content=current_content if 'current_content' in locals() else "",
                reflection_history=reflection_history,
                total_iterations=len(reflection_history),
                final_score=reflection_history[-1].score if reflection_history else 0.0,
                improvement_summary="",
                success=False,
                error_message=str(e),
                total_time=total_time
            )
    
    def _generate_initial_content(self, task: str, context: Dict[str, Any]) -> str:
        """生成初始内容"""
        prompt = f"""请完成以下任务：

任务: {task}

要求：
1. 内容要完整、准确
2. 逻辑要清晰
3. 表达要专业

请直接输出内容，不要额外说明。"""
        
        return self.llm_client.simple_chat(prompt)
    
    def _reflect(
        self,
        content: str,
        task: str,
        strategy: ReflectionStrategy,
        criteria: Optional[List[ReflectionCriteria]],
        context: Dict[str, Any]
    ) -> tuple[str, float, List[str]]:
        """
        执行反思
        
        Returns:
            (critique, score, improvements) 元组
        """
        if strategy == ReflectionStrategy.SIMPLE:
            return self._simple_reflect(content, task, criteria)
        elif strategy == ReflectionStrategy.MULTI_ASPECT:
            return self._multi_aspect_reflect(content, task, criteria)
        elif strategy == ReflectionStrategy.DEBATE:
            return self._debate_reflect(content, task)
        elif strategy == ReflectionStrategy.EXPERT:
            return self._expert_reflect(content, task, context)
        else:
            return self._simple_reflect(content, task, criteria)
    
    def _simple_reflect(
        self,
        content: str,
        task: str,
        criteria: Optional[List[ReflectionCriteria]]
    ) -> tuple[str, float, List[str]]:
        """简单反思策略"""
        criteria_text = ""
        if criteria:
            criteria_text = "\n评估标准：\n" + "\n".join([
                f"- {c.name}: {c.description}" for c in criteria
            ])
        
        prompt = f"""你是一个严格的批评者。请对以下内容进行批判性反思。

任务要求: {task}

生成的内容:
{content}
{criteria_text}

请从以下角度进行评估：
1. 内容的完整性和准确性
2. 逻辑的清晰性和连贯性
3. 表达的专业性和易读性
4. 是否完成了任务要求

请以 JSON 格式返回评估结果：
{{
    "critique": "详细的批评和分析",
    "score": 0.0-1.0之间的质量评分,
    "improvements": ["改进建议1", "改进建议2", ...]
}}

只返回 JSON，不要其他内容。"""
        
        response = self.llm_client.simple_chat(prompt)
        return self._parse_reflection_response(response)
    
    def _multi_aspect_reflect(
        self,
        content: str,
        task: str,
        criteria: Optional[List[ReflectionCriteria]]
    ) -> tuple[str, float, List[str]]:
        """多维度反思策略"""
        aspects = criteria if criteria else [
            ReflectionCriteria("准确性", "内容是否准确无误", 1.0),
            ReflectionCriteria("完整性", "内容是否完整全面", 1.0),
            ReflectionCriteria("逻辑性", "逻辑是否清晰连贯", 0.9),
            ReflectionCriteria("可读性", "表达是否易于理解", 0.8),
            ReflectionCriteria("专业性", "是否符合专业标准", 0.9)
        ]
        
        aspects_text = "\n".join([
            f"{i+1}. **{a.name}** (权重{a.weight}): {a.description}"
            for i, a in enumerate(aspects)
        ])
        
        prompt = f"""你是一个多维度评估专家。请从多个角度对以下内容进行深入反思。

任务要求: {task}

生成的内容:
{content}

评估维度:
{aspects_text}

请对每个维度进行详细评估，并给出综合评价。

请以 JSON 格式返回：
{{
    "critique": "综合批评和分析（包括各维度的评价）",
    "score": 0.0-1.0之间的综合评分,
    "improvements": ["改进建议1", "改进建议2", ...]
}}

只返回 JSON，不要其他内容。"""
        
        response = self.llm_client.simple_chat(prompt)
        return self._parse_reflection_response(response)
    
    def _debate_reflect(
        self,
        content: str,
        task: str
    ) -> tuple[str, float, List[str]]:
        """辩论式反思策略（正反两方）"""
        # 正方：找优点
        pros_prompt = f"""你是一个支持者。请找出以下内容的优点和做得好的地方。

任务: {task}

内容:
{content}

请列出这个内容的优点、亮点和价值。"""
        
        pros = self.llm_client.simple_chat(pros_prompt)
        
        # 反方：找问题
        cons_prompt = f"""你是一个批评者。请找出以下内容的问题和不足之处。

任务: {task}

内容:
{content}

请列出这个内容的问题、不足和需要改进的地方。"""
        
        cons = self.llm_client.simple_chat(cons_prompt)
        
        # 综合判断
        judge_prompt = f"""你是一个公正的裁判。请基于正反两方的观点，给出客观评价。

任务: {task}

内容:
{content}

支持方观点:
{pros}

批评方观点:
{cons}

请以 JSON 格式返回综合评价：
{{
    "critique": "综合双方观点的客观评价",
    "score": 0.0-1.0之间的质量评分,
    "improvements": ["改进建议1", "改进建议2", ...]
}}

只返回 JSON，不要其他内容。"""
        
        response = self.llm_client.simple_chat(judge_prompt)
        return self._parse_reflection_response(response)
    
    def _expert_reflect(
        self,
        content: str,
        task: str,
        context: Dict[str, Any]
    ) -> tuple[str, float, List[str]]:
        """专家反思策略"""
        expert_role = context.get('expert_role', '领域专家')
        expert_expertise = context.get('expert_expertise', '相关领域的专业知识')
        
        prompt = f"""你是一位资深的{expert_role}，拥有{expert_expertise}。
请以专家的视角对以下内容进行专业评估。

任务: {task}

内容:
{content}

请从专业角度评估：
1. 专业准确性
2. 深度和广度
3. 实践价值
4. 创新性
5. 可行性

请以 JSON 格式返回专家评估：
{{
    "critique": "专家级别的详细评价",
    "score": 0.0-1.0之间的专业评分,
    "improvements": ["专业改进建议1", "专业改进建议2", ...]
}}

只返回 JSON，不要其他内容。"""
        
        response = self.llm_client.simple_chat(prompt)
        return self._parse_reflection_response(response)
    
    def _parse_reflection_response(self, response: str) -> tuple[str, float, List[str]]:
        """解析反思响应"""
        try:
            # 清理响应
            response_clean = response.strip()
            if response_clean.startswith("```"):
                response_clean = response_clean.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(response_clean)
            
            critique = result.get("critique", "")
            score = float(result.get("score", 0.5))
            improvements = result.get("improvements", [])
            
            # 确保评分在有效范围内
            score = max(0.0, min(1.0, score))
            
            return critique, score, improvements
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  解析反思响应失败: {e}")
            
            # 返回默认值
            return response, 0.5, ["无法解析具体改进建议，请重新审视内容"]
    
    def _improve(
        self,
        content: str,
        critique: str,
        improvements: List[str],
        task: str,
        context: Dict[str, Any]
    ) -> str:
        """基于反思进行改进"""
        improvements_text = "\n".join([f"{i+1}. {imp}" for i, imp in enumerate(improvements)])
        
        prompt = f"""请根据批评意见改进以下内容。

原始任务: {task}

当前内容:
{content}

批评意见:
{critique}

改进建议:
{improvements_text}

要求：
1. 认真考虑所有批评意见和改进建议
2. 保留内容中好的部分
3. 改进或修正有问题的部分
4. 确保改进后的内容更完整、准确、专业
5. 直接输出改进后的完整内容，不要额外说明

请输出改进后的内容："""
        
        return self.llm_client.simple_chat(prompt)
    
    def _generate_improvement_summary(
        self,
        reflection_history: List[ReflectionResult],
        task: str
    ) -> str:
        """生成改进总结"""
        if not reflection_history:
            return "没有反思历史记录"
        
        iterations_summary = []
        for result in reflection_history:
            iterations_summary.append(
                f"第{result.iteration}轮: 评分{result.score:.2f}, "
                f"{len(result.improvements)}条改进建议"
            )
        
        score_improvement = (
            reflection_history[-1].score - reflection_history[0].score
            if len(reflection_history) > 1 else 0.0
        )
        
        summary = f"""## 反思改进总结

**任务**: {task}

**迭代过程**:
{chr(10).join(['- ' + s for s in iterations_summary])}

**质量提升**: {score_improvement:+.2f} (从 {reflection_history[0].score:.2f} 到 {reflection_history[-1].score:.2f})

**主要改进点**:
"""
        
        # 收集所有改进建议
        all_improvements = []
        for result in reflection_history:
            all_improvements.extend(result.improvements)
        
        # 去重并添加到总结
        unique_improvements = list(dict.fromkeys(all_improvements))[:5]  # 取前5个
        for i, imp in enumerate(unique_improvements, 1):
            summary += f"{i}. {imp}\n"
        
        return summary


# ==================== 预定义的反思场景 ====================


class ContentReflection:
    """内容创作反思场景"""
    
    @staticmethod
    def get_criteria() -> List[ReflectionCriteria]:
        """获取内容创作的反思标准"""
        return [
            ReflectionCriteria(
                name="内容质量",
                description="内容是否准确、完整、有价值",
                weight=1.0,
                examples=["信息准确", "逻辑清晰", "观点明确"]
            ),
            ReflectionCriteria(
                name="语言表达",
                description="语言是否流畅、专业、易读",
                weight=0.9,
                examples=["表达流畅", "用词准确", "结构清晰"]
            ),
            ReflectionCriteria(
                name="用户价值",
                description="对读者是否有实际价值和帮助",
                weight=1.0,
                examples=["解决问题", "提供见解", "易于应用"]
            ),
            ReflectionCriteria(
                name="创新性",
                description="是否有独特见解或新颖角度",
                weight=0.7,
                examples=["新颖观点", "独特视角", "创新思路"]
            )
        ]


class CodeReflection:
    """代码反思场景"""
    
    @staticmethod
    def get_criteria() -> List[ReflectionCriteria]:
        """获取代码的反思标准"""
        return [
            ReflectionCriteria(
                name="正确性",
                description="代码逻辑是否正确，是否有bug",
                weight=1.0,
                examples=["逻辑正确", "边界处理", "异常处理"]
            ),
            ReflectionCriteria(
                name="可读性",
                description="代码是否清晰易懂，注释是否充分",
                weight=0.9,
                examples=["命名清晰", "注释完善", "结构清晰"]
            ),
            ReflectionCriteria(
                name="性能",
                description="代码效率是否合理",
                weight=0.8,
                examples=["时间复杂度", "空间复杂度", "资源使用"]
            ),
            ReflectionCriteria(
                name="可维护性",
                description="代码是否易于维护和扩展",
                weight=0.9,
                examples=["模块化", "可扩展", "低耦合"]
            ),
            ReflectionCriteria(
                name="最佳实践",
                description="是否遵循语言和框架的最佳实践",
                weight=0.8,
                examples=["设计模式", "代码规范", "安全性"]
            )
        ]


class AnalysisReflection:
    """分析报告反思场景"""
    
    @staticmethod
    def get_criteria() -> List[ReflectionCriteria]:
        """获取分析报告的反思标准"""
        return [
            ReflectionCriteria(
                name="数据准确性",
                description="数据和事实是否准确可靠",
                weight=1.0,
                examples=["数据真实", "引用可靠", "论据充分"]
            ),
            ReflectionCriteria(
                name="分析深度",
                description="分析是否深入透彻",
                weight=1.0,
                examples=["深入分析", "多角度", "因果关系"]
            ),
            ReflectionCriteria(
                name="逻辑性",
                description="论证逻辑是否严密",
                weight=0.9,
                examples=["逻辑严密", "推理合理", "结论可靠"]
            ),
            ReflectionCriteria(
                name="实用性",
                description="结论和建议是否具有实践价值",
                weight=0.9,
                examples=["可操作", "有价值", "可落地"]
            ),
            ReflectionCriteria(
                name="表达清晰",
                description="报告表达是否清晰易懂",
                weight=0.8,
                examples=["结构清晰", "重点突出", "易于理解"]
            )
        ]


class TranslationReflection:
    """翻译反思场景"""
    
    @staticmethod
    def get_criteria() -> List[ReflectionCriteria]:
        """获取翻译的反思标准"""
        return [
            ReflectionCriteria(
                name="准确性",
                description="翻译是否准确传达原文意思",
                weight=1.0,
                examples=["意思准确", "无遗漏", "无误译"]
            ),
            ReflectionCriteria(
                name="流畅性",
                description="译文是否符合目标语言习惯",
                weight=0.9,
                examples=["表达自然", "语言流畅", "符合习惯"]
            ),
            ReflectionCriteria(
                name="专业性",
                description="专业术语翻译是否准确",
                weight=1.0,
                examples=["术语准确", "行业规范", "专业表达"]
            ),
            ReflectionCriteria(
                name="一致性",
                description="全文翻译风格和术语是否一致",
                weight=0.8,
                examples=["风格统一", "术语一致", "格式统一"]
            )
        ]

