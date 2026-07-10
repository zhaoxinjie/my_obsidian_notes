---
type: synthesis
status: active
created: 2026-04-21
updated: 2026-07-09
source_count: 14
tags:
  - synthesis
  - agent
  - engineering
---

# agent 工程地图（agent engineering map）
## 这页在做什么
这页不是单篇文章摘要，而是把当前知识库里与 agent 相关的主要概念组织成一张结构地图（conceptual map）。

它回答的核心问题是：
- 构建 agent 系统时，关键问题大致分成哪几层？
- 新读到一篇文章时，应该把它挂到哪一层？
- 这些层之间是什么关系？

## 一张简化地图
可以先把当前结构粗略理解成 9 层：

1. 方法论层（methodology）
2. 信息流层（context and retrieval）
3. 行动接口层（tools）
4. 协议与生态层（protocol and ecosystem）
5. 长时运行层（long-running execution）
6. 评估层（evaluation）
7. 安全与演化层（safety and evolution）
8. 自我改进与优化层（self-improvement and optimization）
9. 推理计算层（reasoning and test-time compute）

## 1. 方法论层（methodology）
这一层讨论：什么时候该使用 agent，复杂度应该如何控制，系统设计应优先追求什么。

对应页面：
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]

这一层更像总原则：
- 是否真的需要 agent
- 什么时候 workflow 就足够
- 为什么要从简单方案开始
- 早期 agent 基础结构：planning、memory、tool use

如果一篇文章主要在讨论“该不该这样设计系统”，通常属于这一层。

## 2. 信息流层（context and retrieval）
这一层讨论：模型每一轮应该看到什么信息，这些信息如何被选择、压缩、加载和检索。

对应页面：
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]

这一层的核心问题包括：
- 什么信息应该进入上下文
- 什么信息应该延迟加载（just-in-time context）
- 如何压缩历史
- 如何通过 contextual retrieval 提高检索质量
- 长期记忆如何在 recency、importance、relevance 之间权衡

如果一篇文章主要在讨论“信息怎么进入模型工作记忆”，通常属于这一层。

## 3. 行动接口层（tools）
这一层讨论：agent 如何通过工具与外部世界互动，以及工具应该怎么被设计成适合 agent 使用。

对应页面：
- [[wiki/concepts/工具|工具（tool）]]

这一层的核心问题包括：
- 工具该不该实现
- 工具边界如何划分
- 返回值该怎么设计
- 参数名、描述、错误信息如何帮助 agent 正确使用工具
- agent 是只能调用给定工具，还是能检索、学习和组合多个工具

如果一篇文章主要在讨论“agent 怎么做事、工具怎么设计”，通常属于这一层。

## 4. 协议与生态层（protocol and ecosystem）
这一层讨论：当工具规模上升之后，agent 如何通过协议接入更大的工具生态，并进一步解决发现、加载和执行问题。

对应页面：
- [[wiki/concepts/MCP|MCP（Model Context Protocol）]]

这一层的核心问题包括：
- 工具如何标准化接入
- agent 如何规模化连接外部系统
- 工具太多之后，如何发现、按需加载、动态执行

如果一篇文章主要在讨论“MCP、协议、生态扩展、大规模工具接入”，通常属于这一层。

## 5. 长时运行层（long-running execution）
这一层讨论：当任务跨多个上下文窗口、多个阶段、多个 session 时，系统如何持续推进、交接、纠偏和验收。

对应页面：
- [[wiki/concepts/harness工程|harness工程]]

这一层的核心问题包括：
- 如何记录进度
- 如何保持连续性
- 如何把生成与评估分离
- 如何让系统在长任务中持续纠偏
- 如何为复杂任务动态生成子代理拓扑、验证路径和停止条件

如果一篇文章主要在讨论“长时运行”“多阶段推进”“交接与验收”，通常属于这一层。

新的补充是：动态工作流（dynamic workflows）说明 harness 不一定是固定流程，也可以是按任务临时生成的编排结构。它把工具、子代理、模型选择、worktree 隔离和评估者组织成一个任务专属执行系统。

## 6. 评估层（evaluation）
这一层讨论：如何判断一个 agent 系统、人机协作流程、或 AI 时代的人类能力是否真的有价值且仍有区分度。

对应页面：
- [[wiki/concepts/AI评估|AI评估]]

这一层的核心问题包括：
- 什么叫有效评估
- 评估是否还有信号（signal）
- 评估测到的是人、模型，还是人+AI
- 如何在真实性、公平性、抗AI性之间做权衡

如果一篇文章主要在讨论“怎么验证能力和系统是否真的好”，通常属于这一层。

## 7. 安全与演化层（safety and evolution）
这一层讨论：当 agent 会长期运行、积累记忆、创建工具、优化 workflow，甚至更新模型时，系统如何避免在自我改进中变坏。

