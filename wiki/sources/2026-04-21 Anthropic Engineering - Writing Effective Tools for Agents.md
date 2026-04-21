---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - agent
  - tool
  - engineering
---

# 2026-04-21 Anthropic Engineering - Writing Effective Tools for Agents
## 来源信息
- 原始路径: `raw/inbox/writing-tools-for-agents.pdf`
- 标题: Writing effective tools for agents
- 作者机构: Anthropic Engineering
- 发布日期: 2025-09-11
- 原文链接: https://www.anthropic.com/engineering/writing-tools-for-agents

## 摘要
这篇文章讨论的核心不是 agent 会不会调用工具，而是工具是否被设计成适合 agent 使用。文章指出，工具是一种连接确定性系统与非确定性 agent 的新型契约，好的工具需要围绕高价值工作流、上下文效率、清晰命名、可行动报错与 evaluation 驱动迭代来设计。

## 关键要点
- 工具不等于普通 API 封装，它要为 agent 的理解方式而设计。
- 多工具并不天然更好，关键是边界清晰与工作流贴合度。
- 工具返回值应优先返回高信号信息，而不是低层技术细节。
- 工具名、参数说明和错误提示会直接影响 agent 的行为。
- 工具质量需要通过真实任务评测持续改进。

## 重要概念
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]

## 对知识库的影响
- 为知识库补上了一个关键工程层：如何把外部能力设计成适合 agent 使用的工具。
- 让现有的 `上下文工程` 与 `构建高效智能体` 有了更具体的执行接口层。

## 开放问题
- 对你的知识库 agent 来说，最值得优先设计的三个工具是什么？
- 如果未来工具越来越多，是否需要更明确的命名空间与评测机制？
