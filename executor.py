# pee_core/executor.py

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from typing import List, Dict, Any, Optional

class LLMExecutor:
    """
    LLM执行器模块。
    负责将增强后的消息历史发送给LLM并获取响应。
    """
    def __init__(self, client: OpenAI, model: str = "gpt-3.5-turbo"):
        self.client = client
        self.model = model
        print(f"[Executor] LLM执行器已初始化，默认模型: {self.model}")

    def execute(self, message_history: List[Dict[str, Any]]) -> str:
        """
        执行消息历史中的对话，并返回LLM的文本响应。

        参数:
        - message_history: 增强后的消息历史列表，符合OpenAI API的格式。

        返回:
        - LLM的文本输出。
        """
        print(f"[Executor] 正在调用模型 '{self.model}' 执行任务...")
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.model,
                messages=message_history,
                temperature=0.7
            )
            
            output_content = response.choices[0].message.content
            print("[Executor] LLM执行完成，成功返回结果。")
            return output_content
        except Exception as e:
            print(f"[Executor ERROR] 调用LLM时发生错误: {e}")
            raise