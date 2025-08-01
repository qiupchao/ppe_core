import json
from openai import OpenAI
import os
from typing import Optional, List, Dict, Any

from .data_models import PromptMetadata
from .parser import PromptParser
from .strategies import EnhancementEngine, PersonaStrategy, CoTStrategy, OutputFormatStrategy
from .executor import LLMExecutor
from .evaluator import EvaluationModule
from .database import DataManager

class PEECoreEngine:
    """
    提示词增强工程的核心引擎。
    负责编排整个工作流，并协调各个模块。
    """
    def __init__(self, config: Optional[dict] = None):
        print("[Core Engine] 核心引擎初始化...")
        self.config = config if config else {}
        
        # 从环境变量获取 API Key，确保安全性
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("环境变量 'OPENAI_API_KEY' 未设置。请设置你的API密钥。")

        self.openai_client = OpenAI(api_key=api_key)

        # 实例化 PromptParser
        self.parser = PromptParser(client=self.openai_client, model=self.config.get("parser_model", "gpt-4o"))
        
        # 实例化 EnhancementEngine 并配置策略列表
        self.enhancer = EnhancementEngine(strategies=[
            PersonaStrategy(),
            CoTStrategy(),
            OutputFormatStrategy()
        ])
        
        # 实例化 LLMExecutor
        self.executor = LLMExecutor(
            client=self.openai_client, 
            model=self.config.get("executor_model", "gpt-3.5-turbo")
        )

        # 实例化 EvaluationModule
        self.evaluator = EvaluationModule(
            client=self.openai_client, 
            model=self.config.get("evaluator_model", "gpt-4o")
        )

        # 实例化 DataManager
        self.data_manager = DataManager(db_url=self.config.get("db_url", "sqlite:///pee_runs.db"))
        
        print("[Core Engine] 所有模块加载完成。")

    def run(self, raw_prompt: str, context: Optional[dict] = None) -> dict:
        """
        执行完整的PEE工作流，从原始提示词到最终输出。
        
        参数:
        - raw_prompt: 用户输入的原始提示词。
        - context: 包含历史信息或用户偏好的上下文数据。
        
        返回:
        一个包含完整工作流结果的字典。
        """
        print("\n[Core Engine] ----- PEE工作流开始 -----")
        
        # 1. 提示词解析
        metadata = self.parser.parse(raw_prompt, context)
        
        # 2. 应用增强策略
        metadata.message_history.append({"role": "user", "content": metadata.original_prompt})
        metadata = self.enhancer.apply(metadata)
        
        # 3. LLM执行
        llm_output = self.executor.execute(metadata.message_history)
        
        # 4. 评估与反馈
        enhanced_prompt_summary = json.dumps(metadata.message_history, indent=2, ensure_ascii=False)
        evaluation_result = self.evaluator.evaluate(enhanced_prompt_summary, llm_output)
        
        print("\n[Core Engine] ----- PEE工作流结束 -----")
        
        # 5. 数据持久化
        run_data = {
            "original_prompt": raw_prompt,
            "enhanced_prompt": enhanced_prompt_summary,
            "llm_output": llm_output,
            "evaluation_result": evaluation_result.model_dump_json(),
            "config": json.dumps(self.config),
            "context": json.dumps(context or {})
        }
        self.data_manager.save_run(run_data)
        
        return run_data

if __name__ == "__main__":
    # --- 运行示例 ---
    # 确保在运行前设置环境变量 OPENAI_API_KEY
    # export OPENAI_API_KEY="your-api-key"
    
    try:
        # 初始化核心引擎
        engine = PEECoreEngine(config={
            "parser_model": "gpt-4o",
            "executor_model": "gpt-3.5-turbo",
            "evaluator_model": "gpt-4o",
            "db_url": "sqlite:///pee_runs.db"
        })
        
        user_prompt = "帮我写一篇关于人工智能未来趋势的文章，强调其在医疗领域的应用，并以markdown格式输出。"
        
        result = engine.run(user_prompt)
        
        print("\n[Core Engine] ----- 最终结果概览 -----")
        print("原始提示词:", result["original_prompt"])
        print("增强后提示词:\n", result["enhanced_prompt"])
        print("LLM输出:\n", result["llm_output"])
        print("评估结果:\n", result["evaluation_result"])
        print("本次运行数据已保存至 pee_runs.db 文件中。")
    except ValueError as e:
        print(f"配置错误: {e}")