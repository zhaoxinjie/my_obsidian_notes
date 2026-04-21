---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - retrieval
  - context
  - rag
---

# 2026-04-21 Anthropic Research - Introducing Contextual Retrieval
## 来源信息
- 原始路径: `raw/assets/contextual-retrieval.pdf`
- 标题: Introducing Contextual Retrieval
- 作者机构: Anthropic Research
- 发布日期: 2024-09-19
- 原文链接: https://www.anthropic.com/research/contextual-retrieval

## 摘要
这篇文章讨论如何改进传统 RAG 的检索阶段。它提出，很多检索失败并不是因为完全找不到相关内容，而是因为被切出来的 chunk 脱离了原始文档语境。为了解决这个问题，文章提出在 embedding 和 BM25 建索引前，先给每个 chunk 补一段简短的局部语境说明，从而提升检索准确率。

## 关键要点
- 传统 chunking 会让片段丢失文档语境。
- 给 chunk 预先补上下文，可以显著改善检索效果。
- contextual embeddings 与 contextual BM25 可以叠加收益。
- reranking 能进一步提升最终召回质量。
- 检索增强不只是运行时问题，也可以在预处理阶段解决。

## 重要概念
- [[wiki/concepts/上下文工程|上下文工程（context engineering）]]

## 对知识库的影响
- 为 `上下文工程` 补上了一个非常具体的方法层：检索前的上下文化。
- 说明知识库结构、标题和来源组织，本身就会影响后续检索质量。

## 开放问题
- 在个人知识库里，哪些粒度适合做 contextual chunking？
- 对 Obsidian 这样的页面型知识库，页面级上下文和段落级上下文应该如何结合？
