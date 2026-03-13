"""Test Claude SDK adapter end-to-end."""
import json
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.claude_sdk_agent import ClaudeSDKAdapter
from arena.evaluator import evaluate_scenario


async def get_tool_log():
    """Get tool log from MCP server."""
    server_params = StdioServerParameters(
        command="python",
        args=["arena/mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("arena_get_log", {})
            return json.loads(result.content[0].text)


def test_scenario(scenario_id: str):
    """Test one scenario."""
    print(f"\n{'='*60}")
    print(f"Testing Scenario {scenario_id}")
    print(f"{'='*60}")

    scenario = SCENARIOS[scenario_id]
    adapter = ClaudeSDKAdapter(SYSTEM_PROMPT)

    print("Connecting to MCP server...")
    adapter.start_mcp_server()
    adapter.connect_to_mcp()
    print(f"✓ Connected, {len(adapter.mcp_tools)} tools available")

    print(f"\nUser message: {scenario['user_message']}")
    print("\nRunning agent...")

    final_response = adapter.run_agent(scenario["user_message"])

    print(f"\n✓ Agent complete")
    print(f"  Response: {final_response[:200]}...")

    # Get token usage
    usage = adapter.get_token_usage()
    print(f"  Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out")

    # Get tool log from adapter
    tool_log = adapter.get_tool_log()
    print(f"  Tool calls: {tool_log}")

    # Evaluate
    eval_result = evaluate_scenario(scenario_id, tool_log, final_response)
    print(f"  Correctness: {eval_result['correctness_score']:.2f}")
    print(f"  Details: {json.dumps(eval_result['correctness_details'], indent=4)}")

    adapter.stop_mcp_server()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Claude SDK Adapter Test")
    print("="*60)

    # Test all scenarios
    test_scenario("S1")
    test_scenario("S2")
    test_scenario("S3")
