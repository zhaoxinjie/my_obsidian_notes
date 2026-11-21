import json
from uuid import uuid4


def trace_lookup(table):
    run_id = uuid4().hex
    events = []

    def emit(step, status, detail):
        events.append({"run_id": run_id, "seq": len(events) + 1,
                       "step": step, "status": status, "detail": detail})

    if not isinstance(table, str) or not table.strip():
        emit("workflow", "stopped", {"reason": "invalid_table"})
        return events
    emit("schema_lookup", "started", {"table": table})
    if table != "dwd.orders":
        emit("schema_lookup", "failed", {"code": "table_not_found"})
        emit("workflow", "stopped", {"reason": "confirm_table"})
        return events
    # 模拟只读工具调用成功；摘要不代表真实集群查询结果。
    emit("schema_lookup", "succeeded", {"column_count": 3})
    emit("workflow", "paused", {"reason": "awaiting_next_step"})
    return events


if __name__ == "__main__":
    for table in ["dwd.orders", "unknown.table"]:
        events = trace_lookup(table)
        for event in events:
            print(json.dumps(event, ensure_ascii=False))
