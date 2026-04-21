---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - agent
  - methodology
---

# 2026-04-21 Anthropic - Building Effective Agents
## 来源信息
- 原始路径: `raw/inbox/building-effective-agents.pdf`
- 标题: Building effective agents
- 作者机构: Anthropic
- 日期: 2024-12-19
- 原文链接: https://www.anthropic.com/research/building-effective-agents

## 摘要
这篇文章强调，成功的智能体系统往往不是靠复杂框架堆出来的，而是靠简单、可组合、可调试的模式逐步搭建出来的。它明确区分了工作流与智能体，并给出何时该使用哪一种的实践建议。

## 关键要点
- 优先寻找最简单可行方案，而不是默认上 agent。
- 固定路径任务更适合工作流，开放式任务更适合智能体。
- 智能体本质上通常是“模型 + 工具 + 环境反馈”的循环。
- 工具接口设计、透明性与测试，比框架炫酷程度更重要。
- 复杂度会带来成本、延迟与错误累积，因此必须设置边界与护栏。

## 重要概念
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]
- [[wiki/concepts/LLM-based Agents|大语言模型智能体（LLM-based Agents）]]

## 对知识库的影响
- 为 agent 主题补上了一张偏工程实践的方法论页面。
- 让知识库里关于 agent 的内容，从“是什么”扩展到“怎么设计更有效”。

## 开放问题
- 这套原则在你的实际任务里，最先适合应用在哪类场景？
- 你现在接触的 agent 系统，问题更像是模型能力问题，还是工程复杂度问题？
