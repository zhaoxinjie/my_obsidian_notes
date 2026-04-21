---
type: overview
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - index
---

# Wiki Index
这是知识库的内容目录。回答问题前，优先从这里开始定位页面。

## 总览
- [[wiki/overview|知识库总览]] - 这套 wiki 的目标、结构与当前状态

## 运行与维护
- [[wiki/log|知识库日志]] - 摄入、问答和维护记录

## 来源页
- [[wiki/sources/2026-04-21 Karpathy - LLM Wiki|2026-04-21 Karpathy - LLM Wiki]] - Karpathy 提出的 LLM 维护型 wiki 方法论来源页
- [[wiki/sources/2026-04-21 Xi et al. - The Rise and Potential of Large Language Model Based Agents A Survey|2026-04-21 Xi et al. - The Rise and Potential of Large Language Model Based Agents A Survey]] - LLM-based agents 的综述论文，提供领域框架、应用全景与开放问题
- [[wiki/sources/2026-04-21 Anthropic - Building Effective Agents|2026-04-21 Anthropic - Building Effective Agents]] - 关于何时使用工作流或智能体，以及如何用最小复杂度构建有效 agent 的实践文章
- [[wiki/sources/2026-04-21 Anthropic Engineering - Effective Harnesses for Long-Running Agents|2026-04-21 Anthropic Engineering - Effective Harnesses for Long-Running Agents]] - 关于长时运行智能体如何通过工程外壳保持连续性、增量推进与干净交接的文章
- [[wiki/sources/2026-04-21 Anthropic Engineering - Harness Design for Long-Running Application Development|2026-04-21 Anthropic Engineering - Harness Design for Long-Running Application Development]] - 关于生成与评估分离、三角色 harness 和阶段合同的工程文章
- [[wiki/sources/2026-04-21 Anthropic Engineering - Effective Context Engineering for AI Agents|2026-04-21 Anthropic Engineering - Effective Context Engineering for AI Agents]] - 关于上下文作为有限注意力预算，以及压缩、即时加载、外部记忆和子代理等策略的文章
- [[wiki/sources/2026-04-21 Anthropic Engineering - Writing Effective Tools for Agents|2026-04-21 Anthropic Engineering - Writing Effective Tools for Agents]] - 关于如何把工具设计成适合 agent 使用的行动契约，以及如何用评测持续优化工具
- [[wiki/sources/2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations|2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations]] - 关于 AI 时代如何设计仍然有区分度、又兼顾公平与真实性的技术评估
- [[wiki/sources/2026-04-21 Anthropic Research - Introducing Contextual Retrieval|2026-04-21 Anthropic Research - Introducing Contextual Retrieval]] - 关于在检索前给 chunk 补局部语境，以提升 RAG 检索质量的方法
- [[wiki/sources/2026-04-21 Anthropic Engineering - Code Execution with MCP|2026-04-21 Anthropic Engineering - Code Execution with MCP]] - 关于 MCP 工具规模扩大后，如何用代码执行减少直接 tool calling 的上下文与 token 开销
- [[wiki/sources/2026-04-21 Anthropic Engineering - Introducing Advanced Tool Use|2026-04-21 Anthropic Engineering - Introducing Advanced Tool Use]] - 关于在大规模工具库中实现动态发现、按需加载与高级工具编排的文章

## 概念页
- [[wiki/concepts/LLM Wiki|LLM Wiki]] - 用 LLM 持续维护、而非每次临时检索的知识库模式
- [[wiki/concepts/个人知识库|个人知识库]] - 面向个人成长、项目与长期主题研究的知识组织方式
- [[wiki/concepts/LLM-based Agents|大语言模型智能体（LLM-based Agents）]] - 以大语言模型为核心构建智能体的研究主题
- [[wiki/concepts/Brain Perception Action Framework|脑-感知-行动框架（Brain-Perception-Action）]] - 论文提出的 LLM agent 通用结构框架
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]] - 强调最小必要复杂度、工具设计和环境反馈的智能体方法论
- [[wiki/concepts/harness工程|harness工程]] - 为长时运行智能体搭建可持续交接、可验证推进的工程外壳
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]] - 管理模型每轮工作记忆与信息流的底层工程方法
- [[wiki/concepts/工具|工具（tool）]] - 连接 agent 与外部世界的行动契约，以及面向 agent 的工具设计原则
- [[wiki/concepts/AI评估|AI评估]] - 在 AI 时代设计仍有区分度、可代表真实能力的评估方法
- [[wiki/concepts/MCP|MCP（Model Context Protocol）]] - 让 agent 与大量外部工具和资源建立标准化连接的协议层

## 实体页
- [[wiki/entities/Andrej Karpathy|Andrej Karpathy]] - 提出该模式的研究者与工程师
- [[wiki/entities/Zhiheng Xi|Zhiheng Xi]] - LLM-based agents survey 的主要作者之一

## 问题页
- 暂无问题归档

## 综合页
- [[wiki/syntheses/agent 工程地图|agent 工程地图（agent engineering map）]] - 把当前知识库里的 agent 相关文章整理成 6 层结构地图
