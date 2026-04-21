---
type: concept
status: active
created: 2026-04-21
updated: 2026-04-21
source_count: 1
tags:
  - concept
  - evaluation
  - ai
---

# AI评估
## 定义
`AI评估（AI evaluation）` 指面向 AI 系统、AI 辅助工作流，以及 AI 时代的人类能力筛选而设计的评估方法。它关注的不只是“能不能测（can it be measured）”，还包括“是否还有区分度（does it still have signal）”“是否公平（is it fair）”“是否代表真实能力（does it reflect real capability）”。

## 为什么重要
随着模型能力快速提升，很多原本有效的评估正在迅速失效（many previously useful evaluations are decaying quickly）。一个过去能区分候选人或系统水平的任务，今天可能已经能被强模型轻松完成（a task that once separated strong and weak performers may now be trivial for a frontier model）。

因此，AI评估不再只是出题和打分，而是在持续回答三个问题：
- 这个评估还有没有信号？(Does this evaluation still carry signal?)
- 这个评估测到的是谁的能力？(Whose capability is this actually measuring?)
- 这个评估还能否代表真实工作或真实系统表现？(Does it still reflect real work or real system performance?)

## 我们目前对它的几个关键判断
### 1. 评估本身正在被模型能力反向压力测试
- 过去是人去做评估（humans took the test）
- 现在评估也要面对模型的直接攻击（now the evaluation itself is pressure-tested by models）
- 所以评估设计不再是静态工作，而是持续更新的系统工程（evaluation design is no longer static; it becomes an iterative systems problem）

### 2. “贴近真实工作”不再总是最优解
- 以前我们倾向于让评估尽量像真实任务（we used to optimize for realism）
- 但越像常见真实工作，越可能已被模型训练分布覆盖（the more realistic and common a task is, the more likely it is already covered by model training）
- 这意味着“真实性”和“抗模型性”之间会出现张力（realism and resistance to model exploitation can conflict）

### 3. 好评估必须同时满足多重目标
- 有足够区分度（high signal）
- 对人公平（fair to humans）
- 不被当前最强模型轻易碾过（not easily crushed by the strongest current model）
- 能在有限时间和成本内执行（feasible under practical time and cost constraints）

这几个目标常常彼此冲突，因此 AI评估天然是权衡问题（AI evaluation is inherently a tradeoff problem）。

### 4. AI时代的评估更像对抗性工程
- 不是简单把题目变难（it is not just about making tests harder）
- 而是不断调整任务形式、时间结构、反馈条件和工具边界（it is about redesigning task form, time structure, feedback conditions, and tool boundaries）
- 目标是让评估继续保有信号，而不是单纯提高门槛（the goal is to preserve signal, not merely raise the bar）

## 核心矛盾
### 1. 真实性与抗AI性
- 越像真实工作，越可能被模型快速掌握（the more realistic the task, the easier it may be for models to absorb）
- 越追求抗AI，越可能变得古怪、脱离真实场景（the more AI-resistant the task, the more artificial it may become）

### 2. 公平性与难度
- 如果任务太怪异，人类可能没有合理准备机会（if the task is too strange, humans may not have a fair chance to prepare）
- 如果任务太常规，又可能只是在测“谁更会调用模型”（if the task is too standard, it may only measure who delegates to AI more effectively）

### 3. 时间限制与真实能力
- 短时间任务更容易被模型快速压平差距（short tasks are easier for models to flatten）
- 长时间任务更可能让人类重新拉开优势（longer horizons may restore human advantage）
- 但长时间评估又更贵、更慢、更难组织（but longer evaluations are costlier, slower, and harder to run）

## 设计原则
### 1. 把评估看成可迭代系统
- 不要假设一个评估设计可以长期有效（do not assume an evaluation will remain valid for long）
- 应持续观察模型如何击穿当前评估（watch how models break the current design）
- 根据失效方式重构评估（redesign based on the failure mode）

