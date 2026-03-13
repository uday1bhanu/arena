"""Test Claude Agent SDK with MCP server."""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Set environment for Bedrock
os.environ["AWS_PROFILE"] = "prod-tools"
os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"

from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, UserMessage, ResultMessage


async def test_agent_sdk():
    """Test basic query with MCP server."""

    # Configure MCP server
    mcp_servers = {
        "arena": {
            "type": "stdio",
            "command": "python",
            "args": ["arena/mcp_server.py"]
        }
    }

    options = ClaudeAgentOptions(
        system_prompt="You are a customer support agent for TechCorp.",
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions",  # Auto-allow tools
        max_turns=10
    )

    prompt = "Hi, this is customer CUST-001. I ordered a laptop 3 days ago and it arrived damaged. Order #ORD-1234. I want a refund."

    print(f"Prompt: {prompt}\n")
    print("Running agent with MCP tools...\n")

    response_text = ""
    tool_calls = []

    async for event in query(prompt=prompt, options=options):
        # Handle different event types
        if isinstance(event, AssistantMessage):
            print(f"[Assistant Message]")
            for block in event["message"]["content"]:
                if hasattr(block, "type"):
                    if block.type == "text":
                        response_text += block.text
                        print(f"  Text: {block.text[:100]}...")
                    elif block.type == "tool_use":
                        tool_calls.append(block.name)
                        print(f"  Tool: {block.name}({block.input})")

        elif isinstance(event, ResultMessage):
            print(f"[Result Complete]")
            if hasattr(event, "usage"):
                print(f"  Tokens: {event.usage}")

        elif isinstance(event, UserMessage):
            print(f"[User Message]")

    print(f"\nTool calls made: {tool_calls}")
    print(f"\nFinal response:\n{response_text}")


if __name__ == "__main__":
    asyncio.run(test_agent_sdk())
