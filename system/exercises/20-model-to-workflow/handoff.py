import json
from validate_reply import validate_reply
from workflow import run


def handoff(reply_text, confirmed_request, workflow=run):
    try:
        reply = validate_reply(reply_text)
    except ValueError:
        return {"status": "stopped", "reason": "invalid_model_reply", "executed": False}
    if reply["status"] == "needs_info":
        return {"status": "ask_user", "questions": reply["questions"], "executed": False}
    if not isinstance(confirmed_request, dict) or reply["request"] != confirmed_request:
        return {"status": "stopped", "reason": "request_mismatch", "executed": False}
    return workflow(reply["request"])


if __name__ == "__main__":
    # 模拟从用户确认界面取得的参数；不能从同一份模型回答生成。
    confirmed = {"table": "dwd.orders", "fields": ["id"], "day": "2026-11-08"}
    ready = {"status": "ready", "request": confirmed.copy(), "questions": []}
    missing = {"status": "needs_info", "request": None,
               "questions": ["请确认查询日期。"]}
    changed = {"status": "ready", "request": {**confirmed, "day": "2026-11-07"},
               "questions": []}
    cases = [
        ("matched", json.dumps(ready), "needs_review", 1),
        ("missing", json.dumps(missing), "ask_user", 0),
        ("changed", json.dumps(changed), "stopped", 0),
        ("broken", "{", "stopped", 0),
    ]
    for name, text, expected, expected_calls in cases:
        calls = []

        def counted_workflow(request):
            calls.append(request)
            return run(request)

        result = handoff(text, confirmed, workflow=counted_workflow)
        assert result["status"] == expected
        assert result["executed"] is False
        assert len(calls) == expected_calls
        if name == "matched":
            assert "2026-11-08" in result["sql"]
        else:
            assert "sql" not in result
        print(f"{name}: {result['status']}; workflow_calls={len(calls)}")
    print("4 个回答交接场景通过；未执行 SQL")
