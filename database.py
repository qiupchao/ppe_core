# pee_core/database.py

from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel, create_engine, Session

class PromptRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    original_prompt: str
    enhanced_prompt: str
    llm_output: str
    evaluation_result: str
    
    config: str
    context: str

class DataManager:
    """
    数据与状态管理模块。
    负责将PEE工作流中的关键数据持久化到数据库。
    """
    def __init__(self, db_url: str = "sqlite:///pee_runs.db"):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)
        print(f"[DataManager] 数据库已初始化: {db_url}")
    
    def save_run(self, data: Dict[str, Any]):
        """
        保存一次PEE工作流的完整运行数据。
        """
        print("[DataManager] 正在保存运行数据到数据库...")
        run = PromptRun(
            original_prompt=data["original_prompt"],
            enhanced_prompt=data["enhanced_prompt"],
            llm_output=data["llm_output"],
            evaluation_result=data["evaluation_result"],
            config=data["config"],
            context=data["context"]
        )
        
        with Session(self.engine) as session:
            session.add(run)
            session.commit()
            print(f"[DataManager] 数据保存成功，ID: {run.id}")