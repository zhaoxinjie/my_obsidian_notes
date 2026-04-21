---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - mcp
  - tool
  - discovery
---

# 2026-04-21 Anthropic Engineering - Introducing Advanced Tool Use
## 来源信息
- 原始路径: `raw/assets/advanced-tool-use.pdf`
- 标题: Introducing advanced tool use on the Claude Developer Platform
- 作者机构: Anthropic Engineering
- 发布日期: 2025-11-24
- 原文链接: https://www.anthropic.com/engineering/advanced-tool-use

## 摘要
这篇文章介绍了 Claude Developer Platform 上与高级工具使用（advanced tool use）相关的几项新能力，核心方向是让 agent 在面对大规模工具库时，不再一次性把全部定义塞进上下文，而是逐步实现工具发现、按需加载和动态执行。

## 关键要点
- 大规模工具使用需要动态发现（discovery）和按需加载（deferred loading）。
- 工具调用正在从简单函数调用走向更智能的编排（orchestration）。
- MCP 让工具生态更容易扩展，但也让发现和执行策略变得更重要。

## 重要概念
- [[wiki/concepts/MCP|MCP（Model Context Protocol）]]
- [[wiki/concepts/工具|工具（tool）]]

## 对知识库的影响
- 让知识库未来如果接很多外部工具时，有了更清晰的进阶方向。
- 说明“接很多工具”不是终点，“怎么用好很多工具”才是后续难点。
