import json
from pathlib import Path
import subprocess
import sys
import unittest

TOOL = Path(__file__).with_name("sql_tool.py")


class SqlToolTests(unittest.TestCase):
    def call_tool(self, text):
        proc = subprocess.run(
            [sys.executable, str(TOOL)], input=text,
            capture_output=True, text=True, timeout=3,
        )
        self.assertEqual(proc.stderr, "")
        self.assertEqual(len(proc.stdout.splitlines()), 1)
        return proc.returncode, json.loads(proc.stdout)

    def test_success(self):
        code, result = self.call_tool(json.dumps({
            "table": "dwd.orders", "fields": ["id"], "day": "2026-10-20"
        }))
        self.assertEqual(code, 0)
        self.assertEqual(result, {
            "ok": True,
            "sql": "SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-20' LIMIT 10;"
        })

    def test_unknown_field(self):
        code, result = self.call_tool(json.dumps({
            "table": "dwd.orders", "fields": ["unknown"], "day": "2026-10-20"
        }))
        self.assertEqual(code, 2)
        self.assertIs(result["ok"], False)
        self.assertEqual(result["error"]["code"], "invalid_input")
        self.assertNotIn("sql", result)

    def test_malformed_json(self):
        code, result = self.call_tool("{")
        self.assertEqual(code, 2)
        self.assertIs(result["ok"], False)
        self.assertEqual(result["error"]["code"], "invalid_input")
        self.assertNotIn("sql", result)


if __name__ == "__main__":
    unittest.main()
