import json

# 教学快照，金额单位与日期口径仅对本例有效。
CATALOG = {
    "table": "dwd.orders",
    "source": "mock://catalog/orders/v1",
    "snapshot_date": "2026-11-07",
    "columns": {
        "id": {"type": "bigint", "comment": "订单唯一编号"},
        "amount": {"type": "decimal(18,2)", "comment": "订单金额，单位元"},
        "dt": {"type": "string", "comment": "分区日期，格式 YYYY-MM-DD"},
    },
}


def build_context(table, fields):
    if not isinstance(table, str) or table != CATALOG["table"]:
        raise ValueError("unknown_table")
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) for f in fields)):
        raise ValueError("invalid_fields")
    if len(set(fields)) != len(fields):
        raise ValueError("duplicate_fields")
    missing = sorted(set(fields) - CATALOG["columns"].keys())
    if missing:
        raise ValueError("unknown_fields: " + ", ".join(missing))
    return {
        "table": table,
        "source": CATALOG["source"],
        "snapshot_date": CATALOG["snapshot_date"],
        "columns": [{"name": field, **CATALOG["columns"][field]}
                    for field in fields],
    }


if __name__ == "__main__":
    context = build_context("dwd.orders", ["amount", "dt"])
    assert [c["name"] for c in context["columns"]] == ["amount", "dt"]
    assert context["source"] == "mock://catalog/orders/v1"
    print(json.dumps(context, ensure_ascii=False, indent=2))
    try:
        build_context("dwd.orders", ["gmv"])
    except ValueError as exc:
        assert str(exc) == "unknown_fields: gmv"
        print("未知字段自测通过；未猜测 gmv 与 amount 的映射")
    else:
        raise AssertionError("未知字段必须失败")
