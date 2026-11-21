import hashlib


def fingerprint(sql):
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL 必须是非空字符串")
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()


def review_gate(sql, approval=None):
    try:
        current = fingerprint(sql)
    except ValueError:
        return {"status": "invalid_input", "executed": False}
    if approval is None:
        return {"status": "needs_review", "sql_sha256": current,
                "executed": False}
    if (not isinstance(approval, dict)
            or type(approval.get("approved")) is not bool
            or not isinstance(approval.get("sql_sha256"), str)):
        return {"status": "invalid_approval", "executed": False}
    if approval["approved"] is False:
        return {"status": "rejected", "executed": False}
    if approval["sql_sha256"] != current:
        return {"status": "stale_approval", "executed": False}
    return {"status": "review_matched", "sql_sha256": current,
            "executed": False}


if __name__ == "__main__":
    sql = "SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-29' LIMIT 10;"
    card = review_gate(sql)
    # 模拟人工查看 SQL 后留下审核结果；此处不是实际用户授权。
    approval = {"approved": True, "sql_sha256": card["sql_sha256"]}
    cases = [
        (sql, None, "needs_review"),
        (sql, approval, "review_matched"),
        (sql.replace("LIMIT 10", "LIMIT 100"), approval, "stale_approval"),
        (sql, {"approved": False, "sql_sha256": card["sql_sha256"]}, "rejected"),
    ]
    for text, audit, expected in cases:
        result = review_gate(text, audit)
        assert result["status"] == expected
        assert result["executed"] is False
        print(result["status"])
    print("4 个基础场景通过；未执行 SQL")
