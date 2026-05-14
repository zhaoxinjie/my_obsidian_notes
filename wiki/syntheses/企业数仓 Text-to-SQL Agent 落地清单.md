---
type: synthesis
status: active
created: 2026-05-14
updated: 2026-05-14
source_count: 1
tags:
  - synthesis
  - warehouse
  - text-to-sql
  - agent
---

# 企业数仓 Text-to-SQL Agent 落地清单
## 一句话结论
Spider 2.0 的直接启发是：企业数仓里的 `text-to-SQL` 不是“生成 SQL”问题，而是“在复杂数据环境里完成分析任务”问题。

## 现在最该提前做好的事
### 1. 先统一语义层（semantic layer）
- 定义核心指标、维度、时间口径、主键、常见 join 路径。
- 如果口径没统一，模型越强，错得越稳定。

### 2. 补齐高质量元数据（metadata）
- 每张核心表至少要有：业务描述、字段说明、负责人、更新频率、常见用途、样例查询。
- 超大 schema 下，元数据质量会直接决定检索与 schema linking 成败。

### 3. 建业务别名字典（business alias dictionary）
- 把“新增、活跃、转化、GMV、留存、成交”等业务词统一映射到正式口径。
- 不做这一步，用户说法和仓内定义会长期错位。

### 4. 整理方言知识包（dialect knowledge pack）
- 把你们实际使用的数据库方言整理出来，例如 `BigQuery`、`Snowflake`、`ClickHouse`。
- 优先覆盖：时间函数、数组/json、窗口函数、日期截断、null 处理、权限限制。

### 5. 做执行反馈闭环（execution feedback loop）
- 让系统能试跑 SQL、拿到报错、再修正。
- 没有执行反馈，复杂任务通常做不完。

### 6. 做错误分类体系（failure taxonomy）
- 至少区分：找错表、找错字段、指标口径错、join 错、时间范围错、方言错、能跑但业务答案错。
- 不分类型，你们只能看到“总分低”，却不知道该补哪里。

## 评估最小闭环
### 1. 先收 `20-50` 个真实任务
- 不先造 benchmark，先用真实业务问题、历史失败案例、内部常问分析题。

### 2. 每题补齐 5 个字段
- 用户问题
- 正确业务口径
- 相关表/字段
- 参考 SQL / workflow
- 常见错误点

### 3. 评估至少分 4 层
- 检索层：有没有找到对的表、字段、文档
- 规划层：有没有形成对的分析路径
- 执行层：SQL 能不能跑通、能不能修错
- 业务层：最终结果是否符合真实口径

### 4. 任务至少分 3 类
- 核心任务：必须稳
- 边界任务：最容易出错
- 挑战任务：现在做不好，但未来要提升

## 现在不要急着做的事
- 不要先追求“全仓覆盖”
- 不要先追求“最强模型”
- 不要先堆海量评测题
- 不要只看最终 SQL 是否能执行

## 更值得优先投入的方向
- 指标口径标准化
- 元数据补全
- 别名映射
- 方言文档整理
- 试跑与报错反馈
- transcript 级失败复盘

## 相关来源
- [[wiki/sources/2026-05-14 Spider 2.0 - Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows|2026-05-14 Spider 2.0 - Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows]]
