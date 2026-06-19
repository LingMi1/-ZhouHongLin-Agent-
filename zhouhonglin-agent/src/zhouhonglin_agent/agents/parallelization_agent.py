"""
Parallelization Agent - 并行化代理

这个模块实现了 Agentic Design Pattern 中的 Parallelization 模式。
并行化模式的核心思想是同时执行多个任务或将复杂任务分解为可以并行执行的子任务，
通过并行处理来提高效率、获得多角度视角，并提升结果质量。

核心优势：
1. 提高效率：多个任务同时执行，显著减少总耗时
2. 多样性：从不同角度或使用不同方法处理同一问题
3. 鲁棒性：多个并行结果可以相互验证，提高可靠性
4. 可扩展：轻松增加并行任务数量
5. 灵活性：支持多种并行策略和聚合方式
"""

from typing import List, Dict, Any, Callable, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
import asyncio
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class ParallelStrategy(Enum):
    """并行策略枚举"""
    FULL_PARALLEL = "full_parallel"  # 全并行：所有任务同时执行
    BATCH_PARALLEL = "batch_parallel"  # 批量并行：分批执行
    PIPELINE = "pipeline"  # 流水线：任务之间有依赖，按阶段并行
    VOTE = "vote"  # 投票：多个相同任务并行，结果投票决定
    ENSEMBLE = "ensemble"  # 集成：多个不同方法并行，结果融合


class AggregationMethod(Enum):
    """结果聚合方法枚举"""
    MERGE = "merge"  # 合并所有结果
    VOTE = "vote"  # 投票选择最佳结果
    CONCAT = "concat"  # 连接所有结果
    SUMMARIZE = "summarize"  # 总结所有结果
    BEST = "best"  # 选择评分最高的结果
    FIRST = "first"  # 使用第一个完成的结果
    CONSENSUS = "consensus"  # 寻找共识


@dataclass
class ParallelTask:
    """并行任务定义"""
    name: str  # 任务名称
    handler: Callable  # 处理函数
    input_data: Any  # 输入数据
    description: str = ""  # 任务描述
    priority: int = 0  # 优先级（用于流水线）
    dependencies: Optional[List[str]] = None  # 依赖的任务名称
    timeout: Optional[float] = None  # 超时时间（秒）
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class TaskResult:
    """单个任务的执行结果"""
    task_name: str  # 任务名称
    output: Any  # 输出结果
    success: bool  # 是否成功
    execution_time: float  # 执行时间
    error_message: str = ""  # 错误信息
    metadata: Optional[Dict[str, Any]] = None  # 额外的元数据


@dataclass
class ParallelResult:
    """并行执行的总体结果"""
    task_results: List[TaskResult]  # 所有任务结果
    aggregated_result: Any  # 聚合后的结果
    total_time: float  # 总执行时间
    parallel_time: float  # 并行执行时间（最长任务的时间）
    success_count: int  # 成功任务数
    failed_count: int  # 失败任务数
    strategy: str  # 使用的并行策略
    aggregation_method: str  # 使用的聚合方法


