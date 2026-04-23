---
type: concept
status: active
created: 2026-04-21
updated: 2026-04-22
source_count: 2
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

## 评估的基本结构（eval anatomy）
如果我们把一个 eval 当作工程系统来看，最基础的组成通常包括：

### 1. 任务（task）
- 一条具体测试用例（test case）
- 有明确输入、环境和成功标准
- 它回答的是：要测的具体问题是什么

### 2. 试次（trial）
- 同一个任务的一次独立尝试（independent attempt）
- 因为模型输出有随机性，所以单次结果通常不够稳
- 多次 trial 能帮助我们看一致性，而不只是最好的一次

### 3. 评分器（grader）
- 用来判断成功与否的逻辑（scoring logic）
- 可以是确定性检查、测试脚本、静态分析，也可以是 LLM-as-judge
- 一个任务可以有多个 grader，分别检查不同维度

### 4. 轨迹（transcript / trace）
- 一次 trial 的完整执行记录
- 包括提示、工具调用、环境变化、中间结果、最终输出
- 这不是附属材料，而是排障、校准和发现评分缺陷的核心依据

如果没有清楚区分这四层，团队很容易把“任务设计问题”“评分器 bug”“模型随机波动”“环境噪音”混在一起。

## 能力评估与回归评估（capability vs regression evals）
这两类评估不能混用，因为它们服务的目标不同。

### 1. 能力评估（capability evals）
- 关注：系统现在到底能做什么（what the agent can do）
- 任务通常更难，起始通过率可以较低
- 作用是给团队一个“要往上爬的坡（hill to climb）”

这类评估更适合：
- 新能力验证
- 模型升级比较
- prompt / harness / tool 改动前后的能力观察

### 2. 回归评估（regression evals）
- 关注：系统是不是把以前会做的事情弄坏了（does it still do what it used to do）
- 通过率通常应接近 100%
- 一旦掉分，默认说明有问题，而不是“模型今天运气不好”

这类评估更适合：
- 每次提交后的自动检查
- 模型切换前后的稳定性对比
- 保护关键工作流不被意外破坏

### 3. 两者的关系
- 能力评估回答“能不能爬上去”
- 回归评估回答“会不会掉下来”

一个成熟系统通常两套都需要。只做 capability eval，会高估进步；只做 regression eval，会失去创新方向。

## Eval 到底怎么做（practical workflow）
如果从零开始做 AI agent 的 eval，我更推荐下面这条实操路径。

### 1. 先明确“成功”长什么样
- 不要先急着写 benchmark
- 先把“什么算好”说清楚
- 如果团队里两个人对成功标准的理解不同，先解决这个问题

这一步的产出应至少包括：
- 任务目标
- 约束条件
- 失败方式
- 最低可接受结果

### 2. 先收集 20 到 50 个真实任务
- 不必一开始就追求几百条任务
- 早期小样本往往已经足够看出系统性问题
- 最好的任务来源，通常是：真实失败案例、用户反馈、内部 dogfooding 问题、线上事故回放

如果一条 task 不是来自真实需求，而只是“看起来像题目”，它的长期价值通常会更低。

### 3. 给任务分层
一开始就把任务混在一起，后面会很难解释结果。更稳的做法是至少做这几层：
- 核心成功任务：系统必须稳定完成
- 边界任务：最容易出错的场景
- 挑战任务：当前能力还不稳定，但未来想提升的任务

这样分层后，capability 和 regression 两套 eval 也更容易拆开。

### 4. 先做确定性 grader（deterministic grader）
只要能用测试、脚本、断言、结构检查解决，就优先不用 LLM judge。

典型做法包括：
- 单元测试（unit tests）
- 集成测试（integration tests）
- 状态断言（state assertions）
- 输出格式检查
- 关键字段比对

确定性 grader 的优势是：
- 便宜
- 稳
- 好调试

### 5. 再补 LLM-as-judge
有些维度天然不容易写死，比如：
- 是否“做得好”
- 是否满足复杂主观要求
- 是否足够自然

这时可以引入 LLM judge，但要注意：
- rubric 要清楚
- 最好拆成多个维度分别判断
- 要定期和人工判断做校准（human calibration）
- 要允许模型返回 `Unknown` 之类的退出项，避免硬判

### 6. 搭好评估运行环境（eval harness）
agent eval 很容易被“不是 agent 本身的问题”污染，所以 harness 很重要。

