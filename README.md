## PEE框架简介

**提示词增强工程（PEE）框架**是一个模块化的原型系统，旨在将“提示词增强工程”的理念付诸实践。它将一个复杂的任务分解为六个相互独立又协作的模块，实现了从原始提示词到结构化增强、LLM执行、评估和数据持久化的完整自动化流程。



### 文件结构



为了清晰起见，整个框架代码可以组织在 `pee_core` 文件夹下，并包含以下文件：

```
pee_core/
├── __init__.py         # 初始化文件
├── data_models.py      # Pydantic数据模型
├── database.py         # 数据持久化模块 (SQLModel)
├── evaluator.py        # 评估与反馈模块
├── executor.py         # LLM执行器模块
├── parser.py           # 提示词解析器模块
├── strategies.py       # 增强策略模块
└── engine.py           # 核心引擎模块 (主入口)
```

下面是每个模块的完整代码。

------



### 1. 核心引擎模块 (Core Engine)



这是框架的主入口和工作流编排中心。它负责实例化和协调其他所有模块，并执行完整的 PEE 工作流。

**文件: `pee_core/engine.py`**



### 2. 提示词解析器模块 (Prompt Parser)



该模块使用 LLM 将原始提示词转化为结构化的 `PromptMetadata` 对象。

**文件: `pee_core/parser.py`**



### 3. 增强策略模块 (Enhancement Strategies)



该模块包含可插拔的增强策略，负责根据元数据对提示词进行具体优化。

**文件: `pee_core/strategies.py`**



### 4. LLM执行器模块 (LLM Executor)



该模块封装了 LLM 的 API 调用，并负责将增强后的提示词发送给大模型。

**文件: `pee_core/executor.py`**



### 5. 评估与反馈模块 (Evaluation Module)



该模块使用另一个 LLM 对输出质量进行自动化评估，并返回结构化的评估结果。

**文件: `pee_core/evaluator.py`**



### 6. 数据与状态管理模块 (Data & State)



该模块负责将每次运行的完整数据持久化到数据库，实现版本控制和历史记录。

**文件: `pee_core/database.py`**



### 7.数据模型 (Data Models)



这是框架中使用的 Pydantic 数据模型，确保数据在模块间传递时的结构化和类型安全。

**文件: `pee_core/data_models.py`**



### 8. init文件

 模块包的标识文件。

**文件: `pee_core/__init__.py`**





好的，这是为我们开发的**提示词增强工程（PEE）框架**准备的一份详细使用指南。这份指南将帮助用户快速上手，了解如何配置、运行以及扩展这个框架。



## PEE 框架使用指南





#### 1. 框架简介



我们开发的 `PEE-Core` 框架是一个模块化的 Python 库，旨在将提示词从一个简单的文本字符串升级为可管理、可优化和可自动化的“软件资产”。它通过一个完整的工作流，将用户的原始提示词自动增强为更具鲁棒性、更明确的提示词，从而提高大型语言模型（LLM）的输出质量和稳定性。

核心工作流程：

原始提示词 -> 解析 -> 增强 -> LLM执行 -> 评估 -> 数据存储



#### 2. 环境准备



在使用框架之前，请确保你的环境已正确配置。

2.1. 安装依赖

该框架依赖于以下 Python 库：

- `openai`：用于调用 OpenAI 的 API。
- `pydantic`：用于数据模型的类型安全验证。
- `sqlmodel`：用于数据库 ORM，基于 `Pydantic` 和 `SQLAlchemy`。

你可以通过以下命令一次性安装所有依赖：

Bash

```
pip install openai pydantic sqlmodel
```

2.2. 设置 API Key

框架通过 openai 库调用 OpenAI API。你必须将你的 API Key 设置为环境变量。在终端中执行以下命令：

Bash

```
export OPENAI_API_KEY="你的_OpenAI_API_密钥"
```

或者，在 `.env` 文件中配置，并使用 `python-dotenv` 库加载。



#### 3. 基本使用



要使用框架，你只需要在你的代码中实例化 `PEECoreEngine` 类，并调用其 `run` 方法。

**示例代码:**

Python

