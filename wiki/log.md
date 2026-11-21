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

## [2026-08-13] answer+ingest | nanochat 架构与学习路径
- 阅读 `karpathy/nanochat` 的 README、仓库树、speedrun、模型、tokenizer、dataloader、预训练、SFT、RL、评测与推理代码
- 基于 `master` commit `92d63d4` 新建来源页：`Karpathy - nanochat`
- 新建综合页：`nanochat 架构与学习路径`
- 将仓库整理为实验配方、阶段控制器、可复用内核、任务契约和测试五层架构
- 给出从 CPU/MPS 跑通、模型主干、训练 step、SFT/eval、KV cache 到研究优化的四周学习路线
- 更新 `Andrej Karpathy` 实体页和 `wiki/index.md`

## [2026-10-16] practice | 数仓 AI 工程第 01 练
- 新建 [[wiki/syntheses/数仓 AI 工程每日实战]]，提供字段变化检查的完整 Python 示例、契约、运行方式与自测标准。
- 关联工具、MCP、构建高效智能体及企业数仓落地清单；更新 `wiki/index.md`。
- 当前仅代表已布置，尚无用户完成或掌握反馈。

## [2026-10-17] practice | 数仓 AI 工程第 02 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加字段说明完整性检查，提供独立运行的示例、输入契约、异常自测与占位说明挑战。
- 保留第 01 练复习入口；两练均待用户反馈，不推定已掌握。更新 `wiki/index.md`。

## [2026-10-18] practice | 数仓 AI 工程第 03 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加检查结果转 Markdown 治理报告练习，覆盖边界契约、状态一致性与未知规则拒绝处理。
- 提供独立运行示例、自测和排序汇总挑战；更新 `wiki/index.md`，保留前两练待反馈状态。

## [2026-10-19] practice | 数仓 AI 工程第 04 练
- 在 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加白名单 SQL 草稿生成练习，包含日期校验、基础自测与 limit 参数挑战。
- 明确输入校验、SQL 执行验证与业务验证的边界；更新 `wiki/index.md`，保留前三练待反馈状态。

## [2026-10-20] practice | 数仓 AI 工程第 05 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加 SQL 生成器 JSON 调用接口练习，覆盖稳定错误码、输入输出分层与进程退出码。
- 提供完整独立示例、正常/异常请求和接口版本挑战；更新 `wiki/index.md`，前四练仍待用户反馈。

## [2026-10-21] practice | 数仓 AI 工程第 06 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加 SQL 工具黑盒回归测试，提供 system/exercises/06-sql-tool-tests 下完整工具和测试文件。
- 验证三项测试通过，并在临时副本注入 LIMIT 错误确认测试能失败；前五练仍待反馈，更新 `wiki/index.md`。

## [2026-10-26] practice | 数仓 AI 工程第 07 练
- 完成 2026-10-24 触发的 Skill 工作流程练习，追加至 [[wiki/syntheses/数仓 AI 工程每日实战]]；未为缺席日期补编课次。
- 在 system/exercises/07-sql-skill 下提供 SKILL.md 与完整 SQL 工具；采用手动加载演练，未安装或宣称自动发现生效。
- 更新 `wiki/index.md`；第 01–06 练仍待用户反馈。

## [2026-10-28] practice | 数仓 AI 工程第 08 练
- 完成上次未交付的只读 MCP 练习，追加至 [[wiki/syntheses/数仓 AI 工程每日实战]]，提供 catalog/server/client 与固定版本依赖文件。
- 官方文档接口已核对，语法与业务函数检查通过；依赖下载未完成，协议连通仍待验证，不宣称运行成功。
- 更新 `wiki/index.md`；前七练仍待反馈。

## [2026-10-29] practice | 数仓 AI 工程第 09 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加工具返回值错误分支练习，以无依赖模拟输入练习继续/确认/停止的契约。
- 验证四个命令行场景与五项额外异常输入；提供权限错误挑战。更新 `wiki/index.md`，前八练及 MCP 连通仍待反馈。

## [2026-10-30] practice | 数仓 AI 工程第 10 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加 SQL 草稿审核版本核对练习，模拟审核匹配、过期、拒绝和待审核状态。
- 验证四个命令行场景与七项非法输入/审核检查；明确指纹不证明身份、不代表真实授权且不执行 SQL。更新 `wiki/index.md`，前九练仍待反馈。

## [2026-10-31] practice | 数仓 AI 工程第 11 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加模拟元数据查询运行记录练习，提供 run_id、顺序号、事件摘要与停止原因。
- 实际核对 6 行 JSON、正常/失败路径及三类非法输入；更新 `wiki/index.md`。前十练及 MCP 连通仍待反馈。

## [2026-11-01] practice | 数仓 AI 工程第 12 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加决策评测练习，提供独立 policy、四个标签案例、失败明细与误继续统计。
- 实测原规则 4/4；临时错误规则 1/4、误继续 3 次并非零退出，交付规则保持正确。更新 `wiki/index.md`，前十一练仍待反馈。

