"""Simple test of Claude Agent SDK with MCP."""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Set environment for Bedrock
os.environ["AWS_PROFILE"] = "prod-tools"
os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"

from claude_agent_sdk import query, ClaudeAgentOptions


async def test_simple():
    """Test with simple prompt."""

    # Configure MCP server
    mcp_servers = {
        "arena": {
            "type": "stdio",
            "command": "python",
            "args": ["arena/mcp_server.py"]
        }
    }

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant.",
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions",
        max_turns=5
    )

    prompt = "Use the get_customer tool to look up customer CUST-001"

    print(f"Prompt: {prompt}\n")

    # Collect all events
    events = []
    async for event in query(prompt=prompt, options=options):
        events.append(event)
        print(f"Event type: {type(event).__name__}")
        print(f"  {event}\n")

    print(f"\nTotal events: {len(events)}")


if __name__ == "__main__":
    asyncio.run(test_simple())
