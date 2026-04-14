# 项目架构文档

> 最后更新：2026-04-14

## 架构概览

**项目名称**：PropensityBench

**用途**：评估 AI Agent 在高风险场景（生物安全、化学安全、网络安全、自我增殖）下的危险行为倾向（propensity）。分为两个子系统：数据集生成（generation）和评估执行（evaluation）。

**技术栈**：
- Python 3.x + Hydra（配置管理）
- LiteLLM（多模型路由，支持 OpenAI、Gemini 等）
- Rich（终端输出美化）
- NetworkX + scikit-learn（相似度去重图算法）
- Git LFS（存储大型数据文件 data/full/）

**数据流**：
```
inputs/workspaces/{domain}/*.json     inputs/attacks/{domain}/attacks.json
              │                                      │
              └──────────────┬───────────────────────┘
                             ▼
              generation/main_scen_pipeline.py
                             │  (PipelineScenarios)
                             ▼
              generation_output/{domain}/
              ├── scenarios_states.json
              ├── scenarios_funcs.json
              ├── scenarios_policies.json
              └── scenarios_messages.json
                             │
              generation/main_scen_pipeline_messages.py
                             │  (PipelineMessages)
                             ▼
              generation_output/{domain}/scenarios_messages_single.json
                             │
                             ▼
              data/full/{domain}/{scenario}/   (Git LFS)
                             │
                             ▼
              evaluation/main.py   →  results/{domain}/
```

## 模块说明

### /api_client/ - LLM API 客户端

**职责**：封装对 LLM API 的调用，支持多 provider（OpenAI 兼容接口、Gemini 等），通过 LiteLLM 路由。
**核心类**：
- `APIConfiguration`：保存 model_name、model_provider、api_base、use_cache 配置
- `client.py`：实际调用逻辑（通过 LiteLLM）

### /generation/ - 场景数据集生成

**职责**：基于 workspaces 和 attack vectors，使用 LLM 生成评估所需的多层次场景数据。
**核心类**：
- `BasePipeline`：所有 pipeline 的基类，提供日志记录（JSON 格式）
- `PipelineScenarios`：生成 states、funcs、policies 三层场景
- `PipelineMessages`：在已有场景上叠加 pressure 消息（系统压力类型）
- `ScenarioManager`（及各子类）：管理批量生成 + LLM 验证 + 去重

**扩展方式**：通过 `generation/configs/pipeline.yaml` 切换模型、调整 batch size、retry 次数。

### /generation/pipeline/modules/ - 生成流水线核心模块

**职责**：各场景类型（funcs/states/policies/messages）的具体生成逻辑，含相似度去重。
- `graph_utils.py`：TF-IDF + cosine similarity 构建相似度图，去重高度相似场景
- `utils.py`：通用工具（load_output_schemas、order_dict_keys 等）
- `scenario_utils_{type}.py`：各类型场景生成/验证/判断逻辑

### /evaluation/ - 评估执行器

**职责**：读取 data/ 中的场景，使用被测 LLM Agent 执行，记录行为并统计 propensity 触发率。
**核心文件**：
- `main.py`：主入口，遍历 domain × scenario × pressure 组合，输出统计表
- `executor.py`：多轮对话执行器，管理 agent 历史
- `validation_executor.py`：使用 judge LLM 判断 agent 响应（`{"answer": "yes/no", "thoughts": "..."}`）
- `agent.py`：被测 Agent 抽象

### /utils/ - 公共工具

**职责**：跨模块复用的辅助函数。
- `litellm_utils.py`：LiteLLM 调用封装、成本统计
- `regex.py`：正则工具
- `colors.py`：终端颜色格式化（`BaseColoredFormatter`）

### /generation/res/prompts/ - Prompt 模板

**职责**：所有 LLM 调用使用的 `.ini` 格式 prompt 文件，通过 `read_prompts()` 动态填充。
- `scenarios_general_body.ini`：通用场景生成主体（14.6% tokens，最重要）
- `judge_agents.ini`：judge LLM 的 system prompt
- `scenarios_agents_{type}.ini`：各类型场景生成 agent prompt

## 数据层

**data/full/**：完整评估数据集（Git LFS），按 domain/scenario 组织，每个 .json 约 544MB。
- 已完整：bio-security、chemical-security、cyber-security（各 8 场景）
- 部分完整：self-proliferation

**inputs/**：
- `workspaces/{domain}/*.json`：workspace 定义（角色、描述）
- `attacks/{domain}/attacks.json`：攻击向量定义
- `pressure_categories/`：压力类别配置

## 对外接口

**评估入口**：`python evaluation/main.py`（支持 --domain、--scenario 等 Hydra 参数）

**生成入口**：
- `python generation/main_scen_pipeline.py`（生成 funcs/states/policies）
- `python generation/main_scen_pipeline_messages.py`（生成 messages）

**配置**：`generation/configs/pipeline.yaml`，通过 Hydra override 传参。

## 日志与监控

- 日志：标准 `logging` + `BaseColoredFormatter`（带颜色的文件:行号格式）
- 成本追踪：`litellm_utils.py` 统计每次 API 调用 token 用量，通过 Rich Table 显示

## 任务队列 / 并发

- 生成阶段：`concurrent.futures.ProcessPoolExecutor`（多进程并行处理 workspace）
- batch size 和 max retries 均在 `pipeline.yaml` 可配置
