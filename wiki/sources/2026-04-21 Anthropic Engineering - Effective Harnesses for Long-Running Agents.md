---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - agent
  - harness
  - engineering
---

# 2026-04-21 Anthropic Engineering - Effective Harnesses for Long-Running Agents
## 来源信息
- 原始路径: `raw/assets/effective-harnesses-for-long-running-agents.pdf`
- 标题: Effective harnesses for long-running agents
- 作者机构: Anthropic Engineering
- 发布日期: 2025-11-26
- 原文链接: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

## 摘要
这篇文章讨论的核心不是如何让智能体在单轮里更强，而是如何让它在多个上下文窗口之间持续、稳定地推进复杂任务。文章提出，长时运行智能体需要一套工程化 harness，把初始化、进度记录、目标清单、环境验证和干净交接显式做出来。

## 关键要点
- 长时运行智能体的核心问题是跨 session 失去连续性。
- 仅靠上下文压缩不足以解决连续协作问题。
- 初始化代理负责搭建环境，后续代理负责逐轮增量推进。
- 每轮应只推进一个特性，并留下清晰交接信息。
- 智能体应通过真实环境验证进展，而不是过早宣布完成。

## 重要概念
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]

## 对知识库的影响
- 为 agent 方法论补上了“长时运行工程外壳”这一层。
- 让知识库中关于 agent 的讨论，从“如何设计能力”延伸到“如何保证跨轮次稳定推进”。

## 开放问题
- 这套 harness 思路如何迁移到非编码任务？
- 哪些外部工件最能有效降低交接成本？
