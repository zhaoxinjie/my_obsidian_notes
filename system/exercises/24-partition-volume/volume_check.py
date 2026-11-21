import json


def check_volume(current_rows, baseline_rows, threshold_pct=20):
    if type(threshold_pct) is not int or not 0 <= threshold_pct <= 100:
        raise ValueError("阈值必须是 0–100 的整数百分数")
    for count in (current_rows, baseline_rows):
        if count is not None and (type(count) is not int or count < 0):
            raise ValueError("行数必须是非负整数或 None")
    if current_rows is None or baseline_rows is None:
        return {"status": "insufficient_data", "reason": "missing_count"}
    if baseline_rows == 0:
        return {"status": "insufficient_data", "reason": "zero_baseline"}
    delta = current_rows - baseline_rows
    # abs(delta) / baseline_rows > threshold_pct / 100 的整数比较。
    exceeded = abs(delta) * 100 > baseline_rows * threshold_pct
    return {"status": "review" if exceeded else "pass",
            "delta_rows": delta, "baseline_rows": baseline_rows,
            "threshold_pct": threshold_pct}


if __name__ == "__main__":
    cases = [(1100, 1000, "pass"), (700, 1000, "review"),
             (1200, 1000, "pass"), (None, 1000, "insufficient_data"),
             (100, 0, "insufficient_data")]
    for current, baseline, expected in cases:
        result = check_volume(current, baseline)
        assert result["status"] == expected
        print(json.dumps({"current_rows": current, **result}, ensure_ascii=False))
    print("5 个行数检查场景通过")
