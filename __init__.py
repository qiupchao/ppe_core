# pee_core/__init__.py

"""
这是一个“提示词增强工程 (Prompt Enhancement Engineering)”框架的核心包。
它包含实现 PEE 工作流的各个模块，如解析、增强、执行和评估。
"""

# 在这里可以导入常用的类或函数，以方便外部调用
from .engine import PEECoreEngine
from .data_models import PromptMetadata, EvaluationResult

__all__ = [
    "PEECoreEngine",
    "PromptMetadata",
    "EvaluationResult"
]