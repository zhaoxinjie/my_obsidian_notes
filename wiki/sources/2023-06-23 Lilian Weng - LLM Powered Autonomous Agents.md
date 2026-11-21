---
type: source
status: active
created: 2026-07-09
updated: 2026-07-09
tags:
  - source
  - agent
  - planning
  - memory
  - tools
---
# 2023-06-23 Lilian Weng - LLM Powered Autonomous Agents
## 来源
- 标题：`LLM Powered Autonomous Agents`
- 作者：Lilian Weng
- 日期：2023-06-23
- 原文链接：`https://lilianweng.github.io/posts/2023-06-23-agent/`
- 原始文件：`raw/assets/lilianweng-2023-06-23-agent.pdf`
## 一句话总结
这篇是早期 LLM agent 的经典综述，把 autonomous agent 拆成三个基础组件：规划（planning）、记忆（memory）和工具使用（tool use）。如果说 2026 年的 `Harness Engineering for Self-Improvement` 关注 agent runtime 如何自我改进，那么这篇 2023 年文章关注的是 agent 的基本解剖结构。
## Agent 系统总览
文章的核心框架是：
- LLM 作为 agent 的大脑（brain）
- 规划负责拆解任务、反思和修正
- 记忆负责保存短期上下文和长期知识
- 工具负责连接模型权重之外的信息、能力和外部世界
这套框架今天看仍然成立，但我们会把它放进更大的工程语境里：早期公式是 `agent = LLM + memory + tools + planning + action`；后来的 harness 工程进一步加入 workflow、评估、权限、持久状态、审计和自我改进。
## 组件一：规划
### 任务拆解
文章把任务拆解放在 agent planning 的中心。大任务需要被拆成小目标，常见方法包括：
- Chain of Thought（CoT）：让模型 step by step 地消耗更多 test-time compute
- Tree of Thoughts（ToT）：在每个思考步骤探索多条可能路径，并用 BFS/DFS、分类器或投票做搜索
- LLM+P：让 LLM 把问题翻译成 PDDL，再调用经典规划器生成 plan，最后翻译回自然语言
这里的核心不是“模型会不会想”，而是 agent 是否能把开放任务转化成可执行步骤。规划越长，越需要外部反馈和纠偏，否则模型很容易在中途偏航。
### 自我反思
文章总结了几类早期 self-reflection 方法：
- ReAct：把 reasoning 和 acting 交替组织成 `Thought -> Action -> Observation` 循环
- Reflexion：把失败轨迹和反思写入工作记忆，用于下一轮尝试
- Chain of Hindsight：把一组逐步改进的输出和反馈展示给模型，让模型学习改进趋势
- Algorithm Distillation：把跨 episode 的学习历史蒸馏进模型，使模型在上下文中表现出类似 RL 的改进
这些方法都在尝试同一件事：让 agent 不只是一次性输出，而是在环境反馈中迭代。它们是后来 loop engineering 和 harness engineering 的早期形态。
## 组件二：记忆
文章把人类记忆类比到 agent：
- 感觉记忆（sensory memory）：原始输入的 embedding 表征
- 短期记忆（short-term memory）：上下文窗口和 in-context learning
- 长期记忆（long-term memory）：外部向量库和检索系统
它介绍了 MIPS、ANN、LSH、ANNOY、HNSW、FAISS、ScaNN 等向量检索技术。放到今天看，这部分是早期 RAG / agent memory 工程的基础。
但这篇更偏“如何召回”，还没有充分处理“召回内容是否可信、是否过期、是否应该进入长期记忆”。结合后续知识库主线，长期记忆不能只是 vector store，还需要来源、置信度、更新时间、适用范围、过期策略和审计。
## 组件三：工具使用
工具使用被定义为扩展模型能力边界的关键方式。模型权重难以及时更新，工具可以提供：
- 当前信息
- 代码执行能力
- 私有数据访问
- 专业工具和外部 API
文章涉及的典型系统包括：
- MRKL：LLM 作为 router，在神经模块和符号工具之间选择
- TALM / Toolformer：让模型学习何时调用外部 API
- HuggingGPT：LLM 负责任务规划、模型选择、任务执行协调和结果总结
- API-Bank：评估 tool-augmented LLM 的 benchmark
API-Bank 的三级能力很有复用价值：
- Level 1：给定 API 描述，判断是否调用、正确调用并处理返回
- Level 2：先检索合适 API，再读文档学会调用
- Level 3：面对模糊需求，规划多个 API 调用完成任务
我的理解：企业 agent 的工具评估也可以沿用这三层。很多系统只测 Level 1，其实真正业务价值往往在 Level 2 和 Level 3。
## 案例
### ChemCrow / 科学发现 agent
ChemCrow 用 GPT-4 加 13 个化学工具处理有机合成、药物发现和材料设计任务。文章里一个重要观察是：LLM-as-judge 认为 GPT-4 和 ChemCrow 接近，但专家人评认为 ChemCrow 明显更好。
这说明专业领域里，模型自评或通用 LLM judge 很可能不知道自己错在哪里。越是高专业、高风险领域，越需要领域专家、确定性检查、外部证据和 trace audit。
### Boiko et al. 的科学实验 agent
这个 agent 能浏览互联网、读文档、执行代码、调用机器人实验 API、调用其他 LLM。它能为“开发新型抗癌药”这类目标规划趋势调研、靶点选择、结构生成和合成步骤。
同时，文章提到化学武器/生物安全风险：在 11 个已知化学武器请求中，4 个被接受并尝试获取合成方案。这说明工具增强 agent 的安全风险不只是“说错话”，而是会主动查资料、规划步骤和尝试执行。
### Generative Agents
Generative Agents 用 25 个 LLM 控制的虚拟角色在沙盒里互动。它的记忆系统包括：
- memory stream：用自然语言记录观察和事件
- retrieval model：根据 recency、importance、relevance 召回记忆
- reflection：把低层观察综合成更高层推断
- planning/reacting：把记忆、计划和环境信息转成行为
这里最值得沉淀的是三因子记忆召回：
- recency：越近的记忆越重要
- importance：越核心的记忆越重要
- relevance：越贴近当前情境的记忆越重要
这比简单向量相似度更接近真实 agent 记忆管理。
### AutoGPT / GPT-Engineer
AutoGPT 和 GPT-Engineer 代表早期 agent 原型：靠系统 prompt、命令列表、JSON 格式、文件读写和自我批评组织行为。它们很有启发，但也暴露出早期 agent 的脆弱性：大量工程代码都在处理格式解析、上下文限制和模型输出不稳定。
## 文章指出的挑战
### 1. 上下文长度有限
历史信息、详细指令、API 文档、工具返回和自我反思都会挤占上下文窗口。向量库能缓解，但检索表示不等于 full attention。
### 2. 长期规划和任务拆解困难
LLM 在长历史上规划和探索仍然不稳，遇到意外错误时调整能力弱于人类试错。
### 3. 自然语言接口不可靠
早期 agent 大量依赖自然语言或 JSON 作为 LLM 与外部组件之间的接口。模型可能格式错误、拒绝遵循指令或产生难以解析的输出，因此很多 demo 代码都在处理 parsing。
## 和 2026 harness 文章的关系
这两篇可以组成一条清晰时间线：
- 2023：Agent = LLM + planning + memory + tools
- 2026：Harness = workflow + eval + permissions + persistent state + self-improvement
2023 年的问题是“agent 由哪些组件构成”；2026 年的问题是“这些组件如何被运行时系统组织、评估、治理，并进一步自我改进”。
## 对我们当前知识库的理解增量
- `ReAct` 的 `Thought -> Action -> Observation` 是现代 loop 的早期原型
- 记忆不能只理解为向量库，至少要考虑 recency、importance、relevance 以及治理
- 工具使用能力可以分层评估：调用、检索、组合规划
- LLM-as-judge 在专业领域容易失真，必须引入专家或可验证证据
- 早期 agent 的核心挑战：上下文有限、长期规划不稳、自然语言接口脆弱，后来 harness 工程基本都在回应这些问题
## 已整合到
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/syntheses/agent 工程地图|agent 工程地图（agent engineering map）]]
