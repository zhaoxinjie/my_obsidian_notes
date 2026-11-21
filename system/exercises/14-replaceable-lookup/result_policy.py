def decide(result, expected_table="dwd.orders"):
    stop = {"action": "stop", "reason": "invalid_result"}
    if not isinstance(result, dict) or type(result.get("tool_error")) is not bool:
        return stop
    if result["tool_error"]:
        return {"action": "stop", "reason": "tool_failure"}
    payload = result.get("payload")
    if not isinstance(payload, dict):
        return stop
    if payload.get("ok") is False:
        error = payload.get("error")
        if isinstance(error, dict) and error.get("code") == "table_not_found":
            return {"action": "ask_user", "reason": "confirm_table"}
        return {"action": "stop", "reason": "unknown_business_error"}
    if payload.get("ok") is not True or payload.get("table") != expected_table:
        return stop
    columns = payload.get("columns")
    if not isinstance(columns, list) or not columns:
        return stop
    names = set()
    for column in columns:
        if not isinstance(column, dict):
            return stop
        name, kind = column.get("name"), column.get("type")
        if not all(isinstance(x, str) and x.strip() for x in (name, kind)):
            return stop
        key = name.strip().lower()
        if key in names:
            return stop
        names.add(key)
    return {"action": "continue", "reason": "schema_received"}


