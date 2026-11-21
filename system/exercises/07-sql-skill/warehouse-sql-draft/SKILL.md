---
name: warehouse-sql-draft
description: 为模拟 dwd.orders 表生成指定日期、指定字段的 Hive/Spark SQL 查询草稿；适用于学习环境中的简单分区取样查询。
---

# 数仓 SQL 草稿

本技能仅覆盖模拟 dwd.orders 表，字段白名单为 id、amount、dt。dt 为 YYYY-MM-DD 字符串分区，固定 LIMIT 10。复杂聚合、JOIN 或实际集群执行超出本练习范围，应说明限制。

## 工作流程

1. 从用户请求中提取 table、fields、day。缺少任一项时，询问缺失项并等待回复；不猜日期，不默认选择全部字段。
2. 参数齐全时，将对象 JSON 编码后交给本技能目录内 scripts/sql_tool.py 的标准输入。不要将用户原话直接拼接为 shell 命令。可用下方 subprocess 示例，按实际技能目录设置脚本路径。
3. 检查进程退出码和结果 JSON：退出 0 且 ok=true 时，展示 sql，并说明“仅完成输入与模板检查，未在集群执行、未验证业务口径”。退出 2 且 error.code=invalid_input 时，报告错误原因并请用户更正对应参数；不绕过白名单，不反复重试相同请求。其他失败应说明工具异常，不编造 SQL。
4. 用户若要求执行 SQL，说明本练习只提供草稿；不声称已经运行。

## 本地调用示例

在技能目录内运行：

```python
import json
from pathlib import Path
import subprocess
import sys

request = {"table": "dwd.orders", "fields": ["id"], "day": "2026-10-23"}
proc = subprocess.run(
    [sys.executable, str(Path("scripts/sql_tool.py").resolve())],
    input=json.dumps(request), capture_output=True, text=True, timeout=3,
)
print(proc.returncode)
print(proc.stdout, end="")
```