```
import os
from pee_core.engine import PEECoreEngine

# 1. 确保环境变量已设置
# os.environ["OPENAI_API_KEY"] = "你的_OpenAI_API_密钥" 

# 2. 实例化核心引擎，并配置模型版本
try:
    engine = PEECoreEngine(config={
        "parser_model": "gpt-4o",       # 用于解析提示词的强大模型
        "executor_model": "gpt-3.5-turbo", # 用于执行任务的经济高效模型
        "evaluator_model": "gpt-4o"     # 用于评估输出质量的强大模型
    })
    
    # 3. 定义用户原始提示词
    user_prompt = "帮我写一篇关于人工智能未来趋势的文章，强调其在医疗领域的应用。"
    
    # 4. 运行工作流
    result = engine.run(user_prompt)
    
    # 5. 打印结果
    print("\n--- 完整运行结果 ---")
    print(f"原始提示词: {result['original_prompt']}")
    print(f"增强后提示词:\n{result['enhanced_prompt']}")
    print(f"LLM输出:\n{result['llm_output']}")
    print(f"评估结果:\n{result['evaluation_result']}")

except ValueError as e:
    print(f"框架运行错误: {e}")
except Exception as e:
    print(f"发生意外错误: {e}")
```



#### 4. 核心配置 (`config`)



`PEECoreEngine` 的 `config` 参数是一个字典，你可以用它来控制框架的行为。

- `parser_model`：指定用于解析用户提示词的 LLM 模型。建议使用能力较强的模型（如 `gpt-4o`）以确保准确理解意图。
- `executor_model`：指定用于执行最终任务的 LLM 模型。可以根据性能和成本的权衡来选择（如 `gpt-3.5-turbo`）。
- `evaluator_model`：指定用于评估输出质量的 LLM 模型。建议使用强大的模型（如 `gpt-4o`）以获得更可靠的评估结果。
- `db_url`：指定数据库连接 URL。默认为 `sqlite:///pee_runs.db`，会将所有运行数据保存在当前目录下的一个 SQLite 文件中。



#### 5. 模块化与扩展性



框架的模块化设计是其最大的优势。你可以轻松地扩展或替换任何模块。

5.1. 扩展增强策略

如果你想添加一个例如“语言风格增强”或“任务分解”的新策略，只需执行以下步骤：

1. 创建一个继承自 `pee_core.strategies.EnhancementStrategy` 的新类。
2. 在 `apply` 方法中实现你的增强逻辑。
3. 在 `pee_core/engine.py` 的 `__init__` 方法中，将你的新策略类添加到 `enhancer` 的 `strategies` 列表中。

Python

```
# 示例：添加一个自定义增强策略
from pee_core.strategies import EnhancementStrategy
from pee_core.data_models import PromptMetadata

class MyCustomStrategy(EnhancementStrategy):
    def apply(self, metadata: PromptMetadata) -> PromptMetadata:
        # 实现你的逻辑
        return metadata

# 在 engine.py 的 __init__ 中
self.enhancer = EnhancementEngine(strategies=[
    PersonaStrategy(),
    CoTStrategy(),
    MyCustomStrategy()  # 将你的新策略添加进来
])
```

5.2. 替换 LLM 客户端

如果你想使用 Anthropic 或 Google 的 LLM，只需创建一个新的 Executor 类来封装其 API。

1. 创建一个新的 `AnthropicExecutor` 类，实现与 `LLMExecutor` 相同的 `execute` 方法接口。
2. 在 `pee_core/engine.py` 中，将 `self.executor` 替换为你的新类实例。



#### 6. 数据管理



每次 `run` 调用都会将所有关键数据（原始提示、增强提示、LLM输出、评估结果等）持久化到 `pee_runs.db` 文件中。你可以使用 SQLite 工具或 Python 库（如 `sqlite3`）来浏览和分析这些数据，进行版本比较或模型性能分析。



#### 7. 下一步的开发方向

- **Web API 接口：** 使用 FastAPI 或 Flask 封装核心引擎，提供一个 RESTful API 服务。
- **用户界面：** 开发一个简单的 Web UI，让用户可以输入提示词，并可视化看到增强和评估过程。
- **优化循环：** 开发一个自动反馈循环，根据评估结果自动调整增强策略，实现自我优化。

