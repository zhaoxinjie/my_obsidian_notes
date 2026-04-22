---
type: overview
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - log
---

# Wiki Log
## [2026-04-21] setup | 初始化个人知识库
- 基于 Karpathy 的 `LLM Wiki` 思路完成初始搭建
- 建立 `raw/`、`wiki/`、`system/` 三层结构
- 新增 `AGENTS.md` 作为 agent 维护协议
- 新增入口页、索引页、总览页、模板与使用手册

## [2026-04-21] ingest | Karpathy - LLM Wiki
- 将 Karpathy 的 `LLM Wiki` gist 作为首条来源页摄入
- 新建概念页：`LLM Wiki`、`个人知识库`
- 新建实体页：`Andrej Karpathy`
- 更新 `wiki/index.md` 以反映首批正式知识页面

## [2026-04-21] discuss+ingest | Anthropic - Building Effective Agents
- 先讨论再落库，将该文定位为“方法论概念页”而非普通摘要
- 新建概念页：`构建高效智能体（Building Effective Agents）`
- 新建来源页：`Anthropic - Building Effective Agents`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Effective Harnesses for Long-Running Agents
- 先讨论概念定位，再落库
- 将该文沉淀为概念页：`harness工程`
- 新建来源页：`Anthropic Engineering - Effective Harnesses for Long-Running Agents`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Harness Design for Long-Running Application Development
- 先讨论定位，再决定不单独建新概念页
- 将其核心观点综合进 `harness工程`
- 新建来源页：`Anthropic Engineering - Harness Design for Long-Running Application Development`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Effective Context Engineering for AI Agents
- 先讨论概念定位，再落库
- 新建概念页：`上下文工程（context engineering）`
- 新建来源页：`Anthropic Engineering - Effective Context Engineering for AI Agents`
- 更新 `harness工程` 与 `构建高效智能体` 的关联
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Writing Effective Tools for Agents
- 先讨论概念定位，再落库
- 新建概念页：`工具（tool）`
- 新建来源页：`Anthropic Engineering - Writing Effective Tools for Agents`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Designing AI-Resistant Technical Evaluations
- 先讨论概念定位，再落库
- 新建概念页：`AI评估`
- 新建来源页：`Anthropic Engineering - Designing AI-Resistant Technical Evaluations`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | Introducing Contextual Retrieval
- 先讨论定位，再决定不单独建一级概念页
- 将其核心观点综合进 `上下文工程`
- 新建来源页：`Anthropic Research - Introducing Contextual Retrieval`
- 更新 `wiki/index.md`

## [2026-04-21] discuss+ingest | MCP related articles
- 基于后续几篇文章补建概念页：`MCP（Model Context Protocol）`
- 新建来源页：`Anthropic Engineering - Code Execution with MCP`
- 新建来源页：`Anthropic Engineering - Introducing Advanced Tool Use`
- 更新 `wiki/index.md`

## [2026-04-21] synthesis | agent engineering map
- 新建综合页：`agent 工程地图（agent engineering map）`
- 将当前 agent 相关内容整理为 6 层结构
- 更新 `wiki/index.md`

## [2026-04-21] lint | 首次知识库巡检
- 对 `wiki/` 执行首次结构与风格巡检
- 修复早期页面残留的英文小节标题与字段标签
- 在 `wiki/index.md` 增加目录说明入口，强化目录型 README 的可发现性
- 检查结果：当前未发现明显重复概念页或断裂主线
- 备注：若干 `README.md` 在脚本统计中显示为孤立页，主要因为同名文件导致的统计假阳性，不是实际断链

## [2026-04-22] seed | 张一鸣人物研究页
- 新建实体页：`张一鸣`
- 先建立人物研究骨架，不急着写满结论
- 作为后续人物研究支线的起点
