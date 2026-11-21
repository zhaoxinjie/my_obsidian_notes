import json


def lookup_schema(table):
    if table != "dwd.orders":
        return {"ok": False, "error": {"code": "table_not_found"}}
    return {"ok": True, "table": table,
            "columns": [{"name": "id", "type": "bigint"}]}


def dispatch(proposals, max_calls=2, lookup=lookup_schema):
    if (not isinstance(proposals, list) or type(max_calls) is not int
            or not 1 <= max_calls <= 10):
        raise ValueError("调用提议必须是数组，预算必须是 1–10 的整数")
    results = []

    def finish(status, reason):
        return {"status": status, "reason": reason,
                "calls": len(results), "results": results.copy()}

    for proposal in proposals:
        if len(results) >= max_calls:
            return finish("stopped", "call_budget_exceeded")
        if (not isinstance(proposal, dict)
                or set(proposal) != {"tool", "arguments"}):
            return finish("stopped", "invalid_proposal")
        if proposal["tool"] != "get_table_schema":
            return finish("stopped", "unknown_tool")
        args = proposal["arguments"]
        if (not isinstance(args, dict) or set(args) != {"table"}
                or not isinstance(args["table"], str) or not args["table"].strip()):
            return finish("stopped", "invalid_arguments")
        result = lookup(args["table"])
        results.append(result)
        if result.get("ok") is not True:
            return finish("stopped", "lookup_failed")
    return finish("completed", "proposals_consumed")


if __name__ == "__main__":
    call = {"tool": "get_table_schema", "arguments": {"table": "dwd.orders"}}
    cases = [
        ([call], "completed", "proposals_consumed", 1),
        ([call, call, call], "stopped", "call_budget_exceeded", 2),
        ([{"tool": "execute_sql", "arguments": {}}], "stopped", "unknown_tool", 0),
        ([{"tool": "get_table_schema", "arguments": {}}], "stopped", "invalid_arguments", 0),
    ]
    for proposals, status, reason, expected_calls in cases:
        seen = []

        def counted_lookup(table):
            seen.append(table)
            return lookup_schema(table)

        report = dispatch(proposals, lookup=counted_lookup)
        assert (report["status"], report["reason"]) == (status, reason)
        assert report["calls"] == len(seen) == expected_calls
        print(json.dumps({key: report[key] for key in ["status", "reason", "calls"]}))
    print("4 个调用关卡场景通过")
