# pee_core/parser.py

import json
from openai import OpenAI
from pydantic import ValidationError
from typing import Optional, List, Dict, Any

from .data_models import PromptMetadata

class PromptParser:
    """
    提示词解析器模块。
    使用LLM将非结构化的原始提示词解析为结构化的PromptMetadata对象。
    """
    def __init__(self, client: OpenAI, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.system_prompt = """
        你是一个专业的提示词分析专家。你的任务是深入分析用户提供的原始提示词，并提取以下关键信息。
        请严格按照 JSON 格式输出，不要包含任何额外的文字或解释。
        
        JSON 格式应遵循以下结构：
        - "original_prompt": string, 原始提示词。
        - "task_type": string, 识别出的任务类型，例如 "content_creation", "code_generation", "data_analysis", "problem_solving" 等。
        - "keywords": array of string, 提取出的核心关键词列表。
        - "suggested_persona": string 或 null, 建议为LLM设定的角色，例如 "资深软件工程师", "市场营销专家", "数据科学家"。如果不需要或无法识别，则为 null。
        - "suggested_format": string 或 null, 建议的输出格式，例如 "Markdown", "JSON", "Python代码块", "表格" 等。如果不需要或无法识别，则为 null。
        - "needs_cot": boolean, 判断该任务是否需要“思维链”（Chain-of-Thought）指令以提升推理能力。
        """

    def parse(self, raw_prompt: str, context: Optional[dict] = None) -> PromptMetadata:
        """
        解析原始提示词。
        """
        print(f"[Parser] 正在使用模型 '{self.model}' 解析原始提示词: '{raw_prompt}'")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"原始提示词：{raw_prompt}"}
                ],
                response_format={"type": "json_object"}
            )
            
            json_response = response.choices[0].message.content
            parsed_data = json.loads(json_response)
            
            metadata = PromptMetadata(**parsed_data)
            print("[Parser] 解析成功，生成PromptMetadata对象。")
            return metadata
        
        except ValidationError as e:
            print(f"[Parser ERROR] Pydantic 数据验证失败: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"[Parser ERROR] LLM输出的不是有效的JSON: {e}")
            raise
        except Exception as e:
            print(f"[Parser ERROR] 调用LLM解析时发生错误: {e}")
            raise