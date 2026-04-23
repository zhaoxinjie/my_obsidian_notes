---
type: source
status: active
created: 2026-04-22
updated: 2026-04-22
tags:
  - source
  - tool
  - thinking
  - agent
---

# 2026-04-22 Anthropic Engineering - The Think Tool
## 来源信息
- 原始路径: `raw/assets/claude-think-tool.pdf`
- 标题: The "think" tool: Enabling Claude to stop and think in complex tool use situations
- 作者机构: Anthropic Engineering
- 发布日期: 2025-03-20
- 原文链接: https://www.anthropic.com/engineering/claude-think-tool

## 摘要
这篇文章讨论一种特殊工具：`think tool`。它不会获取新信息，也不会改变外部环境，而是给模型一个显式的中间思考步骤，用来在复杂工具链里分析工具输出、检查规则约束、确认信息是否完整，再决定下一步动作。

## 关键要点
- `think tool` 的核心价值是增加显式暂停点，而不是增加外部能力。
- 它特别适合工具输出复杂、规则重、决策串行累积的场景。
- 单独加 `think tool` 有时有效，但在复杂领域里，通常需要配合明确提示词和示例。
- 它不是通用增益项，简单任务或低约束场景往往收益有限。
- Anthropic 后续也指出，很多场景下更推荐使用 `extended thinking`。

## 重要概念
- [[wiki/concepts/工具|工具（tool）]]

## 对知识库的影响
- 为 `工具` 这条主线补上了一类特殊工具：不是执行动作，而是显式帮助模型整理判断。
- 让知识库中的工具概念，从“行动接口”扩展到“思考接口”。
