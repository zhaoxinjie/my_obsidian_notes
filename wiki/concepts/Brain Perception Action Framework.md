---
type: concept
status: active
created: 2026-04-21
updated: 2026-04-21
source_count: 1
tags:
  - concept
  - framework
  - agent
---

# 脑-感知-行动框架（Brain-Perception-Action）

## 定义

这是该综述中用于概括 LLM-based agents 的通用框架：

- `brain`: 语言理解、知识、记忆、推理、规划
- `perception`: 多模态输入与环境感知
- `action`: 工具使用、外部执行与具身行为

## 为什么重要

它提供了一个很实用的分析框架。后续你看 agent 论文、产品或系统设计时，都可以用这三层去拆。

## 当前理解

- `brain` 是 agent 的认知中枢，通常由 LLM 驱动。
- `perception` 决定 agent 能看到什么、理解什么输入。
- `action` 决定 agent 能实际做什么，而不只是生成文本。
- 很多 agent 系统的瓶颈，往往不在 LLM 本身，而在 perception/action 接口和长期状态管理。

## 相关来源

- [[wiki/sources/2026-04-21 Xi et al. - The Rise and Potential of Large Language Model Based Agents A Survey|2026-04-21 Xi et al. - The Rise and Potential of Large Language Model Based Agents: A Survey]]

## 相关实体

- [[wiki/entities/Zhiheng Xi|Zhiheng Xi]]

## 张力与开放问题

- 哪些系统其实只有 `brain`，却被包装成 agent？
- 什么时候 tool use 应被视为 action，什么时候应被视为 brain 的扩展？
- 长期记忆应该归入 brain，还是视作独立系统层？
