---
type: source
status: active
created: 2026-08-03
updated: 2026-08-03
tags:
  - source
  - database
  - distributed-systems
  - bigtable
---
# 2026-05-31 Baltieri et al - Twenty Years of Bigtable

## 来源
- 标题：`Twenty Years of Bigtable`
- 作者：Fabio Baltieri、Bora Beran、Igor Bernstein 等 Google Bigtable 团队成员
- 会议：SIGMOD Companion 2026
- 日期：2026-05-31
- DOI：`10.1145/3788853.3803095`
- 原始文件：`raw/assets/Twenty Years of Bigtable.pdf`

## 一句话总结
Bigtable 的二十年表明，长寿分布式系统不必频繁推翻核心架构；更有效的路径是守住简单数据模型和关键约束，把复制、分析、可靠性与资源治理等新能力尽量做成异步、可隔离、可独立扩展的外围机制。

## 系统规模与基本架构
论文写作时，Bigtable 管理约 `10 EB` 数据，总峰值约 `70 亿 QPS`；单表可超过 `1.6 × 10^15` 行和 `1 EB`，单集群可超过 `2.5 亿 QPS`。

它的核心结构与 2006 年论文基本一致：
- 数据是按 `(row key, column key, timestamp)` 索引的三维有序映射，值是不透明字节数组。
- 行空间按字典序切分为 `tablet`；tablet 是托管、移动和负载均衡的基本单元。
- 列归入 column family，再按 locality group 形成存储和 compaction 单元。
- 持久化由 WAL、memtable、不可变 SSTable 与 LSM-tree compaction 组成。
- master 管理控制面和 tablet 分配，客户端直接访问 tablet server；数据本身放在 Colossus 中，因此移动 tablet 通常不需要搬数据。
- 事务边界仍是单行，跨行和跨副本不提供 ACID 保证。

## 二十年间扩展出的能力

### 1. 多主复制
复制是原始论文之后最重要的新能力。副本之间不在前台写路径上协调，而是异步拉取 mutation，因此用最终一致性换取低写延迟、高可用和较低成本。

关键设计包括：
- 用 replication watermark 按来源和行区间追踪进度；同一来源、同一行的 mutation 保序，不承诺跨行顺序。
- 用全局 sequencer 和 last-write-wins 解决同一行的冲突。
- 目的副本采用 pull 模式，减轻写入源的负担，并简化拉取端崩溃后的恢复。
- 每个 tablet 持久化 replication position，实现远端 mutation 的 exactly-once delivery；这对计数器等非幂等操作很重要。
- 新增副本时，BEAR 一边批量复制 SSTable，一边处理实时写入，并给历史文件较低 sequencer，从而无需停写。

这套模型适合读写隔离、地理就近访问和故障切换，但应用必须接受跨行、跨副本弱一致性的边界。

### 2. 数据库内分析能力
Bigtable 从“存储与摄入层”继续向数据库内处理扩展：
- 以 GoogleSQL 作为高级查询接口，并为宽列模型增加 collection、temporal filter、pivot、unnest 与 row-key schema。
- CDC 按 tablet 分片，以 `(row, replica, logical time)` 续传位置提供至少一次交付；Beam adapter 封装了 split/merge 时的状态移交。
- Counters/CRDT 在 LSM 层的 changelog 中同时保存已解析小计和未解析操作，使异步复制下的增减与删除仍能正确合并。
- 原生物化视图把持续 SQL 转换下推到 tablet server，使用 mapper、shuffle table、reducer 和 finalizer 构成内部流水线，以 watermark 跟踪进度。

共同模式是：尽量复用既有的日志、LSM、watermark、coprocessor 和异步处理基础，而不是把复杂计算塞进前台写路径。

## 在规模压力下的工程改造

### 可扩展性
- 冷 tablet 应更大、热 tablet 应更小；tablet 太多会同时拖累 server、client location cache、master 和 metadata。
- 把 merge/major compaction 的文件构建外置到独立、可自动伸缩的 worker，减少对在线流量的干扰。
- master 用细粒度锁和并行 schema 更新扩展控制面。
- 文件 GC 从 master 串行执行改为 master 协调、tablet server 并行处理。
- location lookup 逐步增加旧位置 hint 与独立 autoscaled proxy，避免 metadata 热点。
- rebalancer 不总是移动最热 tablet；保留热点、搬走较冷 tablet，有时能避免大量客户端缓存失效。