对应页面：
- [[wiki/concepts/自演化智能体风险|自演化智能体风险（Misevolution）]]

这一层的核心问题包括：
- agent 自修改之后是否仍然安全
- 记忆、工具、workflow 的演化是否引入新风险
- 如何给自演化系统做版本化、审计、回滚和持续安全评估
- 如何避免能力优化把安全边界优化掉

如果一篇文章主要在讨论“self-evolving agents”“agent safety”“memory/tool/workflow evolution risk”，通常属于这一层。

## 8. 自我改进与优化层（self-improvement and optimization）
这一层讨论：当 agent 不只是执行任务，而是开始优化自己的上下文、workflow、harness code，甚至 optimizer code 时，系统应该如何组织搜索空间、评估候选和治理合并。

对应页面：
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/自演化智能体风险|自演化智能体风险（Misevolution）]]

这一层的核心问题包括：
- prompt、context、workflow、harness code 哪些可以被优化
- 如何从失败 trace 中挖掘可修复的 weakness
- 如何用 held-in / held-out 验证候选改动
- 权限、安全、审计和评估层如何保持在自修改 loop 外
- 文件系统如何作为持久工作区，而不是变成无治理的长期记忆垃圾堆

如果一篇文章主要在讨论“harness optimization”“Self-Harness”“Meta-Harness”“workflow search”“recursive self-improvement”，通常属于这一层。

## 9. 推理计算层（reasoning and test-time compute）
这一层讨论：模型或 agent 在推理时如何分配额外计算，什么时候多想、什么时候并行采样、什么时候顺序修订、什么时候调用工具验证。

对应页面：
- [[wiki/concepts/测试时计算|测试时计算（test-time compute）]]
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/AI评估|AI评估]]

这一层的核心问题包括：
- CoT 为什么能提升能力
- thinking budget 如何按任务难度分配
- parallel sampling 与 sequential revision 如何取舍
- CoT 是否忠实，如何避免把 CoT 当真相
- loop 如何成为 agent 外部的 test-time compute

如果一篇文章主要在讨论“reasoning model”“CoT”“test-time compute”“thinking tokens”“self-correction”，通常属于这一层。

## 层与层之间的关系
这些层不是并列孤岛，它们更像从内到外逐渐展开：

- 方法论层决定系统设计的总方向
- 信息流层决定模型每轮“看到什么”
- 行动接口层决定模型“能做什么”
- 协议与生态层决定系统“能接多大世界”
- 长时运行层决定系统“能持续工作多久、如何稳定推进”
- 评估层决定我们“怎么知道它是否真的有效”
- 安全与演化层决定系统“变强之后是否仍然可信”
- 自我改进与优化层决定系统“如何在受控边界内变强”
- 推理计算层决定系统“回答前应该怎样花计算”

可以把它压缩成一句话：
- 方法论决定方向，信息流决定认知，工具决定动作，协议决定规模，harness 决定持续性，评估决定真假
- 进一步说，动态 harness 决定复杂任务应该如何分身、并行、验证和停止
- 自演化安全决定系统是否能在持续变化中不越界
- 自我改进优化决定系统能否把失败转化为受控候选改动，而不是自由漂移
- 推理计算决定模型和 agent 是一次性拍答案，还是通过搜索、验证和修正逐步靠近答案

## 如何使用这张地图
以后每当你摄入一篇新文章，可以先问 3 个问题：

### 1. 这篇文章主要在解决哪一层的问题？
- 是设计原则问题
- 信息流问题
- 工具问题
- 协议问题
- 长任务问题
- 评估问题

### 2. 它是在开新主线，还是在加深已有主线？
- 如果只是把已有层讲深，优先综合进现有概念页
- 如果它提出了一条新的一级问题域，再考虑新建概念页

### 3. 它最值得沉淀的是“资料内容”，还是“我们的判断”？
- 资料内容适合进来源页
- 我们讨论出来的稳定结论，应该进入概念页或综合页

## 当前知识库的一个特点
当前这套 agent 相关内容，已经明显从“收集文章”过渡到了“形成结构”。

这意味着后续更重要的事情，不是继续平铺更多文章，而是：
- 让每篇新文章进入已有结构
- 发现结构里还缺哪一层
- 把跨文章的判断逐渐沉淀为稳定页面

## 后续可能会继续长出来的层
当前地图已经有 9 层，但未来很可能还会补出更多层，例如：
- 安全与权限（security and permissions）
- 多代理协作（multi-agent collaboration）
- 记忆（memory）
- 可观察性（observability）
- 经济性与成本控制（cost and latency economics）

如果后续某类文章开始反复出现，就值得考虑把它升格成新的一级概念页。

## 相关页面
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/concepts/MCP|MCP（Model Context Protocol）]]
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/自演化智能体风险|自演化智能体风险（Misevolution）]]
- [[wiki/concepts/测试时计算|测试时计算（test-time compute）]]
