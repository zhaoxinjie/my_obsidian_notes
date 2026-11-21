import json
from policy import decide

CASES = [
    {"id": "valid_schema", "expected": "continue", "input": {
        "tool_error": False, "payload": {"ok": True, "table": "dwd.orders",
        "columns": [{"name": "id", "type": "bigint"}]}}},
    {"id": "missing_table", "expected": "ask_user", "input": {
        "tool_error": False, "payload": {"ok": False,
        "error": {"code": "table_not_found"}}}},
    {"id": "tool_failure", "expected": "stop", "input": {
        "tool_error": True, "payload": None}},
    {"id": "broken_payload", "expected": "stop", "input": {
        "tool_error": False, "payload": {}}},
]


def evaluate(cases, policy):
    if not cases:
        raise ValueError("评测集不能为空")
    passed, unsafe_continue, failures = 0, 0, []
    for case in cases:
        actual = policy(case["input"])["action"]
        if actual == case["expected"]:
            passed += 1
        else:
            failures.append({"id": case["id"], "expected": case["expected"],
                             "actual": actual})
        if actual == "continue" and case["expected"] != "continue":
            unsafe_continue += 1
    return {"total": len(cases), "passed": passed,
            "unsafe_continue": unsafe_continue, "failures": failures}


if __name__ == "__main__":
    report = evaluate(CASES, decide)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] == report["total"] else 1)
