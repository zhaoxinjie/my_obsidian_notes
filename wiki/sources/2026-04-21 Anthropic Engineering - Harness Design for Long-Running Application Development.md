---
type: source
status: active
created: 2026-04-21
updated: 2026-04-21
tags:
  - source
  - agent
  - harness
  - evaluation
  - engineering
---

# 2026-04-21 Anthropic Engineering - Harness Design for Long-Running Application Development
## 来源信息
- 原始路径: `raw/inbox/harness-design-long-running-apps.pdf`
- 标题: Harness design for long-running application development
- 作者: Prithvi Rajasekaran
- 作者机构: Anthropic Engineering
- 发布日期: 2026-03-24
- 原文链接: https://www.anthropic.com/engineering/harness-design-long-running-apps

## 摘要
这篇文章在早期长时运行 harness 的基础上进一步提出：复杂任务不仅会受到上下文漂移影响，还会受到自我评估偏乐观的影响。因此，harness 不只要解决跨轮次连续性，还要把生成与评估分离，并通过 planner、generator、evaluator 的角色拆分和阶段合同机制，让系统在长时间运行中持续纠偏。

## 关键要点
- 长时任务常见两类失效：上下文焦虑与自我评估偏差。
- context reset 能解决一部分连续性问题，但不是所有场景都必须依赖它。
- 生成与评估分离，是比“让模型自我批评”更可行的工程杠杆。
- 在高层需求与具体实现之间，阶段合同可以充当桥梁。
- 多代理 harness 质量更高，但也显著增加成本与时延。

## 重要概念
- [[wiki/concepts/harness工程|harness工程]]
- [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]]

## 对知识库的影响
- 扩展了 `harness工程` 的内涵，使其不仅包含交接工件，也包含角色分离与阶段验收机制。
- 让知识库中关于 harness 的讨论，从“如何持续运行”推进到“如何持续纠偏并稳定提高质量”。

## 开放问题
- 哪些任务需要 planner，哪些任务只需要 generator + evaluator？
- 阶段合同是否能迁移到知识库维护、研究分析等非代码场景？
