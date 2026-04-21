---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - evaluation
  - ai
---

# 2026-04-21 Anthropic Engineering - Designing AI-Resistant Technical Evaluations
## 来源信息
- 原始路径: `raw/assets/ai-resistant-technical-evaluations.pdf`
- 标题: Designing AI-resistant technical evaluations
- 作者: Tristan Hume
- 作者机构: Anthropic Engineering
- 发布日期: 2026-01-21
- 原文链接: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations

## 摘要
这篇文章讨论的核心不是如何设计更难的技术题，而是如何在 AI 能力持续增强的背景下，设计仍然有区分度的技术评估。文章展示了一个真实 take-home 测试如何被更强的 Claude 模型持续击穿，以及评估设计如何被迫在真实性、公平性、时间成本与抗AI性之间反复权衡。

## 关键要点
- 技术评估会随着模型能力增强而失效。
- 越贴近真实工作的任务，不一定越能抗AI。
- 时间限制会显著影响人类与模型的相对优势。
- 评估设计正在从静态题目设计变成持续迭代的系统工程。
- 在 AI 时代，评估需要重新定义“什么叫有信号”。

## 重要概念
- [[wiki/concepts/AI评估|AI评估]]

## 对知识库的影响
- 为知识库补上了“如何验证系统是否真的有效”的外部视角。
- 让现有的 agent 工程主线之外，多出一条评估主线。

## 开放问题
- 如果未来也要评估知识库 agent，什么指标最能体现真实价值？
- 对人类和对 agent，是否应该使用完全不同的评估框架？
