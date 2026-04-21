---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - mcp
  - tool
  - execution
---

# 2026-04-21 Anthropic Engineering - Code Execution with MCP
## 来源信息
- 原始路径: `raw/assets/code-execution-with-mcp.pdf`
- 标题: Code execution with MCP: Building more efficient AI agents
- 作者机构: Anthropic Engineering
- 发布日期: 2025-11-04
- 原文链接: https://www.anthropic.com/engineering/code-execution-with-mcp

## 摘要
这篇文章讨论当 MCP 工具规模变大之后，直接 tool calling 会如何带来上下文和 token 开销问题。文章提出，更高效的方式是让 agent 通过代码执行（code execution）来调用和编排 MCP 工具，从而减少工具定义和中间结果对上下文窗口的占用。

## 关键要点
- MCP 让 agent 能接入大量工具，但也会带来上下文负担。
- 工具定义和工具结果都可能成为 token 黑洞（token sink）。
- 用代码执行来编排工具调用，比逐次直接调用更高效。
- 这是把一部分 agent 推理从自然语言上下文搬回程序执行层。

## 重要概念
- [[wiki/concepts/MCP|MCP（Model Context Protocol）]]
- [[wiki/concepts/工具|工具（tool）]]

## 对知识库的影响
- 为知识库补上了 MCP 相关的执行层视角。
- 说明一旦未来工具规模扩大，执行方式本身会成为系统效率关键。
