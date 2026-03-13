"""Test MCP server independently."""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Test that MCP server works."""
    server_params = StdioServerParameters(
        command="python",
        args=["arena/mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools_result = await session.list_tools()
            print(f"Tools available: {len(tools_result.tools)}")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description[:50]}...")

            # Test get_customer
            print("\nTesting get_customer('CUST-001'):")
            result = await session.call_tool("get_customer", {"customer_id": "CUST-001"})
            print(f"  Result: {result.content[0].text[:100]}...")

            # Test arena_get_log
            print("\nTesting arena_get_log():")
            log_result = await session.call_tool("arena_get_log", {})
            tool_log = json.loads(log_result.content[0].text)
            print(f"  Tool log: {tool_log}")

            print("\n✓ MCP server test passed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
