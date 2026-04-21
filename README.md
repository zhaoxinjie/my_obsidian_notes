# 我的个人知识库

这套 Obsidian 仓库是按 Karpathy 提出的 `LLM Wiki` 思路搭的：

- `raw/` 放原始资料，只增不改
- `wiki/` 放整理后的知识页，由 LLM 持续维护
- `AGENTS.md` 规定 LLM 以后应该如何摄入、更新、回答、巡检

你可以把 Obsidian 理解成前端界面，把 LLM 理解成知识库维护员。

## 目录

- `00 Home.md`: 入口页
- `raw/`: 原始资料区
- `wiki/`: 已整理知识区
- `system/WORKFLOWS.md`: 你日常怎么用
- `system/templates/`: 模板

## 最简单的使用方式

1. 把文章、网页剪藏、读书笔记、会议纪要、PDF 摘要放进 `raw/inbox/`
2. 对我说："把 `raw/inbox/xxx.md` 摄入知识库"
3. 我会：
   - 读原文
   - 生成或更新 `wiki/sources/` 里的来源页
   - 更新相关主题页、人物页、项目页
   - 更新 `wiki/index.md`
   - 记录到 `wiki/log.md`
4. 你在 Obsidian 里通过双链、图谱、搜索来浏览结果

## 推荐习惯

- 新资料先丢 `raw/inbox/`
- 一次处理一篇，质量最好
- 把重要问题直接问出来，让答案沉淀进 `wiki/questions/` 或 `wiki/syntheses/`
- 每周做一次 lint，让知识库持续变干净

## 推荐插件

- Obsidian Git: 自动备份
- Dataview: 后续如果你想做动态索引会很有用
- Web Clipper: 把网页快速转成 markdown

## 现在这套库更适合放什么

- 读书/文章摘录与总结
- 个人项目记录
- 方法论、框架、技能学习
- 长期主题研究
- 对自己的决策、目标、复盘的持续跟踪
