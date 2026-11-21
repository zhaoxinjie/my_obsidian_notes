import json

KEYS = ("table", "grain", "scope", "metric_version")


def check_comparable(current, baseline):
    for label, stats in (("current", current), ("baseline", baseline)):
        if not isinstance(stats, dict):
            return {"status": "invalid_metadata", "side": label}
        missing = [key for key in KEYS
                   if not isinstance(stats.get(key), str) or not stats[key].strip()]
        if missing:
            return {"status": "invalid_metadata", "side": label, "fields": missing}
    differences = [key for key in KEYS if current[key] != baseline[key]]
    if differences:
        return {"status": "incomparable", "fields": differences}
    return {"status": "comparable"}


if __name__ == "__main__":
    baseline = {"table": "dwd.orders", "grain": "daily",
                "scope": "all_orders", "metric_version": "v1",
                "dt": "2026-11-14", "rows": 1000}
    current = {**baseline, "dt": "2026-11-15", "rows": 700}
    cases = [
        (current, {"status": "comparable"}),
        ({**current, "scope": "paid_only"},
         {"status": "incomparable", "fields": ["scope"]}),
        ({**current, "metric_version": None},
         {"status": "invalid_metadata", "side": "current",
          "fields": ["metric_version"]}),
    ]
    for sample, expected in cases:
        result = check_comparable(sample, baseline)
        assert result == expected, result
        print(json.dumps(result))
