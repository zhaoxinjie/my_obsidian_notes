import json
from catalog import lookup_schema
from sql_generator import build_sql
from result_policy import decide


def run(request, lookup=lookup_schema, generate=build_sql):
    steps = []

    def finish(status, **detail):
        return {"status": status, "steps": steps.copy(),
                "executed": False, **detail}

    steps.append("validate_request")
    if not isinstance(request, dict):
        return finish("stopped", reason="invalid_request")
    required = {"table", "fields", "day"}
    missing = sorted(required - request.keys())
    if missing:
        return finish("ask_user", missing=missing)
    if set(request) != required:
        return finish("stopped", reason="unexpected_keys")
    table, fields, day = request["table"], request["fields"], request["day"]
    if not isinstance(table, str) or not table.strip():
        return finish("stopped", reason="invalid_table")
    steps.append("lookup_schema")
    try:
        schema = lookup(table)
    except TimeoutError:
        return finish("stopped", reason="lookup_timeout")
    decision = decide({"tool_error": False, "payload": schema}, table)
    if decision["action"] == "ask_user":
        return finish("ask_user", reason="table_not_found")
    if decision["action"] != "continue":
        return finish("stopped", reason=decision["reason"])
    steps.append("validate_fields")
    allowed = {column["name"] for column in schema["columns"]}
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) and f in allowed for f in fields)
            or len(set(fields)) != len(fields)):
        return finish("stopped", reason="invalid_fields")
    steps.append("build_sql")
    try:
        sql = generate(table, fields, day)
    except ValueError as exc:
        return finish("stopped", reason="invalid_sql_request", message=str(exc))
    return finish("needs_review", sql=sql)


