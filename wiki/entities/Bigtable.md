---
type: entity
status: active
created: 2026-08-03
updated: 2026-08-03
tags:
  - entity
  - database
  - distributed-systems
  - google
---
# Bigtable

## 简介
Bigtable 是 Google 在约 2004 年构建的分布式宽列数据库。它采用按行键排序的三维映射、tablet 分片、WAL、memtable、SSTable 和 LSM-tree，并把数据存储在分布式文件系统 Colossus 中。

2006 年原始论文影响了 HBase、Cassandra 等非关系数据库。2015 年推出的 Cloud Bigtable 与 Google 内部版本共享同一后端，但控制面、网络连接和客户端架构有所不同。

## 核心边界
- 擅长超大规模、低延迟、高吞吐的键范围访问。
- 单行内提供事务语义；不提供跨行、跨副本 ACID。
- 多主复制默认采用异步、最终一致模型。
- 灵活 schema 和简单数据模型是扩展性的来源，也把部分建模责任交给应用。

## 二十年演化
Bigtable 的总体架构没有被重写，而是在稳定内核周围持续增加：
- 多主复制、故障切换与跨地域访问
- GoogleSQL、CDC、CRDT counter 与物化视图
- 外置 compaction、并行 GC、location proxy 与负载再平衡
- row cache、分片 Bloom filter 与请求优先级
- 端到端 checksum、snapshot、backup 与持续完整性检查
- autosizing、autoscaling、冷热分层、offline access 与 bulk import

它是 [[wiki/concepts/分布式存储系统|分布式存储系统]] “稳定内核、扩展外围”路线的代表案例，也为 [[wiki/concepts/软件工程|软件工程]] 中长寿系统如何持续演化提供了实证。

## 相关页面
- [[wiki/sources/2026-05-31 Baltieri et al - Twenty Years of Bigtable|2026-05-31 Baltieri et al - Twenty Years of Bigtable]]
- [[wiki/concepts/分布式存储系统|分布式存储系统]]
- [[wiki/concepts/软件工程|软件工程]]

