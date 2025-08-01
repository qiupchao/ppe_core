# pee_core/evaluator.py

import json
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any

class EvaluationResult(BaseModel):
    quality_score: float = Field(..., description="输出质量的评分，范围0-1")
    completeness_score: float = Field(..., description="输出内容完整度的评分，范围0-1")
    strengths: List[str] = Field(default_factory=list, description="输出的优点列表")
    improvements: List[str] = Field(default_factory=list, description="改进建议列表")

class EvaluationModule:
    """
    评估与反馈模块。
    使用LLM对另一个LLM的输出进行自动化评估。
    """
    def __init__(self, client: OpenAI, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.system_prompt = """
        你是一位专业的AI输出评估专家。你的任务是评估LLM针对给定任务的输出质量。
        请根据任务、增强后的提示词和LLM的实际输出来进行评估，并严格按照 JSON 格式返回评估结果，不要包含任何额外的文字。
        
        JSON格式应遵循以下结构：
        - "quality_score": float, 整体输出质量的评分，范围0-1。
        - "completeness_score": float, 输出内容的完整度评分，范围0-1。
        - "strengths": array of string, 指出输出的优点。
        - "improvements": array of string, 给出具体的改进建议。
        """

    def evaluate(self, enhanced_prompt_summary: str, llm_output: str) -> EvaluationResult:
        """
        评估LLM的输出质量。
        """
        print(f"[Evaluator] 正在使用模型 '{self.model}' 评估LLM的输出...")
        try:
            user_message = f"""
            任务：{enhanced_prompt_summary}
            
            LLM输出：
            ---
            {llm_output}
            ---
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            
            json_response = response.choices[0].message.content
            parsed_data = json.loads(json_response)
            
            evaluation_result = EvaluationResult(**parsed_data)
            print("[Evaluator] 评估成功，生成结构化评估结果。")
            return evaluation_result
        
        except ValidationError as e:
            print(f"[Evaluator ERROR] Pydantic 数据验证失败: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"[Evaluator ERROR] LLM输出的不是有效的JSON: {e}")
            raise
        except Exception as e:
            print(f"[Evaluator ERROR] 调用LLM评估时发生错误: {e}")
            raise