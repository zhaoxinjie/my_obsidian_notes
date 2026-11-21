def lookup_schema(table: str) -> dict:
    if table != "dwd.orders":
        return {"ok": False, "error": {"code": "table_not_found"}}
    return {"ok": True, "table": table, "columns": [
        {"name": "id", "type": "bigint"},
        {"name": "amount", "type": "decimal(18,2)"},
        {"name": "dt", "type": "string"}
    ]}
