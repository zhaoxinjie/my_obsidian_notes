def query_with_retry(query, max_attempts=2):
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError("max_attempts 必须是 1–3 的整数，含首次调用")
    for attempt in range(1, max_attempts + 1):
        try:
            result = query()
        except TimeoutError:
            if attempt == max_attempts:
                return {"status": "stopped", "reason": "timeout_exhausted",
                        "attempts": attempt}
            continue
        if not isinstance(result, dict) or type(result.get("ok")) is not bool:
            return {"status": "stopped", "reason": "invalid_result",
                    "attempts": attempt}
        if result["ok"] is False:
            return {"status": "stopped", "reason": "business_error",
                    "attempts": attempt, "result": result}
        return {"status": "received", "attempts": attempt, "result": result}


def scripted_query(outcomes):
    sequence = iter(outcomes)
    calls = []

    def query():
        calls.append("lookup")
        outcome = next(sequence)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return query, calls


if __name__ == "__main__":
    success = {"ok": True, "table": "dwd.orders",
               "columns": [{"name": "id", "type": "bigint"}]}
    missing = {"ok": False, "error": {"code": "table_not_found"}}
    cases = [
        ("recover", [TimeoutError(), success], "received", 2),
        ("exhaust", [TimeoutError(), TimeoutError()], "stopped", 2),
        ("missing", [missing, success], "stopped", 1),
    ]
    for name, outcomes, status, attempts in cases:
        query, calls = scripted_query(outcomes)
        report = query_with_retry(query)
        assert report["status"] == status
        assert report["attempts"] == len(calls) == attempts
        if name == "exhaust":
            assert report["reason"] == "timeout_exhausted"
        if name == "missing":
            assert report["reason"] == "business_error"
        print(f"{name}: {status}; calls={len(calls)}")
    print("3 个有限重试场景通过")
