import json
import re
from datetime import date


def validate_day(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("分区日期必须为 YYYY-MM-DD")
    date.fromisoformat(value)


def check_partition(target_day, partitions):
    validate_day(target_day)
    if not isinstance(partitions, list):
        raise ValueError("分区清单必须是数组")
    states = {}
    for row in partitions:
        if not isinstance(row, dict) or set(row) != {"dt", "state"}:
            raise ValueError("每项必须包含且仅包含 dt、state")
        dt, state = row["dt"], row["state"]
        validate_day(dt)
        if dt in states:
            raise ValueError("重复分区: " + dt)
        if state not in ("ready", "running", "failed"):
            raise ValueError("未知分区状态")
        states[dt] = state
    state = states.get(target_day, "missing")
    action = {"ready": "continue", "missing": "wait",
              "running": "wait", "failed": "review"}[state]
    return {"target_day": target_day, "state": state, "action": action}


if __name__ == "__main__":
    partitions = [
        {"dt": "2026-11-08", "state": "failed"},
        {"dt": "2026-11-10", "state": "ready"},
        {"dt": "2026-11-11", "state": "running"},
    ]
    cases = [("2026-11-10", "ready", "continue"), ("2026-11-09", "missing", "wait"),
             ("2026-11-11", "running", "wait"), ("2026-11-08", "failed", "review")]
    for day, state, action in cases:
        result = check_partition(day, partitions)
        assert result == {"target_day": day, "state": state, "action": action}
        print(json.dumps(result, ensure_ascii=False))
    print("4 个分区就绪场景通过")
