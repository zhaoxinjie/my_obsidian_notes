import json
import sys
from datetime import date
import re

SCHEMA = {"dwd.orders": {"id", "amount", "dt"}}


def build_sql(table, fields, day):
    if not isinstance(table, str) or table not in SCHEMA:
        raise ValueError("表不在白名单")
    if not isinstance(fields, list) or not fields:
        raise ValueError("fields 必须是非空数组")
    if not all(isinstance(f, str) and f in SCHEMA[table] for f in fields):
        raise ValueError("字段不在白名单")
    if len(set(fields)) != len(fields):
        raise ValueError("字段不能重复")
    if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
        raise ValueError("日期格式必须是 YYYY-MM-DD")
    date.fromisoformat(day)  # 检查日期真实存在，例如拒绝 2026-02-30
    quoted_table = ".".join("`" + part + "`" for part in table.split("."))
    selected = ", ".join("`" + f + "`" for f in fields)
    return (f"SELECT {selected} FROM {quoted_table} "
            f"WHERE `dt` = '{day}' LIMIT 10;")


