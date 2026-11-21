class Budget:
    def __init__(self, total):
        if type(total) is not int or not 0 <= total <= 10:
            raise ValueError("总预算必须是 0–10 的整数")
        self.remaining = total

    def take(self):
        if self.remaining == 0:
            return False
        self.remaining -= 1
        return True


def query_with_retry(query, budget, max_attempts=2):
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError("尝试上限必须是 1–3 的整数")
    attempts = 0
    while attempts < max_attempts:
        if not budget.take():
            return {"status": "budget_exhausted", "attempts": attempts}
        attempts += 1  # 首次、重试、超时都计入实际调用预算
        try:
            result = query()
        except TimeoutError:
            continue
        if not isinstance(result, dict) or type(result.get("ok")) is not bool:
            return {"status": "invalid_result", "attempts": attempts}
        if result["ok"] is False:
            return {"status": "business_error", "attempts": attempts}
        return {"status": "received", "attempts": attempts}
    return {"status": "timeout_exhausted", "attempts": attempts}


if __name__ == "__main__":
    budget = Budget(3)  # 本次工作流只创建一次，由所有查询共享
    outcomes = iter([TimeoutError(), {"ok": True}, TimeoutError(), {"ok": True}])
    calls = []

    def lookup():
        calls.append("lookup")
        outcome = next(outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    first = query_with_retry(lookup, budget)
    assert first == {"status": "received", "attempts": 2}
    print(f"first: {first['status']}; attempts={first['attempts']}; remaining={budget.remaining}")
    second = query_with_retry(lookup, budget)
    assert second == {"status": "budget_exhausted", "attempts": 1}
    print(f"second: {second['status']}; attempts={second['attempts']}; remaining={budget.remaining}")
    third = query_with_retry(lookup, budget)
    assert third == {"status": "budget_exhausted", "attempts": 0}
    assert len(calls) == 3 and budget.remaining == 0
    print(f"third: {third['status']}; attempts={third['attempts']}; actual_calls={len(calls)}")
    print("共享预算场景通过；第 4 个模拟结果未被读取")
