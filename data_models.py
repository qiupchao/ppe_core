# pee_core/data_models.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PromptMetadata(BaseModel):
    original_prompt: str
    task_type: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    suggested_persona: Optional[str] = None
    suggested_format: Optional[str] = None
    needs_cot: bool = False
    
    # 增强后的消息历史列表，用于传递给LLM
    message_history: List[Dict[str, Any]] = Field(default_factory=list)