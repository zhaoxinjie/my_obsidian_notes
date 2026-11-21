import json
from datetime import date
import re


def validate_reply(text):
    data = json.loads(text)
    if not isinstance(data, dict) or set(data) != {"status", "request", "questions"}:
        raise ValueError("回答必须且只能包含 status、request、questions")
    questions = data["questions"]
    if (not isinstance(questions, list)
            or not all(isinstance(q, str) and q.strip() for q in questions)):
        raise ValueError("questions 必须是非空白问题组成的数组")
    if data["status"] == "needs_info":
        if data["request"] is not None or not questions:
            raise ValueError("待补充信息时 request 必须为 null，且至少有一个问题")
        return data
    if data["status"] != "ready" or questions:
        raise ValueError("ready 不得带问题，且不支持其他状态")
    request = data["request"]
    if not isinstance(request, dict) or set(request) != {"table", "fields", "day"}:
        raise ValueError("ready 必须提供 table、fields、day")
    if request["table"] != "dwd.orders":
        raise ValueError("表不在教学白名单")
    fields = request["fields"]
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) and f in {"id", "amount", "dt"} for f in fields)
            or len(set(fields)) != len(fields)):
        raise ValueError("字段列表无效")
    day = request["day"]
    if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
        raise ValueError("日期必须为 YYYY-MM-DD")
    date.fromisoformat(day)
    return data


if __name__ == "__main__":
    ready = {"status": "ready", "request": {
        "table": "dwd.orders", "fields": ["id"], "day": "2026-11-07"
    }, "questions": []}
    missing = {"status": "needs_info", "request": None,
               "questions": ["请提供要查询的分区日期。"]}
    for item in [ready, missing]:
        result = validate_reply(json.dumps(item, ensure_ascii=False))
        print("accepted: " + result["status"])
    contradictory = {**ready, "questions": ["请确认日期。"]}
    try:
        validate_reply(json.dumps(contradictory, ensure_ascii=False))
    except ValueError:
        print("rejected: ready_with_questions")
    else:
        raise AssertionError("矛盾回答必须被拒绝")
    print("3 个回答契约场景通过")
