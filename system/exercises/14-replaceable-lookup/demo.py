from workflow import run

REQUEST = {"table": "dwd.orders", "fields": ["id"], "day": "2026-11-02"}


def timeout_lookup(table):
    raise TimeoutError("模拟查询超时")


def broken_lookup(table):
    return {"ok": True}  # 缺少表名和字段


if __name__ == "__main__":
    normal = run(REQUEST)
    assert normal["status"] == "needs_review" and "sql" in normal
    print("normal: " + normal["status"])
    for lookup, expected in [(timeout_lookup, "lookup_timeout"),
                             (broken_lookup, "invalid_result")]:
        calls = []

        def forbidden_generate(*args):
            calls.append(args)
            raise AssertionError("失败后不得调用生成器")

        result = run(REQUEST, lookup=lookup, generate=forbidden_generate)
        assert result["status"] == "stopped"
        assert result["reason"] == expected
        assert "build_sql" not in result["steps"]
        assert "sql" not in result and not calls
        assert result["executed"] is False
        print("failure: " + result["reason"] + "; generate_calls=0")
    print("3 个场景通过")
