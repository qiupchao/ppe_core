# pee_core/strategies.py

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from .data_models import PromptMetadata

# 增强策略的抽象基类
class EnhancementStrategy(ABC):
    """
    所有增强策略都必须继承此抽象基类，并实现 apply 方法。
    """
    @abstractmethod
    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        """
        根据 PromptMetadata 对提示词进行增强。
        """
        pass

# 具体的增强策略实现

class PersonaStrategy(EnhancementStrategy):
    """
    角色设定策略：如果元数据中建议了角色，则在提示词中添加角色指令。
    """
    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        if metadata.suggested_persona:
            print(f"[Strategy: Persona] 应用角色设定: {metadata.suggested_persona}")
            metadata.message_history.insert(0, {"role": "system", "content": f"你是一个{metadata.suggested_persona}。"})
        return metadata

class CoTStrategy(EnhancementStrategy):
    """
    思维链策略：如果元数据中指示需要CoT，则在提示词中添加指令。
    """
    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        if metadata.needs_cot:
            print("[Strategy: CoT] 应用思维链指令。")
            metadata.message_history[1]['content'] = "为了确保准确性，请一步步思考你的答案，然后给出最终结论。\n\n" + metadata.message_history[1]['content']
        return metadata

class OutputFormatStrategy(EnhancementStrategy):
    """
    输出格式策略：如果元数据中建议了输出格式，则添加格式要求。
    """
    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        if metadata.suggested_format:
            print(f"[Strategy: Format] 应用输出格式要求: {metadata.suggested_format}")
            metadata.message_history[1]['content'] += f"\n\n请使用{metadata.suggested_format}格式输出。"
        return metadata

class EnhancementEngine:
    """
    增强策略引擎：负责管理和按序执行所有增强策略。
    """
    def __init__(self, strategies: Optional[List[EnhancementStrategy]] = None):
        self.strategies = strategies if strategies is not None else []

    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        """
        按顺序应用所有注册的增强策略。
        """
        for strategy in self.strategies:
            metadata = strategy.apply(metadata)
        return metadata