### 2. 明确你在测什么
- 是测独立完成能力（independent performance）
- 还是测与 AI 协作后的综合产出（human+AI collaborative output）
- 还是测在受限条件下的判断、验证、调试能力（judgment, verification, and debugging under constraints）

如果这个问题不清楚，评估结果就很容易被误读（if this is unclear, the results are easy to misread）。

### 3. 允许 AI 存在时，要重新定义信号
- 不能只看最终结果（do not judge only the final output）
- 还要看策略选择、验证能力、工具判断、时间分配和纠错能力（also look at strategy choice, verification, tool judgment, time allocation, and error correction）
- 否则评估只会退化成“谁更会把任务丢给模型”（otherwise the evaluation collapses into “who delegates better”）

### 4. 用多层信号替代单点信号
- 避免把评估建立在单个灵感点上（avoid evaluations that hinge on a single trick）
- 让任务包含多次展示能力的机会（create multiple chances to demonstrate capability）
- 这样更不容易被单次幸运或单一模型策略击穿（this makes the evaluation harder to defeat through one lucky break or one dominant model strategy）

## 常见应对策略
### 1. 提高任务新颖性
- 选择更偏分布外的问题（choose more out-of-distribution problems）
- 降低模型从既有经验直接套解法的机会（reduce the chance that a model can retrieve a known pattern）

### 2. 调整时间结构
- 缩短或拉长时间窗口（shorten or lengthen the time horizon）
- 利用不同时间尺度下人和模型的相对优势变化（exploit how relative advantages shift across time scales）

### 3. 改变反馈条件
- 不提供完整调试工具（withhold full debugging support）
- 限制可见信息（limit visible information）
- 观察候选人如何主动构建验证手段（observe how people build their own validation tools）

### 4. 重构评分方式
- 不只看最后结果（do not score only the final answer）
- 也看过程质量、判断质量和工具使用质量（also evaluate process quality, judgment quality, and tool use quality）

## 与其他概念的关系
- 它和 [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]] 的关系是外部验证层（external validation layer）：前者讲怎么构建，AI评估讲怎么证明它真的有效。
- 它和 [[wiki/concepts/工具|工具（tool）]]、[[wiki/concepts/上下文工程|上下文工程（context engineering）]]、[[wiki/concepts/harness工程|harness工程]] 一样都强调 evaluation-driven，但这里评估对象更广，既包括 AI 系统，也包括 AI 时代的人类能力（both AI systems and human capability in an AI-shaped environment）。
- 它也与 [[wiki/concepts/LLM-based Agents|大语言模型智能体（LLM-based Agents）]] 相关，因为 agent 能力提升会直接改变什么样的评估还能保有区分度（agent progress changes what kinds of evaluations still work）。

## 对知识库场景的启发
- 以后如果你想评估“这个知识库 agent 是否真的有用”，不能只看它写得像不像（do not judge it only by whether the output sounds good）
- 更该看它是否更稳定、是否更少幻觉、是否更会找对资料、是否更会持续更新（look at stability, hallucination rate, retrieval quality, and maintenance quality）
- 也就是说，知识库 agent 的评估不应只看输出文本，而应看整个维护过程的质量（evaluate the maintenance process, not just the final prose）

## 相关来源
- [[wiki/sources/2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations|2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations]]

## 张力与开放问题
- 未来是否存在既真实、又公平、又抗AI的稳定评估？(Can a stable evaluation be realistic, fair, and AI-resistant at the same time?)
- 当 AI 已成为默认工作伙伴时，评估到底该测“人”，还是测“人+AI”？(When AI is the default collaborator, should we evaluate humans alone or human+AI systems?)
- 一个评估如果每隔几个月就要重做，长期成本是否可接受？(If an evaluation must be redesigned every few months, is that sustainable?)
- 对不同岗位和不同 agent 系统，AI评估是否应完全不同？(Should AI evaluation be entirely different across roles and agent types?)
