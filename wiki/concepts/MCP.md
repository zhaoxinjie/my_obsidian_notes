---
type: concept
status: active
created: 2026-04-21
updated: 2026-04-21
source_count: 2
tags:
  - concept
  - mcp
  - tool
  - protocol
---

# MCP（Model Context Protocol）
## 定义
`MCP（Model Context Protocol）` 是一种让 AI agent 与外部工具、数据源、服务系统建立标准化连接的协议（protocol）。它的目标是把“每个 agent 都要为每个工具单独做一套集成”的模式，变成“一次实现协议，就能接入整个工具生态”的模式。

## 为什么重要
如果没有统一协议，agent 接工具的方式会高度碎片化（fragmented）：每个模型、每个平台、每个工具系统都要重复写集成层，成本高，也很难扩展。

MCP 的价值在于：
- 把工具接入从一次性定制开发，转成协议化接入（protocol-based integration）
- 让 agent 能在更大规模的工具集合上工作
- 为后续的动态发现、按需加载、代码执行等能力提供基础

## 我们目前对它的几个关键判断
### 1. MCP 是工具生态的连接层（integration layer）
- 它本身不是某个具体工具
- 它也不是某个单独 agent 产品
- 它更像 agent 与外部世界之间的标准接口层（standard interface layer）

### 2. MCP 解决的是规模化连接问题（scalable connectivity）
- 工具少的时候，手写集成还能接受
- 工具一多，集成碎片化会迅速成为瓶颈（bottleneck）
- MCP 的意义就在于让工具扩展能力不再线性依赖手工接线

### 3. MCP 会把工具问题推向“发现、加载、执行”三个新问题
- 一旦工具数量上来，问题不再只是“能不能接”
- 而会变成：怎么发现相关工具（discovery）、怎么按需加载（deferred loading）、怎么高效执行（efficient execution）
- 所以 MCP 是起点，不是终点

### 4. MCP 让工具工程、上下文工程和执行模式重新耦合
- 工具定义怎么写，会影响上下文负担
- 工具怎么加载，会影响 agent 的决策质量
- 工具怎么执行，会影响 token 消耗、时延和稳定性

换句话说，MCP 不是孤立协议，它会直接改变 agent 工程的其他层。

## 核心组成
### 1. 协议化接入
- 用统一格式暴露工具和资源
- 让不同客户端和不同服务之间减少定制适配

### 2. 工具与资源暴露
- 通过 MCP server 向 agent 暴露可调用能力
- 这些能力可能是 API、文件系统、数据库、SaaS 服务或本地程序

### 3. 生态兼容性
- 一旦 agent 实现了 MCP，就更容易复用已有 server 和工具
- 一旦工具实现了 MCP，也更容易被多个 agent 客户端共享

## 与其他概念的关系
- 它是 [[wiki/concepts/工具|工具（tool）]] 的协议基础（protocol foundation）。工具页更关注工具怎么设计，MCP 更关注工具怎么接入和暴露。
- 它和 [[wiki/concepts/上下文工程|上下文工程（context engineering）]] 强相关，因为大量 MCP 工具定义会直接占用上下文。
- 它也和 [[wiki/concepts/构建高效智能体|构建高效智能体（Building Effective Agents）]] 有关，因为 agent 一旦进入多工具环境，协议层设计就会影响整体系统复杂度。

## 进一步会遇到的问题
### 1. 工具太多
- 当 server 和工具数量上升时，直接把所有定义塞进上下文会非常昂贵

### 2. 中间结果太重
- 每次工具返回都进入上下文，会让长任务越来越笨重

### 3. 动态选择难
- agent 需要学会在大工具库里发现、筛选、学习和调用合适的工具

## MCP 的进阶问题（advanced MCP patterns）
### 1. 代码执行（code execution）
当 MCP 工具规模继续扩大后，直接 tool calling 往往会变得低效（inefficient）。

主要原因有两个：
- 工具定义（tool definitions）本身会占掉大量上下文
- 工具的中间结果（intermediate results）会持续吞噬 token

