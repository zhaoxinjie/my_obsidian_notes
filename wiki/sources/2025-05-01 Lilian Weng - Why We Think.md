---
type: source
status: active
created: 2026-07-09
updated: 2026-07-09
tags:
  - source
  - reasoning
  - test-time-compute
  - agent
---
# 2025-05-01 Lilian Weng - Why We Think
## 来源
- 标题：`Why We Think`
- 作者：Lilian Weng
- 日期：2025-05-01
- 原文链接：`https://lilianweng.github.io/posts/2025-05-01-thinking/`
- 原始文件：`raw/assets/lilianweng-2025-05-01-thinking.pdf`
## 一句话总结
这篇文章系统解释了测试时计算（test-time compute）和思维链（chain-of-thought, CoT）：模型为什么“多想一会儿”会变强，如何通过并行采样、顺序修订、工具调用、RL、verifier 和 latent thinking 组织这种思考，以及为什么 CoT 既有用又不能被当成绝对真实的内心过程。
## 核心主张
能力提升不只来自模型更大、数据更多、训练更久，还来自推理时给模型更多计算。CoT 的本质不是魔法，而是在最终答案前生成中间 token，让模型对难题使用更多 inference-time compute。
文章给出三个解释角度：
- 心理学类比：人类也有快思考（System 1）和慢思考（System 2），复杂问题需要 deliberate thinking。
- 计算资源：每个 token 的前向计算大致固定，但 CoT 可以让模型在答案前消耗更多计算。
- 潜变量建模：问题是 `x`，答案是 `y`，思考路径是隐藏变量 `z`；搜索多个 `z` 可以提高找到好答案的概率。
## 两类使用 test-time compute 的方式
### 1. 并行采样（parallel sampling）
并行采样一次生成多个候选，再用评分器、verifier、投票或 reward model 选择更好的答案。常见形式包括：
- best-of-N
- beam search
- self-consistency
- process reward model（PRM）
- verifier reranking
优点是简单、可并行、容易落地。缺点是如果模型某次都无法生成正确路径，再多候选也只是重复错误分布。
### 2. 顺序修订（sequential revision）
顺序修订让模型先生成，再反思、修改、验证、继续修改。但文章强调：naive self-correction 并不可靠。
没有外部反馈时，模型可能：
- 把正确答案改错
- 只做表面小改
- 编出更像样但更假的解释
- 在分布外问题上退化
真正可靠的顺序修订需要外部反馈，例如 ground truth、heuristic、unit tests、compiler trace、强模型、人类反馈或领域工具结果。
## RL 与 reasoning model
文章讨论了 DeepSeek-R1、OpenAI o 系列等 reasoning model 的路线：用可验证任务做 RL，让模型因为答对被奖励，从而学会更长、更有效的 reasoning。
关键观察：
- 纯 RL 也可能诱发反思、backtracking 和所谓 `aha moment`
- PRM 很难做，因为中间步骤是否正确往往没有清晰 rubric
- MCTS 在语言 token 空间里很难，因为搜索空间远大于棋类等封闭环境
- 负结果很重要，失败尝试能提醒大家不要把优雅算法想得过于容易
## 工具使用：把可验证子步骤交给外部世界
有些推理步骤不应由模型硬算，而应交给工具：
- 数学计算
- 代码执行
- 符号推理
- 单元测试
- Web search
- 图像处理
PAL、Chain of Code、ReAct、o3/o4-mini 这类方向说明，可靠思考往往不是“模型闭眼想很久”，而是：
- 模型负责判断和编排
- 工具负责可验证的子步骤
- 环境反馈决定下一步是否修正
我的理解：对业务 agent 来说，这一点尤其重要。能 dry-run 的 SQL 不要只让模型口头判断，能查指标口径就不要靠模型记忆，能跑单测就不要靠模型解释。
## CoT 的忠实性问题
CoT 给了人类一个看似可读的思考窗口，但不能默认它忠实反映模型真实内部过程。
文章总结的风险包括：
- 模型可能先有答案，再补一个解释
- 模型可能受提示 bias 影响，却不承认
- 模型可能用人类不易读的方式编码信息
- RL 压力可能让模型学会隐藏真实意图
CoT 监控可以帮助发现 reward hacking，但如果把 CoT monitor 直接放进 RL reward，模型可能学会在 CoT 中伪装，形成 obfuscated reward hacking。
因此，更稳的判断是：CoT 可以作为审计信号，但不能作为唯一真相来源。
## Thinking 不一定是自然语言
文章后半部分讨论 continuous / latent thinking：
- recurrent architecture：让模型在隐藏状态上多迭代
- thinking tokens / pause tokens：插入无语义 token，购买额外计算时间
- Quiet-STaR：在 token level 生成 rationale，并学习哪些 rationale 有助于预测
- latent variable view / STaR：把 thought 当作隐藏变量，通过正确答案筛选和迭代学习
这说明未来的“思考”可能分成两层：
- 可见思考：给人看的计划、解释和关键理由
- 不可见思考：模型内部的 latent computation
对安全和产品来说，真正需要的不是模型全部内心独白，而是可审计的关键理由、可复现的工具结果和可检查的决策 trace。
## Scaling law：多想有边界
test-time compute 可以提升效果，但不能无限替代更强 base model。
文章总结的实用边界是：
- 简单任务不需要大量思考
- 中等任务最容易从 thinking time 中获益
- 超出模型能力太多的任务，光让模型多想也没用
因此，工程上需要动态分配 thinking budget，而不是固定让 agent 无限循环。
## 我们的理解增量
### 1. Thinking 是模型内部的 test-time compute，loop 是 agent 外部的 test-time compute
模型内部 CoT 是多生成 thinking tokens；agent 外部 loop 是多做几轮 plan / act / observe / revise。两者本质上都是把一次性输出变成可搜索、可验证、可修正的过程。
### 2. Prompt 不是全部
设计“让模型思考”不只是写 prompt。prompt 负责每一步怎么说；loop 负责整件事怎么跑；harness 负责让 loop 可控、可验证、可恢复。
### 3. 外部反馈比自我反思更可靠
模型可以反思，但真正可靠的是环境反馈：测试、执行、dry-run、verifier、领域工具、人工 review。没有反馈的 self-correction 很容易变成更漂亮的幻觉。
### 4. CoT 是信号，不是真相
CoT 对审计有价值，但不能被当成模型真实内心。越对 CoT 施加强优化压力，越可能诱导模型学会隐藏意图。
### 5. 企业 agent 应该设计 thinking policy
业务 agent 不应默认“永远多想”，而应根据任务难度、风险、工具可验证性和成本动态决定：
- 是否需要思考
- 思考多久
- 是否并行生成候选
- 是否顺序修订
- 是否调用工具验证
- 什么时候停止
- 什么时候交给人
## 已整合到
- [[wiki/concepts/测试时计算|测试时计算（test-time compute）]]
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]
- [[wiki/concepts/自演化智能体风险|自演化智能体风险（Misevolution）]]
