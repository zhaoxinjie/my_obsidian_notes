import json
from pathlib import Path
from validate_reply import validate_reply


def load_cases(path):
    cases, seen = [], set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except ValueError as exc:
            raise ValueError(f"案例文件第 {line_number} 行不是合法 JSON") from exc
        if not isinstance(case, dict) or set(case) != {"id", "expected", "reply"}:
            raise ValueError(f"第 {line_number} 行案例字段错误")
        key = case["id"]
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError(f"第 {line_number} 行案例 id 无效或重复")
        if case["expected"] not in ("accept", "reject") or not isinstance(case["reply"], str):
            raise ValueError(f"第 {line_number} 行标签或 reply 类型错误")
        seen.add(key)
        cases.append(case)
    if not cases:
        raise ValueError("案例文件为空")
    return cases


def replay(cases):
    failures = []
    for case in cases:
        try:
            validate_reply(case["reply"])
            actual = "accept"
        except ValueError:
            actual = "reject"
        if actual != case["expected"]:
            failures.append({"id": case["id"], "expected": case["expected"], "actual": actual})
    return {"total": len(cases), "passed": len(cases) - len(failures), "failures": failures}


if __name__ == "__main__":
    cases = load_cases(Path(__file__).with_name("cases.jsonl"))
    report = replay(cases)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report["failures"] else 0)
