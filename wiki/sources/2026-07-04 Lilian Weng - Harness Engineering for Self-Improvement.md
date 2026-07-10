---
type: source
status: active
created: 2026-07-09
updated: 2026-07-09
tags:
  - source
  - agent
  - harness
  - self-improvement
---
# 2026-07-04 Lilian Weng - Harness Engineering for Self-Improvement
## 来源
- 标题：`Harness Engineering for Self-Improvement`
- 作者：Lilian Weng
- 日期：2026-07-04
- 原文链接：`https://lilianweng.github.io/posts/2026-07-04-harness/`
- 原始文件：`raw/assets/harness_engineering_for_self_improvement.pdf`
## 一句话总结
这篇文章把递归自我改进（recursive self-improvement, RSI）从“模型直接改自己权重”扩展为“模型通过 harness、上下文、workflow、评估、工具和部署系统改进自己的工作方式”。它的关键判断是：近期更现实的自我改进路径，不一定发生在模型参数内部，而可能先发生在模型外部的 agent runtime / harness 层。
## 核心主张
Weng 认为，raw model 和真实世界之间的部署系统同样重要。`harness` 是包在基础模型外面的系统，负责决定模型如何思考和规划、如何调用工具、如何感知和管理上下文、如何保存产物、如何评估结果。
因此，现代 self-improvement 不应只理解为：
- 模型改自己的权重
- 模型生成更多训练数据
- 模型直接 self-play
还应包括：
- 改进上下文管理机制
- 改进 workflow 和 loop
- 改进工具调用与权限控制
- 改进评估、回归测试和 trace audit
- 改进 harness 代码本身
- 甚至改进用于改进 harness 的 optimizer code
我的理解：这篇文章把我们之前讨论的“模型是灵魂、agent 是躯壳”工程化了。模型负责推理和抽象，但只有 harness 给它身体、记忆、工具、反馈和权限，它才真正能在世界里试错。
## Harness 设计模式
### 1. Workflow automation
核心是让模型进入可迭代循环，而不是一次性回答：
- 规划（plan）
- 执行（execute）
- 观察/测试（observe/test）
- 改进（improve）
- 继续执行，直到达到停止条件
这和 `loop engineering` 的语境一致：prompt 不再是中心，中心变成了一个可观察、可中断、可验证、可恢复的执行循环。
### 2. File system as persistent memory
长任务中，实验日志、代码 diff、错误 trace、论文摘要、子代理输出、历史 rollout 都会超过上下文窗口。文章认为 harness 不应把全部历史塞进上下文，而应把持久状态放进文件系统。
但这里需要补上我们的理解：文件系统更准确地说是持久工作区（persistent workspace），不是最终长期知识库。它解决的是“agent 不丢状态”和“人可以审计过程”，不自动解决“哪些内容值得长期保留”。
因此应该区分：
- `scratch/`：临时草稿，任务结束可删除
- `runs/`：执行轨迹、日志、评估结果，保留一段时间用于审计
- `artifacts/`：有交付价值的产物
- `candidate memory`：从多次执行中提炼出的候选经验
- `curated knowledge`：经过审核后进入正式知识库或规则系统的长期知识
一句话：文件是工作记忆，不是组织记忆。
### 3. Sub-agent and backend jobs
复杂任务经常需要并行探索多个假设、运行多个实验或委派互不污染上下文的子任务。harness 需要像一个小型进程管理器：
- 启动子代理或后台任务
- 检查日志和状态
- 取消失败任务
- 收集合并结果
- 把子任务产物写成可检查文件，而不是只存在 chat 里
关键设计原则是：并行必须显式、可检查、可恢复。否则子代理越多，系统越像一团不可审计的噪声。
## Harness 和核心智能的关系
文章提出一个重要预测：近期 RSI 不太可能从模型直接改写权重开始，而更可能从 harness engineering 开始。harness 会朝元方法论（meta-methodology）演进：不是只改答案，而是改“获得更好答案的机器”。
优化对象大致沿着这条线升级：
- instruction prompts
- structured context
- workflow
- harness code
- optimizer code
这条线非常重要。它说明 prompt engineering 并没有消失，而是被上移了：早期人手写 prompt；后来人设计 context；再后来人设计 workflow；再后来 agent 修改 harness；最后 agent 修改用于搜索 harness 的 optimizer。
我的判断：这不是“prompt 不重要”，而是 prompt 从显性技巧变成了系统组件。就像高级语言没有让机器码消失，而是让大多数人不直接写机器码。
## Context engineering 的自我改进
文章把上下文工程分成几个阶段。
### ACE：上下文作为可演化 playbook
Agentic Context Engineering（ACE）把上下文看作逐步演化的 playbook，而不是越来越长的 prompt blob。它有三个角色：
- Generator：生成任务轨迹，并引用已有 bullet point
- Reflector：从成功和失败轨迹中提炼 insight
- Curator：把 insight 以结构化、带编号的 bullet 写入 context logbook
关键设计是 curator 不重写整段 prompt，而是增量地产生 `(identifier, description)` 条目，再由确定性逻辑合并、去重和周期性整理。这能降低上下文反复压缩时的坍缩和偏短偏差。
### MCE：优化上下文管理机制本身
Meta Context Engineering（MCE）进一步区分两层：
- base level：在某个 skill 指导下优化具体任务上下文
- meta level：演化“如何管理上下文”的 skill
它不再强制使用某种人工设计的上下文结构，而是让 agent 搜索上下文函数、skill 和动态算子。实现上，一个 context function 可以是一组文件：`skill.md`、动态上下文、数据 rollout 等。
我的理解：ACE 像是“让记忆有结构”，MCE 像是“让记忆管理方法本身变成优化对象”。这意味着上下文工程会从软件系统层逐步向智能本身靠近。
## Workflow / agentic system 的自动设计
文章总结了几条自动研究和 workflow 搜索路线。
### AI Scientist / ScientistOne
AI Scientist 尝试自动完成研究 idea 生成、代码实现、实验运行、结果分析、论文写作和 review。ScientistOne 则把可验证性放在中心，要求每个 citation、数值、方法和结论都能追溯到证据，并通过 Chain-of-Evidence 审计。
这条线的核心不是“AI 能写论文”，而是“研究 workflow 能否被拆成可验证的证据链”。对企业场景也类似：业务分析不是写一段看起来合理的话，而是每个结论都能追溯到数据、口径、实验或系统记录。
### Autodata
Autodata 用 challenger、weak solver、strong solver、verifier/judge 生成训练和评估数据，目标是合成难度刚好的任务：强模型能做，弱模型不能做。
它的价值在于自动制造 eval/training 分布，但文章也指出，如果 loop 不能继续改进 strong model，更像是间接蒸馏或数据生成，而不是真正完整的 RSI。
### ADAS / AFlow
Automated Design of Agentic Systems（ADAS）把 agent workflow 设计变成搜索问题：meta-agent 基于已有 archive 生成新 workflow，写成代码，评估后把成功候选放回 archive。
AFlow 则把 workflow 表示成图：节点是 LLM 调用，边是代码逻辑，用 MCTS 搜索更优 workflow。
这说明 workflow 本身已经可以被当成可执行搜索空间。人工不再只写一个固定流程，而是定义搜索空间、评估函数和约束。
## Self-Harness：harness 改进自己
Self-Harness 是文章里最实用的一段。它不是让 agent 自由改自己，而是一个受限的 propose-evaluate-accept loop。
### 1. Weakness mining
先用当前 harness 在任务集上执行，收集 execution traces，再把失败聚类成 verifier-grounded failure patterns。关键是不要只看表面错误，比如 timeout、missing artifact，而要记录：
- verifier 层的终端失败原因
- 相关 agent 行为的因果状态
- trace 暴露出的抽象机制问题
这一步的意义是从“它失败了”升级到“它为什么以这种机制失败”。
### 2. Bounded harness proposal
同一个模型在受限上下文中提出 harness 改动。proposal context 应包含：
- 当前 harness 的可编辑面
- 从评估系统挖出的失败模式
- 应保留的通过行为
- 之前尝试过但失败的 edit summary
候选改动应优先解决反复出现、可定位、可通过窄改动修复的问题，而不是针对单个任务过拟合。
### 3. Proposal validation
候选改动必须同时通过：
- held-in：检查原失败是否被修复
- held-out：检查是否引入未知回归
只有没有回归的候选才能合并。被拒绝的候选也要记录下来，避免系统反复尝试同样方向。
我的理解：Self-Harness 的精髓不是“agent 可以改自己”，而是“agent 只能在受限可编辑面里提出候选，真正的合并权交给外部评估和回归测试”。这和企业自演化 agent 的治理思路高度一致。
## Evolutionary search：进化式搜索为什么适合 harness
进化式搜索适合两类问题：
- 搜索空间很大、形状很怪
- 难以直接求梯度，但候选方案容易评估
harness 正好符合：prompt、workflow、工具调用、上下文选择、子代理结构、权限策略组合起来巨大又离散。
文章列了几条代表线：
- Promptbreeder：演化 task prompt，同时演化 mutation prompt
- GEPA：用自然语言 reflection + evolutionary search 更新 prompt
- AlphaEvolve：用 coding agent 生成程序 diff，评估后保留高 fitness 候选
- ShinkaEvolve / ThetaEvolve：提高采样效率、结合 RL 和 in-context learning
- Darwin Gödel Machine（DGM）：允许 coding agent 修改自己的 harness 代码仓库，在固定模型下演化出更强 agent
DGM 的意义尤其大：它证明在基础模型固定时，仅仅演化 harness 也能显著改变系统表现。这进一步支持“能力不只在模型里，也在模型外的运行系统里”。
## Joint optimization：同时优化 harness 和权重
文章最后提到 SIA 这类方向：把 harness 改进和模型权重更新放进同一个循环。系统包括：
- Meta-Agent：提出初始 harness
- Task-Specific Agent：执行任务
- Feedback-Agent：根据轨迹选择下一轮更新 harness 还是更新模型权重
Weng 对证据保持谨慎，因为实验里有混杂因素，比如 meta/feedback agent 比 task agent 更强，baseline 也不够干净。但方向值得关注：长期来看，非参数系统（harness）和参数系统（model weights）可能会联合优化。
我的理解：短期企业落地不应该碰模型权重自更新，风险太高；但可以先做 harness 自改进的候选生成、离线评估和人工合并。
## 未来挑战
### 1. 弱而模糊的评估器
很多真实任务没有快速、精确的 verifier。科研品味、新颖性、长期价值、业务判断都很难打分。自我改进 loop 最适合客观可测任务，一旦进入模糊场景，就需要 trace audit、人工 review 和多层信号。
### 2. 上下文与记忆生命周期
记忆越长，越需要治理。长期记忆不能只是不断追加，而必须有来源、置信度、过期、引用、压缩、升格和删除机制。
### 3. 负结果
人类文献偏向成功案例，模型也容易偏向成功叙事。好的研究 harness 必须保存失败尝试，帮助系统知道何时放弃假设、报告负结果、缩小搜索空间。
### 4. 多样性坍缩
进化和 RL loop 容易围绕当前 evaluator 喜欢的模式收敛。开放式研究尤其需要保护多样性，因为真正有价值的路径一开始可能在当前评估器下看起来不优。
### 5. Reward hacking
自我改进系统会优化给定信号。如果信号是单元测试，它可能过拟合测试；如果信号是 judge model，它可能学会讨好 judge；如果信号是 benchmark，它可能利用 benchmark artifact。
因此，评估器、权限控制、安全层应该放在 harness evolution loop 外部，并使用 held-out tests、trace audits 和关键节点人工 review。
### 6. 长期成功
短期通过任务不等于长期系统健康。以 coding agent 为例，sandbox 里的任务分数不一定反映长期可维护性、ownership 边界、迁移成本、兼容性和未来排障负担。
### 7. 人的角色
文章的结论很重要：人应该上移到更高层，而不是被移出 loop。人不必审批每一步，但应该在方向、评价标准、权限边界、关键升级和长期价值判断上介入。
## 对我们当前知识库的理解增量
### 1. Harness 是 agent 的运行时和身体
之前我们把 harness 看作连续性、纠偏和交接系统。这篇进一步说明：harness 也是自我改进的主要承载层。模型像灵魂，harness 像身体；科学发现、代码修复、数仓分析这类任务都需要身体和世界产生摩擦。
### 2. 自我改进不是自由进化，而是受限搜索
真正可落地的 self-improvement 应该是：
- 可编辑面受限
- 权限和安全层在 loop 外
- 失败 trace 可审计
- held-in / held-out 验证
- 候选改动可回滚
- rejected edits 也保留
- 高风险合并需要人
### 3. 文件系统是工作区，不是知识库
这篇强调 file system as memory，但我们应该更精确地说：file system 是持久工作区。它保存轨迹、产物和中间状态；长期知识必须经过提炼、去重、验证、过期和人工/规则治理。
### 4. 企业 agent 的改进路线应先改 harness，不要先改模型
对企业来说，最现实路线不是训练一个会自我进化的大模型，而是：
- 收集真实任务和失败 trace
- 挖掘反复失败模式
- 提出小范围 harness/prompt/tool/context 改动
- 用 regression eval 验证
- 人工 review 后合并
这比开放式模型自训练更安全，也更贴近业务可控边界。
## 已整合到
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/自演化智能体风险|自演化智能体风险（Misevolution）]]
- [[wiki/syntheses/agent 工程地图|agent 工程地图（agent engineering map）]]