### 性能
- row cache 在 block cache 之上缓存稀疏行结果，使 point read 的 CPU 最多降低约 `25%`。
- Bloom filter 从整份常驻内存改为分片、按需缓存，并根据查询形态做 hybrid filter；其利用率提升约 `4 倍`。
- 请求优先级用于隔离在线点查与分析扫描，支持 HTAP 型混合负载。

### 可靠性
- snapshot 用 copy-on-write 低成本创建；backup 再把底层文件复制到独立服务或其他集群。
- CRC32C 覆盖客户端、RPC、commit log、memtable、复制和 SSTable 读写链路。
- SSTable 在安装进 metadata 前被完整读回、解密、解压、解析并校验；代价较高，但多年几乎消除了 SSTable 不一致。
- compaction 在日常重写中顺带持续验证 checksum；关键元数据、commit log gap 和加密密钥也有额外检查。

### 资源效率
论文把资源效率归纳为三类：减少预留余量、减少单位工作用量、把任务下沉到更便宜的资源层。
- Autosizer 在集群内部快速增减 slack pool 中的 server；Google 级 Autoscaling 负责较慢的资源申请与归还。
- cache sizer 用 TCO 反馈循环在 RAM 成本与 miss 带来的 CPU/I/O 成本之间寻找拐点。
- tiered storage 分开冷热数据；offline access 让批处理直接读 Colossus 中的 SSTable；bulk import 让 worker 直接构建 SSTable。

## 运维经验
Bigtable 最初计划由各使用团队自行运行，但很快出现知识碎片化和临时方案。自 2006 年中起，它主要由专门 SRE 团队以公司级服务运行。

可复用经验包括：
- 用 metadata prober 和模拟正常用户的 black-box prober 分别监控内部可用性与端到端延迟。
- 将系统 metadata 放入独立 partition，再用 partition、subpartition、request priority 和 isolation class 隔离用户与负载类型。
- 标准化 tablet server 规格，以可预测性和可运维性换掉任意资源形状的灵活性。
- 默认给每张表配置备份，把安全基线做成平台默认值，而不是依赖每个用户主动配置。

## 核心启发
- **稳定内核，扩展外围。** 核心架构能持续二十年，靠的不是冻结功能，而是保持简单边界，让新能力复用并扩展原有机制。
- **异步不是免费复杂度。** 它把延迟移出前台路径，却要求显式维护 watermark、sequencer、续传状态、幂等性和垃圾回收安全条件。
- **规模问题常常先击穿控制面。** tablet 数量、metadata、location lookup、GC 和 rebalancing 会在数据容量之外形成新的瓶颈。
- **隔离是性能、可靠性和成本的共同工具。** 外置 compaction、独立 metadata partition、请求优先级和 offline access 都是在把不同工作负载放到不同资源域。
- **可靠性来自昂贵但系统化的验证。** 端到端 checksum、安装前读回和持续巡检看似浪费资源，却把极小概率错误挡在大规模放大之前。
- **服务化是架构的一部分。** 集中 SRE、标准资源形状、默认备份和统一探针，使系统知识与正确配置不再依赖每个使用团队。

## 对知识库的影响
- 新建 [[wiki/entities/Bigtable|Bigtable]] 实体页，记录系统定位、边界与长期演化。
- 新建 [[wiki/concepts/分布式存储系统|分布式存储系统]] 概念页，沉淀可迁移的架构和运维原则。
- 更新 [[wiki/concepts/软件工程|软件工程]]，补充“稳定内核、持续演化”的长寿系统案例。

## 开放问题
- Bigtable 的单行事务与最终一致复制边界，在什么业务模型下会成为不可接受的应用复杂度？
- 当 SQL、CDC、CRDT 和物化视图继续进入存储引擎时，如何防止“稳定内核”逐渐变成难以演进的功能堆叠？
- 外置 compaction、offline access 和 serverless pool 降低了在线资源成本，但会引入多少新的控制面与端到端诊断复杂度？

