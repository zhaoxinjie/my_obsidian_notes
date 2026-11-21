import asyncio
import json
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("server.py").resolve())],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert [t.name for t in tools.tools] == ["get_table_schema"]
            print("工具发现通过")
            for table in ["dwd.orders", "unknown.table"]:
                result = await session.call_tool(
                    "get_table_schema", arguments={"table": table}
                )
                assert not result.isError
                payload = json.loads(result.content[0].text)
                if table == "dwd.orders":
                    assert payload == {"ok": True, "table": table, "columns": [
                        {"name": "id", "type": "bigint"},
                        {"name": "amount", "type": "decimal(18,2)"},
                        {"name": "dt", "type": "string"}
                    ]}
                else:
                    assert payload == {"ok": False, "error": {
                        "code": "table_not_found"
                    }}
                print(json.dumps(payload, ensure_ascii=False))
            print("2 个 MCP 调用场景通过")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=15))