因此，更高效的做法往往不是让模型逐个手动调用工具，而是让模型写一小段程序（write a small program），再由程序去搜索、过滤、循环、聚合和调用工具。

这个转变的意义在于：
- 把一部分推理从自然语言上下文搬回程序执行层（move reasoning from prompt space to execution space）
- 减少上下文窗口里反复堆积的工具说明和中间结果
- 让 agent 在大工具库下仍然保持可扩展性（scalability）

### 2. 高级工具使用（advanced tool use）
当工具数量继续增长，问题不再只是“能不能调用”，而会演化成三个更具体的问题：
- 如何发现相关工具（tool discovery）
- 如何按需加载工具（deferred loading）
- 如何动态执行和编排工具（dynamic execution and orchestration）

这说明 MCP 的真正挑战不是接入本身，而是：
- 如何在大规模工具生态中保持效率
- 如何在不污染上下文的情况下找到对当前任务最有用的工具
- 如何让 agent 学会在很多工具之间形成有效策略

这篇带来的一个更强判断是：
- 大规模工具使用的核心不再是 `call tool`
- 而是 `discover -> load -> execute`

也就是说，当工具库足够大时，问题已经从“模型会不会用工具”，转向“模型如何在巨大工具空间里找到、理解并调用对的工具”。

换句话说，tool use 正在从：
- 函数调用（function calling）

逐渐升级为：
- 工具编排（tool orchestration）

这也是为什么高级工具使用不应被理解成“又多了几个工具 API”，而应被理解成：
- agent 面对大规模工具生态时的一套新操作模式（a new operating mode for large tool ecosystems）

### 3. 从协议层走向系统层
早期理解 MCP，很容易把它看成“统一接工具的标准”。
但随着工具库增大，它会自然演化成一个更大的系统问题：
- 协议如何暴露能力
- 能力如何被发现
- 定义如何进入上下文
- 调用如何被执行
- 结果如何被整理回系统

所以，MCP 不只是一个连接协议（connection protocol），也是后续 agent 系统规模化的入口点（entry point to scalable agent systems）。

## 我们目前对 MCP 的总体理解
如果把当前几篇 MCP 相关文章放在一起看，可以把 MCP 这条主线压缩成三步：

### 1. 先解决连接问题
- 如何让 agent 标准化接入外部工具和资源
- 这是 MCP 作为协议层最基础的意义

### 2. 再解决效率问题
- 当工具太多时，直接 tool calling 会让上下文和 token 成本快速膨胀
- 这时就需要代码执行、按需调用和更高效的执行方式

### 3. 最后解决生态问题
- 当工具生态继续扩大，agent 需要具备发现、加载、学习和编排工具的能力
- 这时 MCP 不再只是“接工具协议”，而更像“工具生态运行环境”的基础层

因此，MCP 的演进方向可以概括为：
- 从“连接工具（connect tools）”
- 到“高效使用工具（use tools efficiently）”
- 再到“在大规模工具生态里组织工具（organize tools at ecosystem scale）”

## 对知识库场景的启发
- 如果以后你给知识库 agent 接很多外部能力，比如网页检索、本地文件分析、数据库查询、日历、任务系统，那么统一协议会明显降低系统复杂度
- 但一旦接入变容易，真正的难点就会从“接不接得上”转向“怎么让 agent 在大量工具里仍然高效工作”

## 相关来源
- [[wiki/sources/2026-04-21 Anthropic Engineering - Code Execution with MCP|2026-04-21 Anthropic Engineering - Code Execution with MCP]]
- [[wiki/sources/2026-04-21 Anthropic Engineering - Introducing Advanced Tool Use|2026-04-21 Anthropic Engineering - Introducing Advanced Tool Use]]

## 张力与开放问题
- MCP 是否会成为长期稳定标准，还是未来会被更高层抽象替代？
- 当工具规模继续扩大时，协议统一是否足以解决效率问题？
- MCP 让接入更容易后，权限、安全和可观察性会不会成为更大的新瓶颈？
