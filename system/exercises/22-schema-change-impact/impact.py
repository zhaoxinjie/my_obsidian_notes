import json


def impact(old, new, jobs):
    for schema in (old, new):
        if not isinstance(schema, dict) or not all(
            isinstance(k, str) and k.strip() and isinstance(v, str) and v.strip()
            for k, v in schema.items()
        ):
            raise ValueError("表结构必须是字段名到非空类型字符串的字典")
    if not isinstance(jobs, list):
        raise ValueError("任务依赖必须是数组")
    changes = {name: "removed" for name in old.keys() - new.keys()}
    changes.update({name: "type_changed" for name in old.keys() & new.keys()
                    if old[name] != new[name]})
    seen, affected = set(), []
    for job in jobs:
        if not isinstance(job, dict) or set(job) != {"name", "fields"}:
            raise ValueError("任务必须包含且仅包含 name、fields")
        name, fields = job["name"], job["fields"]
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("任务名称无效或重复")
        seen.add(name)
        if (not isinstance(fields, list) or not fields
                or not all(isinstance(f, str) and f in old for f in fields)
                or len(set(fields)) != len(fields)):
            raise ValueError("依赖字段必须唯一、非空且存在于旧结构")
        hits = [{"field": field, "reason": changes[field]}
                for field in sorted(fields) if field in changes]
        if hits:
            affected.append({"job": name, "review": hits})
    return {"affected": sorted(affected, key=lambda item: item["job"]),
            "unaffected_by_declared_fields": len(jobs) - len(affected)}


if __name__ == "__main__":
    old = {"id": "bigint", "amount": "int", "legacy": "string"}
    new = {"id": "bigint", "amount": "bigint", "channel": "string"}
    jobs = [
        {"name": "daily_amount", "fields": ["id", "amount"]},
        {"name": "old_export", "fields": ["legacy"]},
        {"name": "id_only", "fields": ["id"]},
    ]
    report = impact(old, new, jobs)
    assert [item["job"] for item in report["affected"]] == ["daily_amount", "old_export"]
    assert report["unaffected_by_declared_fields"] == 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
