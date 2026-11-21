import json
from mcp.server.fastmcp import FastMCP
from catalog import lookup_schema

mcp = FastMCP("warehouse-metadata-demo")


@mcp.tool()
def get_table_schema(table: str) -> str:
    """只读查询模拟 Hive 表结构，仅支持 dwd.orders；不执行 SQL。"""
    return json.dumps(lookup_schema(table), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
