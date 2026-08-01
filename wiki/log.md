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

## [2026-04-22] discuss+ingest | The Think Tool
- 先讨论定位，再决定不单独建概念页
- 将其核心观点综合进 `工具`
- 新建来源页：`Anthropic Engineering - The Think Tool`
- 更新 `wiki/index.md`

## [2026-04-22] discuss+ingest | Demystifying Evals for AI Agents
- 先讨论定位，再决定不单独建概念页
- 将其核心观点综合进 `AI评估`
- 新建来源页：`Anthropic Engineering - Demystifying Evals for AI Agents`
- 补充了更可操作的 eval 落地方法
- 更新 `wiki/index.md`

## [2026-05-14] discuss+ingest | Spider 2.0 and warehouse planning
- 新建来源页：`Spider 2.0 - Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows`
- 新建综合页：`企业数仓 Text-to-SQL Agent 落地清单`
- 新建综合页：`企业数仓 Text-to-SQL Agent 落地规划`
- 将 Spider 2.0 的启发转译为面向数仓场景的实战建议
- 更新 `wiki/index.md`

## [2026-05-23] discuss+ingest | The Founders Playbook and AI-native startup branch
- 新建来源页：`Anthropic - The Founders Playbook: Building an AI-Native Startup`
- 新建综合页：`AI-native 创业`
- 将其定位为一条独立支线，而不是并入 agent 工程主线
- 更新 `wiki/index.md`

## [2026-06-09] ingest | A Harness for Every Task: Dynamic Workflows in Claude Code
- 将 `claude_dynamic_workflows_article.pdf` 归档到 `raw/assets/`
- 新建来源页：`Claude - A Harness for Every Task Dynamic Workflows in Claude Code`
- 将动态工作流综合进 `harness工程`，补充任务专属 harness、子代理编排、失败模式与适用边界
- 轻量更新 `AI评估` 与 `工具`，明确 workflow eval 与工具上层编排的关系
- 更新 `agent 工程地图` 与 `wiki/index.md`

## [2026-06-10] ingest | Your Agent May Misevolve
- 将 `2509.26354v2.pdf` 归档到 `raw/assets/`
- 新建来源页：`Shao et al - Your Agent May Misevolve`
- 新建概念页：`自演化智能体风险（Misevolution）`
- 将论文的模型、记忆、工具、workflow 四条演化风险整理为 agent 安全主线
- 更新 `工具`、`MCP`、`AI评估`、`harness工程` 的相关风险与治理链接
- 将 `agent 工程地图` 从 6 层扩展为 7 层，新增安全与演化层
- 更新 `wiki/index.md`

## [2026-07-30] maintenance | rename Your Agent May Misevolve PDF
- 将 `raw/assets/2509.26354v2.pdf` 重命名为 `raw/assets/Your Agent May Misevolve - Emergent Risks in Self-evolving LLM Agents.pdf`
- 更新来源页中的本地 PDF 链接

## [2026-06-26] ingest | No Silver Bullet
- 下载并归档 Fred Brooks `No Silver Bullet` PDF 到 `raw/assets/Brooks-NoSilverBullet.pdf`
- 新建来源页：`1986 Brooks - No Silver Bullet`
- 新建概念页：`没有银弹`
- 新建实体页：`Fred Brooks`
- 将“本质复杂度 / 偶然复杂度”补充进 `构建高效智能体`，用于解释 AI agent 为什么不是软件工程银弹
- 更新 `wiki/index.md`

## [2026-06-26] refactor | 软件工程概念页
- 将概念页 `没有银弹` 重命名并扩展为 `软件工程`
- 把“没有银弹”调整为 `软件工程` 下的一章，便于后续继续沉淀架构、复杂度和工程管理内容
- 更新相关双链、`wiki/index.md` 和来源页引用

## [2026-07-09] ingest | Harness Engineering for Self-Improvement
- 将 `harness_engineering_for_self_improvement.pdf` 归档到 `raw/assets/`
- 新建来源页：`Lilian Weng - Harness Engineering for Self-Improvement`
- 将文章的 RSI / harness optimization / Self-Harness / evolutionary search 观点综合进 `harness工程`
- 更新 `上下文工程`，补充 ACE、MCE 和“上下文管理机制本身可被优化”的理解
- 更新 `自演化智能体风险`，补充有边界可编辑面、外部权限/评估层和 held-in / held-out 验证
- 更新 `AI评估`，补充 self-improvement eval、负结果和长期健康评估
- 更新 `agent 工程地图`，新增“自我改进与优化层”
- 更新 `wiki/index.md`

## [2026-07-09] ingest | LLM Powered Autonomous Agents
- 将 `lilianweng-2023-06-23-agent.pdf` 归档到 `raw/assets/`
- 新建来源页：`Lilian Weng - LLM Powered Autonomous Agents`
- 将 planning / memory / tool use 的早期 agent 基础框架综合进 `构建高效智能体`
- 更新 `工具`，补充 API-Bank 的三级工具使用能力
- 更新 `上下文工程`，补充 agent 记忆类型与 recency / importance / relevance 召回模型
- 更新 `AI评估`，补充 ChemCrow 案例对 LLM-as-judge 在专业领域的限制
- 更新 `agent 工程地图` 与 `wiki/index.md`

## [2026-07-09] ingest | Why We Think
- 将 `lilianweng-2025-05-01-thinking.pdf` 归档到 `raw/assets/`
- 新建来源页：`Lilian Weng - Why We Think`
- 新建概念页：`测试时计算（test-time compute）`
- 将我们讨论出的 `prompt / loop / harness` 分工写入 `harness工程`
- 更新 `工具`，补充工具作为外部思考与验证资源
- 更新 `AI评估`，补充 CoT 忠实性、CoT monitor 与 reward hacking 风险
- 更新 `构建高效智能体`，补充 thinking budget 的边界
- 更新 `自演化智能体风险`，补充优化 CoT 可能导致隐蔽化 reward hacking
- 更新 `agent 工程地图` 与 `wiki/index.md`

## [2026-07-31] maintenance | rename Lilian Weng harness PDF
- 将 `raw/assets/harness_engineering_for_self_improvement.pdf` 重命名为 `raw/assets/lilianweng-2026-07-04-harness.pdf`
- 更新 `Harness Engineering for Self-Improvement` 来源页中的作者双链与原始文件路径
