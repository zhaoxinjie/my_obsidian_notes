---
type: source
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - source
  - claude-code
  - harness
  - workflow
---
# 2026-06-02 Claude - A Harness for Every Task Dynamic Workflows in Claude Code
## 来源
- 原文：[A harness for every task: dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
- 本地 PDF：[[raw/assets/claude_dynamic_workflows_article.pdf]]
- 作者：Thariq Shihipar、Sid Bidasaria
- 日期：2026-06-02
## 核心主张
Claude Code 的动态工作流（dynamic workflows）让模型可以按当前任务临时写一个 JavaScript harness，并用它生成、协调多个子代理（subagents）。这不是简单“多开几个 agent”，而是把任务的拆分、并行、验证、汇总和停止条件外化成一段可执行编排逻辑。
这篇文章把 harness 的含义从“长时运行的工程外壳”进一步推进到“按任务生成的临时执行结构（task-specific execution structure）”：不同任务可以拥有不同的子代理拓扑、模型选择、worktree 隔离和验证路径。
## 解决的失败模式
- 代理惰性（agentic laziness）：复杂任务做到一部分就提前宣布完成。
- 自我偏好偏差（self-preferential bias）：模型更容易相信自己刚产出的结果，尤其不擅长客观审查自己的方案。
- 目标漂移（goal drift）：长任务经过多轮上下文压缩后，原始目标、边界和禁止项逐渐丢失。
动态工作流的关键是用多个独立上下文窗口分担认知负担：执行者专心做，验证者专心挑错，汇总者专心合并，外层 JavaScript loop 负责保持结构和停止条件。
## 常见编排模式
- 分类后执行（classify-and-act）：先判断任务类型，再路由到不同处理路径。
- 扇出后综合（fan-out-and-synthesize）：把任务拆成许多小块并行处理，再统一合并。
- 对抗式验证（adversarial verification）：每个产出都由独立代理按 rubric 审查。
- 生成后过滤（generate-and-filter）：先生成多个候选，再按标准去重、筛选和保留高质量结果。
- 锦标赛（tournament）：多个代理用不同策略解决同一问题，再通过成对比较选胜者。
- 循环直到完成（loop-until-done）：当工作量未知时，不预设固定轮数，而是运行到没有新发现、没有错误或满足停止条件。
## 适用场景
- 迁移与重构（migrations and refactors）：按 callsite、模块、失败测试拆分，子代理在隔离 worktree 中修复，再由审查代理验证。
- 深度研究（deep research）：并行搜索、抓取来源、验证论断并综合带引用报告。
- 深度验证（deep verification）：抽取报告中的事实声明，逐条查证，再审查证据质量。
- 大规模排序（sorting at scale）：用成对比较、分桶排序或锦标赛替代一次性绝对评分。
- 规则遵守与记忆（memory and rule adherence）：把规则拆给多个 verifier，或从历史会话中挖掘反复纠正的问题并沉淀为规则。
- 根因调查（root-cause investigation）：让不同代理基于日志、代码、数据等不同证据生成假设，再由反驳者验证。
- 大规模分诊（triaging at scale）：分类、去重、行动或升级，并用隔离策略处理不可信输入。
- 探索与品味判断（exploration and taste）：设计、命名、方案探索等主观任务可用 rubric 和 tournament 降低随意性。
- 轻量评估（lightweight evals）：为某类任务启动多个隔离 trial，再用比较代理和 rubric 评分。
## 对知识库的影响
这篇应该综合进 [[wiki/concepts/harness工程|harness工程]]，因为它明确说明：harness 不必总是静态系统，也可以是按任务动态生成的临时编排器。它还强化了 [[wiki/concepts/AI评估|AI评估]] 的一个实践方向：复杂任务的 eval 可以直接复用多代理 workflow，把 trial、grader、transcript 和隔离环境组织起来。
## 我的判断
动态工作流的价值不在“并行”本身，而在“结构性防错”：它用拓扑结构约束模型行为，让模型更难偷懒、更难自嗨、更难在长链路里忘掉目标。但它也不是默认方案，因为它会显著增加 token、延迟和编排复杂度。判断是否使用 workflow 的实用标准是：这个任务是否真的需要更多独立上下文、更强验证或更多并行 compute。
## 相关页面
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/syntheses/agent 工程地图|agent 工程地图]]
