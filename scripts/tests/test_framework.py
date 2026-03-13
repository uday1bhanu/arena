"""Test a single framework implementation."""
import os
import sys
import json
import time
import asyncio
from dotenv import load_dotenv

# Load environment
load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.evaluator import evaluate_scenario
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_claude_sdk():
    """Test Claude SDK with MCP."""
    from anthropic import Anthropic

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Start MCP server and get tools
    server_params = StdioServerParameters(
        command="python",
        args=["arena/mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Reset log
            await session.call_tool("arena_reset_log", {})

            # List tools
            tools_result = await session.list_tools()
            mcp_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools_result.tools
                if not tool.name.startswith("arena_")
            ]

            print(f"Available tools: {len(mcp_tools)}")

            # Test S1 scenario
            scenario = SCENARIOS["S1"]
            user_message = scenario["user_message"]

            print(f"\nTesting Scenario S1:")
            print(f"User: {user_message}")

            # Run agent
            messages = [{"role": "user", "content": user_message}]
            total_input = 0
            total_output = 0

            start = time.perf_counter()

            for turn in range(10):  # Max 10 turns
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=messages,
                    tools=mcp_tools,
                    temperature=0
                )

                total_input += response.usage.input_tokens
                total_output += response.usage.output_tokens

                print(f"\n  Turn {turn + 1}: {response.stop_reason}")

                if response.stop_reason == "end_turn":
                    final_text = ""
                    for block in response.content:
                        if block.type == "text":
                            final_text += block.text

                    elapsed = time.perf_counter() - start
                    print(f"\n  Final response: {final_text[:200]}...")
                    print(f"\n  Latency: {elapsed:.2f}s")
                    print(f"  Tokens: {total_input} in / {total_output} out")

                    # Get tool log
                    log_result = await session.call_tool("arena_get_log", {})
                    tool_log = json.loads(log_result.content[0].text)
                    print(f"  Tool calls: {tool_log}")

                    # Evaluate
                    eval_result = evaluate_scenario("S1", tool_log, final_text)
                    print(f"  Correctness: {eval_result['correctness_score']:.2f}")
                    print(f"  Details: {eval_result['correctness_details']}")

                    break

                elif response.stop_reason == "tool_use":
                    # Add assistant message
                    messages.append({"role": "assistant", "content": response.content})

                    # Execute tools
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            print(f"    Tool: {block.name}({block.input})")
                            result = await session.call_tool(block.name, block.input)
                            result_text = result.content[0].text
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result_text
                            })

                    messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("Testing Claude SDK with Arena MCP server\n")
    asyncio.run(test_claude_sdk())