至少要保证：
- 每个 trial 尽量从干净环境开始
- 不共享会污染结果的状态
- 环境配置尽量稳定
- 测的 agent 与生产 agent 尽量一致

否则你最后测到的，可能是：
- 缓存命中
- 残留文件
- 资源抢占
- 环境抖动

而不是 agent 真实能力。

### 7. 读 transcript，不要只看分数
分数能告诉你“出问题了”，但往往不能告诉你“为什么出问题”。

真正有价值的动作通常是：
- 找低分样本
- 读 transcript
- 区分是任务问题、grader 问题、环境问题，还是 agent 问题

很多“模型退化”最后都会被发现其实是：
- grader 写错
- task 规格模糊
- harness 不稳定
- 合法解被评分器错杀

### 8. 把 eval 变成持续机制
好的 eval 不是一次性项目，而是活文档（living artifact）。

更稳的维护方式通常是：
- 核心基础设施有人负责
- 任务由最懂业务的人持续补
- 每次新能力开发时，就同时补相应 eval
- 模型升级时先跑整套评估，再决定是否切换

## 一套够用的最小落地方案（minimum viable eval stack）
如果现在就要开始做，而不是写完整平台，我建议从这个最小组合开始：

### 1. 一个任务集
- 先收 20 到 50 个真实任务
- 用 markdown、json 或 yaml 管理都可以

### 2. 一个运行脚本
- 能批量跑 agent
- 每条 task 记录结果、时间、成本、日志

### 3. 一个 grader 层
- 优先确定性检查
- 必要时再加 LLM judge

### 4. 一份 transcript 存档
- 至少能回看失败任务的完整轨迹

### 5. 两个分组
- capability
- regression

只要先把这 5 个东西搭起来，就已经比“靠感觉改 agent”强很多。

## 评估不是全部（evals plus other signals）
自动化 eval 很重要，但它不是完整真相（ground truth）。

更稳的做法是把它和这些信号放在一起看：
- 生产监控（production monitoring）
- A/B 测试（A/B testing）
- 用户反馈（user feedback）
- 人工 transcript review
- 定期人工标注校准

可以把它理解成“多层瑞士奶酪（Swiss cheese model）”：
- 任意一层都会漏问题
- 多层叠起来，系统才更稳

## 对知识库 agent 来说怎么做
如果我们要给这套知识库 agent 做 eval，我会建议先从最小闭环开始。

### 1. 先定义 3 类任务
- 摄入一篇来源并正确更新 wiki
- 回答一个问题并给出可追溯依据
- 对已有结构做整理但不破坏链接

### 2. 再定义 4 类 grader
- 链接是否完整
- 是否引用到正确来源
- 是否引入明显幻觉
- 是否符合页面风格约束

### 3. 最后读失败 transcript
特别关注这些失败：
- 明明有资料却找错页
- 总结写得像，但来源不对
- 结构整理时误删重要页
- 更新过度，破坏原有知识网络

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
- 它也与更广义的智能体系统（agent systems）相关，因为 agent 能力提升会直接改变什么样的评估还能保有区分度（agent progress changes what kinds of evaluations still work）。

## 对知识库场景的启发
- 以后如果你想评估“这个知识库 agent 是否真的有用”，不能只看它写得像不像（do not judge it only by whether the output sounds good）
- 更该看它是否更稳定、是否更少幻觉、是否更会找对资料、是否更会持续更新（look at stability, hallucination rate, retrieval quality, and maintenance quality）
- 也就是说，知识库 agent 的评估不应只看输出文本，而应看整个维护过程的质量（evaluate the maintenance process, not just the final prose）

## 相关来源
- [[wiki/sources/2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations|2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations]]
- [[wiki/sources/2026-04-22 Anthropic Engineering - Demystifying Evals for AI Agents|2026-04-22 Anthropic Engineering - Demystifying Evals for AI Agents]]

## 张力与开放问题
- 未来是否存在既真实、又公平、又抗AI的稳定评估？(Can a stable evaluation be realistic, fair, and AI-resistant at the same time?)
- 当 AI 已成为默认工作伙伴时，评估到底该测“人”，还是测“人+AI”？(When AI is the default collaborator, should we evaluate humans alone or human+AI systems?)
- 一个评估如果每隔几个月就要重做，长期成本是否可接受？(If an evaluation must be redesigned every few months, is that sustainable?)
- 对不同岗位和不同 agent 系统，AI评估是否应完全不同？(Should AI evaluation be entirely different across roles and agent types?)