class ParallelizationAgent:
    """
    并行化代理 - 实现 Parallelization 设计模式
    
    示例用法:
        agent = ParallelizationAgent(llm_client, max_workers=5)
        
        # 定义并行任务
        tasks = [
            ParallelTask(
                name="task1",
                handler=handler_func1,
                input_data="input1",
                description="第一个任务"
            ),
            ParallelTask(
                name="task2",
                handler=handler_func2,
                input_data="input2",
                description="第二个任务"
            )
        ]
        
        # 执行并行任务
        result = agent.execute_parallel(
            tasks,
            strategy=ParallelStrategy.FULL_PARALLEL,
            aggregation=AggregationMethod.MERGE
        )
    """
    
    def __init__(
        self,
        llm_client=None,
        max_workers: int = 5,
        verbose: bool = True
    ):
        """
        初始化并行化代理
        
        Args:
            llm_client: 大语言模型客户端
            max_workers: 最大并行工作线程数
            verbose: 是否打印详细信息
        """
        self.llm_client = llm_client
        self.max_workers = max_workers
        self.verbose = verbose
        self._lock = threading.Lock()
        
    def _execute_task(self, task: ParallelTask) -> TaskResult:
        """
        执行单个任务
        
        Args:
            task: 并行任务
            
        Returns:
            TaskResult 任务执行结果
        """
        start_time = time.time()
        
        try:
            if self.verbose:
                print(f"🔄 开始执行任务: {task.name}")
            
            # 执行任务处理器
            output = task.handler(task.input_data, self.llm_client)
            
            execution_time = time.time() - start_time
            
            if self.verbose:
                print(f"✅ 任务完成: {task.name} (耗时: {execution_time:.2f}秒)")
            
            return TaskResult(
                task_name=task.name,
                output=output,
                success=True,
                execution_time=execution_time,
                metadata={"description": task.description}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            if self.verbose:
                print(f"❌ 任务失败: {task.name} - {str(e)}")
            
            return TaskResult(
                task_name=task.name,
                output=None,
                success=False,
                execution_time=execution_time,
                error_message=str(e),
                metadata={"description": task.description}
            )
    
    def _execute_full_parallel(self, tasks: List[ParallelTask]) -> List[TaskResult]:
        """
        全并行执行：所有任务同时执行
        
        Args:
            tasks: 任务列表
            
        Returns:
            任务结果列表
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(self._execute_task, task): task
                for task in tasks
            }
            
            # 收集结果
            for future in as_completed(future_to_task):
                result = future.result()
                results.append(result)
        
        # 按任务名称排序，保持顺序一致
        results.sort(key=lambda x: [t.name for t in tasks].index(x.task_name))
        
        return results
    
    def _execute_batch_parallel(
        self,
        tasks: List[ParallelTask],
        batch_size: int = 3
    ) -> List[TaskResult]:
        """
        批量并行执行：将任务分批执行
        
        Args:
            tasks: 任务列表
            batch_size: 每批的任务数
            
        Returns:
            任务结果列表
        """
        all_results = []
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            
            if self.verbose:
                print(f"\n📦 执行第 {i//batch_size + 1} 批任务 ({len(batch)} 个任务)")
            
            batch_results = self._execute_full_parallel(batch)
            all_results.extend(batch_results)
        
        return all_results
    
    def _execute_pipeline(self, tasks: List[ParallelTask]) -> List[TaskResult]:
        """
        流水线执行：考虑任务依赖关系，分阶段并行
        
        Args:
            tasks: 任务列表
            
        Returns:
            任务结果列表
        """
        # 构建依赖图
        task_dict = {task.name: task for task in tasks}
        completed = {}
        results = []
        
        # 按阶段执行
        while len(completed) < len(tasks):
            # 找出所有依赖已满足的任务
            ready_tasks = []
            for task in tasks:
                if task.name not in completed:
                    # 检查依赖是否都已完成
                    if all(dep in completed for dep in task.dependencies):
                        ready_tasks.append(task)
            
            if not ready_tasks:
                # 如果没有就绪任务但还有未完成任务，说明存在循环依赖
                remaining = [t.name for t in tasks if t.name not in completed]
                raise ValueError(f"检测到循环依赖或无法满足的依赖: {remaining}")
            
            if self.verbose:
                print(f"\n🔀 执行流水线阶段 ({len(ready_tasks)} 个任务)")
            
            # 并行执行就绪的任务
            stage_results = self._execute_full_parallel(ready_tasks)
            
            # 标记已完成
            for result in stage_results:
                completed[result.task_name] = result
                results.append(result)
        
        # 按原始顺序排序
        results.sort(key=lambda x: [t.name for t in tasks].index(x.task_name))
        
        return results
    
    def _aggregate_results(
        self,
        results: List[TaskResult],
        method: AggregationMethod,
        aggregation_prompt: Optional[str] = None
    ) -> Any:
        """
        聚合多个任务结果
        
        Args:
            results: 任务结果列表
            method: 聚合方法
            aggregation_prompt: 自定义聚合提示词
            
        Returns:
            聚合后的结果
        """
        # 只考虑成功的结果
        successful_results = [r for r in results if r.success]
        
        if not successful_results:
            return "所有任务均失败，无法聚合结果"
        
        if method == AggregationMethod.MERGE:
            # 合并所有结果到一个字典
            merged = {}
            for result in successful_results:
                merged[result.task_name] = result.output
            return merged
        
        elif method == AggregationMethod.CONCAT:
            # 连接所有结果
            outputs = [str(r.output) for r in successful_results]
            return "\n\n---\n\n".join(outputs)
        
        elif method == AggregationMethod.FIRST:
            # 返回第一个完成的结果
            return successful_results[0].output
        
        elif method == AggregationMethod.BEST:
            # 返回输出最长的结果（简单启发式）
            best = max(successful_results, key=lambda r: len(str(r.output)))
            return best.output
        
        elif method == AggregationMethod.SUMMARIZE:
            # 使用 LLM 总结所有结果
            if not self.llm_client:
                return self._aggregate_results(results, AggregationMethod.CONCAT)
            
            outputs = [f"**{r.task_name}**:\n{r.output}" for r in successful_results]
            combined = "\n\n".join(outputs)
            
            prompt = aggregation_prompt or f"""请总结以下多个并行任务的结果，提取关键信息并形成一个综合性的回答。

任务结果：
{combined}

请提供一个清晰、全面的总结："""
            
            return self.llm_client.simple_chat(prompt)
        
        elif method == AggregationMethod.VOTE:
            # 投票选择最常见的结果
            from collections import Counter
            outputs = [str(r.output) for r in successful_results]
            counter = Counter(outputs)
            most_common = counter.most_common(1)[0][0]
            return most_common
        
        elif method == AggregationMethod.CONSENSUS:
            # 使用 LLM 寻找共识
            if not self.llm_client:
                return self._aggregate_results(results, AggregationMethod.VOTE)
            
            outputs = [f"**观点{i+1}**:\n{r.output}" for i, r in enumerate(successful_results)]
            combined = "\n\n".join(outputs)
            
            prompt = f"""以下是针对同一问题的多个不同观点或结果。请分析这些观点，找出它们的共识点，并给出一个综合的结论。

不同观点：
{combined}

请提供：
1. 共同点和一致的观点
2. 分歧点和不同的看法
3. 综合结论"""
            
            return self.llm_client.simple_chat(prompt)
        
        else:
            # 默认使用合并
            return self._aggregate_results(results, AggregationMethod.MERGE)
    
    def execute_parallel(
        self,
        tasks: List[ParallelTask],
        strategy: Union[ParallelStrategy, str] = ParallelStrategy.FULL_PARALLEL,
        aggregation: Union[AggregationMethod, str] = AggregationMethod.MERGE,
        aggregation_prompt: Optional[str] = None,
        batch_size: int = 3
    ) -> ParallelResult:
        """
        执行并行任务
        
        Args:
            tasks: 任务列表
            strategy: 并行策略
            aggregation: 结果聚合方法
            aggregation_prompt: 自定义聚合提示词
            batch_size: 批量并行的批次大小
            
        Returns:
            ParallelResult 并行执行结果
        """
        start_time = time.time()
        
        # 转换枚举类型
        if isinstance(strategy, str):
            strategy = ParallelStrategy(strategy)
        if isinstance(aggregation, str):
            aggregation = AggregationMethod(aggregation)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🚀 并行化代理 - {strategy.value}")
            print(f"任务数量: {len(tasks)}")
            print(f"聚合方法: {aggregation.value}")
            print(f"{'='*60}\n")
        
        # 根据策略执行任务
        try:
            parallel_start = time.time()
            
            if strategy == ParallelStrategy.FULL_PARALLEL:
                task_results = self._execute_full_parallel(tasks)
            
            elif strategy == ParallelStrategy.BATCH_PARALLEL:
                task_results = self._execute_batch_parallel(tasks, batch_size)
            
            elif strategy == ParallelStrategy.PIPELINE:
                task_results = self._execute_pipeline(tasks)
            
            elif strategy in [ParallelStrategy.VOTE, ParallelStrategy.ENSEMBLE]:
                # 这两种策略都是全并行，只是聚合方式不同
                task_results = self._execute_full_parallel(tasks)
            
            else:
                raise ValueError(f"不支持的并行策略: {strategy}")
            
            parallel_time = time.time() - parallel_start
            
            # 聚合结果
            if self.verbose:
                print(f"\n📊 聚合结果...")
            
            aggregated = self._aggregate_results(
                task_results,
                aggregation,
                aggregation_prompt
            )
            
            total_time = time.time() - start_time
            
            # 统计成功和失败
            success_count = sum(1 for r in task_results if r.success)
            failed_count = len(task_results) - success_count
            
            if self.verbose:
                print(f"\n✅ 并行执行完成！")
                print(f"总耗时: {total_time:.2f}秒")
                print(f"并行耗时: {parallel_time:.2f}秒")
                print(f"成功: {success_count}, 失败: {failed_count}")
                print(f"{'='*60}\n")
            
            return ParallelResult(
                task_results=task_results,
                aggregated_result=aggregated,
                total_time=total_time,
                parallel_time=parallel_time,
                success_count=success_count,
                failed_count=failed_count,
                strategy=strategy.value,
                aggregation_method=aggregation.value
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            
            if self.verbose:
                print(f"\n❌ 并行执行失败: {str(e)}\n")
            
            return ParallelResult(
                task_results=[],
                aggregated_result=f"执行失败: {str(e)}",
                total_time=total_time,
                parallel_time=0.0,
                success_count=0,
                failed_count=len(tasks),
                strategy=strategy.value,
                aggregation_method=aggregation.value
            )


# ==================== 预定义的并行任务场景 ====================


class MultiPerspectiveAnalysis:
    """多角度分析 - 从不同角度分析同一问题"""
    
    @staticmethod
    def create_tasks(input_text: str, perspectives: Optional[List[str]] = None) -> List[ParallelTask]:
        """
        创建多角度分析任务
        
        Args:
            input_text: 要分析的内容
            perspectives: 分析角度列表
            
        Returns:
            并行任务列表
        """
        if perspectives is None:
            perspectives = [
                "技术角度",
                "商业角度",
                "用户体验角度",
                "风险和挑战角度",
                "创新和机会角度"
            ]
        
        tasks = []
        for perspective in perspectives:
            def make_handler(persp):
                def handler(input_data, llm_client):
                    prompt = f"""请从{persp}分析以下内容：

{input_data}

请提供详细的分析，包括：
1. 主要观察和发现
2. 关键优势和亮点
3. 潜在问题和风险
4. 改进建议"""
                    return llm_client.simple_chat(prompt)
                return handler
            
            tasks.append(ParallelTask(
                name=perspective,
                handler=make_handler(perspective),
                input_data=input_text,
                description=f"从{perspective}进行分析"
            ))
        
        return tasks


class ParallelTranslation:
    """并行翻译 - 将文本翻译成多种语言"""
    
    @staticmethod
    def create_tasks(input_text: str, target_languages: Optional[List[str]] = None) -> List[ParallelTask]:
        """
        创建并行翻译任务
        
        Args:
            input_text: 要翻译的文本
            target_languages: 目标语言列表
            
        Returns:
            并行任务列表
        """
        if target_languages is None:
            target_languages = ["英语", "日语", "法语", "德语", "西班牙语"]
        
        tasks = []
        for lang in target_languages:
            def make_handler(language):
                def handler(input_data, llm_client):
                    prompt = f"""请将以下内容翻译成{language}：

{input_data}

要求：
1. 准确传达原文意思
2. 符合{language}的表达习惯
3. 保持专业术语的准确性"""
                    return llm_client.simple_chat(prompt)
                return handler
            
            tasks.append(ParallelTask(
                name=f"翻译_{lang}",
                handler=make_handler(lang),
                input_data=input_text,
                description=f"翻译成{lang}"
            ))
        
        return tasks


class ParallelContentGeneration:
    """并行内容生成 - 同时生成文档的不同部分"""
    
    @staticmethod
    def create_tasks(topic: str, sections: Optional[List[str]] = None) -> List[ParallelTask]:
        """
        创建并行内容生成任务
        
        Args:
            topic: 文档主题
            sections: 文档章节列表
            
        Returns:
            并行任务列表
        """
        if sections is None:
            sections = [
                "简介和背景",
                "核心概念",
                "实践示例",
                "最佳实践",
                "常见问题"
            ]
        
        tasks = []
        for section in sections:
            def make_handler(sect):
                def handler(topic_data, llm_client):
                    prompt = f"""请为主题"{topic_data}"撰写"{sect}"章节的内容。

要求：
1. 内容要专业、准确
2. 结构清晰，逻辑连贯
3. 适当使用示例说明
4. 字数在300-500字之间

请撰写内容："""
                    return llm_client.simple_chat(prompt)
                return handler
            
            tasks.append(ParallelTask(
                name=section,
                handler=make_handler(section),
                input_data=topic,
                description=f"生成'{section}'章节"
            ))
        
        return tasks


class ParallelCodeReview:
    """并行代码审查 - 从多个维度同时审查代码"""
    
    @staticmethod
    def create_tasks(code: str) -> List[ParallelTask]:
        """
        创建并行代码审查任务
        
        Args:
            code: 要审查的代码
            
        Returns:
            并行任务列表
        """
        review_aspects = [
            ("代码质量", "代码风格、命名规范、可读性"),
            ("性能分析", "时间复杂度、空间复杂度、优化建议"),
            ("安全检查", "安全漏洞、输入验证、错误处理"),
            ("最佳实践", "设计模式、代码组织、可维护性"),
            ("测试建议", "边界条件、测试用例、覆盖率")
        ]
        
        tasks = []
        for aspect, description in review_aspects:
            def make_handler(asp, desc):
                def handler(code_data, llm_client):
                    prompt = f"""请从{asp}的角度审查以下代码：

```
{code_data}
```

关注点：{desc}

请提供：
1. 发现的问题
2. 严重程度评估
3. 具体改进建议
4. 代码示例（如适用）"""
                    return llm_client.simple_chat(prompt)
                return handler
            
            tasks.append(ParallelTask(
                name=aspect,
                handler=make_handler(aspect, description),
                input_data=code,
                description=f"{aspect}审查"
            ))
        
        return tasks


class ParallelResearch:
    """并行研究 - 同时研究问题的不同方面"""
    
    @staticmethod
    def create_tasks(question: str, aspects: Optional[List[str]] = None) -> List[ParallelTask]:
        """
        创建并行研究任务
        
        Args:
            question: 研究问题
            aspects: 研究方面列表
            
        Returns:
            并行任务列表
        """
        if aspects is None:
            aspects = [
                "历史背景和发展",
                "当前状态和趋势",
                "主要方法和技术",
                "实际应用案例",
                "未来展望和挑战"
            ]
        
        tasks = []
        for aspect in aspects:
            def make_handler(asp):
                def handler(input_data, llm_client):
                    prompt = f"""请研究"{input_data}"问题的"{asp}"方面。

要求：
1. 提供详细的分析
2. 引用相关的概念和理论
3. 给出具体的例子
4. 保持客观和专业

请提供研究结果："""
                    return llm_client.simple_chat(prompt)
                return handler
            
            tasks.append(ParallelTask(
                name=aspect,
                handler=make_handler(aspect),
                input_data=question,
                description=f"研究{aspect}"
            ))
        
        return tasks


class ConsensusGenerator:
    """共识生成器 - 通过多次生成寻找最佳答案"""
    
    @staticmethod
    def create_tasks(
        prompt: str,
        num_generations: int = 5,
        temperature_range: tuple = (0.3, 0.9)
    ) -> List[ParallelTask]:
        """
        创建共识生成任务
        
        Args:
            prompt: 提示词
            num_generations: 生成次数
            temperature_range: 温度范围
            
        Returns:
            并行任务列表
        """
        tasks = []
        temperatures = [
            temperature_range[0] + (temperature_range[1] - temperature_range[0]) * i / (num_generations - 1)
            for i in range(num_generations)
        ]
        
        for i, temp in enumerate(temperatures, 1):
            def make_handler(temperature, index):
                def handler(input_data, llm_client):
                    # 注意：GiteeAIClient.simple_chat 不支持 temperature 参数
                    # 使用默认参数调用
                    return llm_client.simple_chat(input_data)
                return handler
            
            tasks.append(ParallelTask(
                name=f"生成_{i}",
                handler=make_handler(temp, i),
                input_data=prompt,
                description=f"第{i}次生成 (temperature={temp:.2f})"
            ))
        
        return tasks

