---
type: source
status: active
created: 2026-04-22
updated: 2026-04-22
tags:
  - source
  - evaluation
  - agent
  - harness
---

# 2026-04-22 Anthropic Engineering - Demystifying Evals for AI Agents
## 来源信息
- 原始路径: `raw/assets/demystifying-evals-for-ai-agents.pdf`
- 标题: Demystifying evals for AI agents
- 作者机构: Anthropic Engineering
- 发布日期: 2026-01-09
- 原文链接: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## 摘要
这篇文章把 agent eval 从“为什么重要”推进到“如何搭建”。它系统解释了 task、trial、grader、transcript 这些基本结构，区分了 capability evals 与 regression evals，并强调 eval harness、grader 设计、任务维护，以及把自动化 eval 与生产监控、A/B test、人工 review 结合起来的重要性。

## 关键要点
- agent eval 比单轮 eval 更复杂，因为 agent 会跨多轮调用工具、修改环境并累积错误。
- 一个完整 eval 不只是题目，还包括 task、trial、grader、transcript 等结构。
- capability evals 和 regression evals 解决的是不同问题，不能混用。
- eval harness 必须稳定、隔离、接近生产，否则结果会被基础设施噪音污染。
- 自动化 eval 很重要，但必须和其他生产信号结合，才能形成完整判断。

## 重要概念
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/harness工程|harness工程]]

## 对知识库的影响
- 让 `AI评估` 从问题意识扩展成更可操作的方法论。
- 为知识库 agent 未来搭建 capability / regression eval 提供了更清晰的起点。
