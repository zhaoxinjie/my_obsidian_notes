---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - pkm
  - llm
---

# 2026-04-21 Karpathy - LLM Wiki

## Source

- Raw source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Author: [[wiki/entities/Andrej Karpathy|Andrej Karpathy]]
- Date: 2026-04-04
- Format: Gist / Markdown note

## Summary

这篇文章提出了一种和传统 RAG 不同的知识管理方式：让 LLM 不只是“查询资料”，而是持续维护一套结构化、可累积、可交叉引用的 wiki。

## Key Points

- 知识库应该分为三层：原始资料层、wiki 编译层、agent 维护规则层。
- 新资料进入后，LLM 不应只做一次性总结，而应更新已有知识结构。
- 好问题的回答本身也是资产，应该沉淀回 wiki，而不是留在聊天记录里。
- `index.md` 负责内容导航，`log.md` 负责时间线记录。
- Obsidian 适合作为浏览与编辑界面，LLM 适合作为维护者。

## Important Entities

- [[wiki/entities/Andrej Karpathy|Andrej Karpathy]]

## Important Concepts

- [[wiki/concepts/LLM Wiki|LLM Wiki]]
- [[wiki/concepts/个人知识库|个人知识库]]

## What Changed In The Wiki

- 建立了这套个人知识库的三层结构。
- 明确了 `raw/`、`wiki/`、`AGENTS.md` 的职责分工。
- 为后续摄入、问答沉淀、lint 维护定义了固定流程。

## Open Questions

- 你的知识库未来会以哪些主题为主轴展开？
- 是否需要把“个人复盘/目标管理”单独发展成一套固定页面结构？
- 当来源数量增长到几十上百篇时，是否要引入更强的本地搜索工具？
