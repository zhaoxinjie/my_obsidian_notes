---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - agent
  - context
  - engineering
---

# 2026-04-21 Anthropic Engineering - Effective Context Engineering for AI Agents
## 来源信息
- 原始路径: `raw/assets/effective-context-engineering-for-ai-agents.pdf`
- 标题: Effective context engineering for AI agents
- 作者机构: Anthropic Applied AI team
- 发布日期: 2025-09-29
- 原文链接: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## 摘要
这篇文章提出，随着多轮 agent 系统越来越常见，工程重点正在从“怎么写好 prompt”转向“怎么管理整套上下文状态”。文章把上下文视作有限注意力预算，并系统讨论了压缩、笔记、即时上下文与子代理架构等方法，说明为什么上下文工程会成为构建有效 agent 的底层能力。

## 关键要点
- 上下文工程是提示词工程的自然升级。
- 上下文窗口是有限资源，会随着内容增长出现质量衰减。
- 高质量 agent 依赖按需取用信息，而不是预加载所有信息。
- 长任务中的关键技术包括压缩、外部记忆和子代理架构。
- 信息组织方式本身会影响 agent 的推理质量和行为稳定性。

## 重要概念
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]

## 对知识库的影响
- 为知识库补上了一个更底层的 agent 工程概念：如何管理模型每轮看到的信息。
- 让现有的 `harness工程` 与 `构建高效智能体` 有了更清晰的上游基础。

## 开放问题
- 在你的知识库里，哪些内容应该常驻上下文，哪些内容应该按需获取？
- 如果以后来源越来越多，是否需要更明确的目录、标签和索引规范？