## [2026-11-02] practice | 数仓 AI 工程第 13 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加查结构→字段校验→SQL 草稿→待审核的独立工作流，提供完整本地依赖副本。
- 验证三条主路径、五项异常输入及三条提前停止路径不调用生成器；更新 `wiki/index.md`。前十二练仍待反馈，不宣称实现自主 Agent。

## [2026-11-03] practice | 数仓 AI 工程第 14 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加可替换查询接口与故障注入练习，提供独立工具、工作流与断言示例。
- 正常、超时、损坏结果三个场景通过，异常场景实际核对生成器调用为 0；更新 `wiki/index.md`。前十三练仍待反馈。

## [2026-11-04] practice | 数仓 AI 工程第 15 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加工具调用白名单与次数预算练习，提供完整模拟提议、执行关卡与真实调用计数断言。
- 四项主场景与非法预算/空提议/未知表检查通过；更新 `wiki/index.md`。前十四练仍待反馈，固定提议回放不宣称完整 Agent。

## [2026-11-05] practice | 数仓 AI 工程第 16 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加只读查询有限重试练习，只重试明确超时，强调每次尝试计入预算。
- 三项主场景及非法预算、损坏结果、非重试异常检查通过；更新 `wiki/index.md`。前十五练仍待反馈。

## [2026-11-06] practice | 数仓 AI 工程第 17 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加共享调用预算练习，将多次查询及其重试统一计数。
- 三条共享预算路径及非法额度、零预算、业务错误和超时耗尽检查通过；更新 `wiki/index.md`，前十六练仍待反馈。

## [2026-11-07] practice | 数仓 AI 工程第 18 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加带来源字段上下文包练习，只输出请求字段、类型、说明与快照来源。
- 正常/未知字段、五项异常输入和快照隔离检查通过；更新 `wiki/index.md`。前十七练仍待反馈，未宣称模型效果或 MCP 连通已验证。

## [2026-11-08] practice | 数仓 AI 工程第 19 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加模拟模型回答契约校验，区分 ready 与 needs_info，拒绝矛盾参数与问题列表。
- 三个脚本场景及六项额外异常检查通过；更新 `wiki/index.md`。前十八练仍待反馈，未进行真实模型/MCP 测试。

## [2026-11-09] practice | 数仓 AI 工程第 20 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加模型回答到草稿工作流的交接关卡，核对输出格式和已确认参数。
- 四条路径实际通过，被阻断的回答均核对工作流调用 0 次；更新 `wiki/index.md`。前十九练仍待反馈，未宣称获得真实人工授权或完成 Agent 集成。

## [2026-11-10] practice | 数仓 AI 工程第 21 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加回答回归案例文件与回放练习，严格区分案例文件损坏和被测回答损坏。
- 实测原校验器 4/4、错误校验器 2/4 并非零退出，重复 id 被拒绝；更新 `wiki/index.md`。前二十练仍待反馈。

## [2026-11-11] practice | 数仓 AI 工程第 22 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加字段变更→下游任务复核清单练习，使用单表显式依赖模拟，明确非完整血缘。
- 原样例、相同结构/仅新增字段及四项非法依赖检查通过；更新 `wiki/index.md`。前二十一练仍待反馈。

## [2026-11-12] practice | 数仓 AI 工程第 23 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加指定日期分区就绪检查，区分缺失、运行中、失败及已就绪。
- 四条状态路径及五类非法清单、空清单核对通过；更新 `wiki/index.md`。前二十二练仍待反馈。

## [2026-11-13] practice | 数仓 AI 工程第 24 练
- 向 [[wiki/syntheses/数仓 AI 工程每日实战]] 追加分区行数波动检查，区分超阈值、缺统计、零基线和实际零行。
- 五条主场景、额外边界及五类非法输入通过；更新 `wiki/index.md`。前二十三练仍待反馈。

## [2026-11-16] practice | 数仓 AI 工程第 25 练
- 在 [[wiki/syntheses/数仓 AI 工程每日实战]] 增加统计口径检查，区分不一致与缺失元数据；更新目录。
- 验证三条运行路径、两项差异与基线缺失；前二十四练仍待反馈。

## [2026-11-21] ingest | Claude 记忆官方文档整理
- 按用户明确的入库请求，读取六页 PDF，并核对其中三份官方网页；文档内容作为来源材料，不作为操作指令。
- 原样归档到 `raw/assets/claude_memory_docs_2026-11.pdf`，保留整理稿性质和原始路径。
- 新建 [[wiki/sources/2026-11-21 Claude 记忆官方文档整理]]，标注引用占位符、组织默认开关更新及历史版本保留边界。
- 更新 [[wiki/concepts/上下文工程]]，补充规则/经验分工、读写治理与记忆污染风险，并关联既有 LLM Wiki 和自演化风险页面。
- 更新 `wiki/index.md`；保留工作区原有的无关修改。
