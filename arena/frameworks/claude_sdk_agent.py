"""Claude SDK framework adapter using claude-agent-sdk-python."""
import os
import asyncio
from arena.frameworks.base import FrameworkAdapter

# Set Bedrock environment variables
os.environ["AWS_PROFILE"] = os.getenv("AWS_PROFILE", "prod-tools")
os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"

from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ResultMessage


class ClaudeSDKAdapter(FrameworkAdapter):
    """Claude Agent SDK with Bedrock configuration."""

    def __init__(self, system_prompt: str):
        super().__init__(system_prompt)
        self.tool_log = []

    def start_mcp_server(self):
        """MCP server will be started by Claude Agent SDK."""
        pass

    def connect_to_mcp(self):
        """Connection handled by Claude Agent SDK."""
        pass

    def run_agent(self, user_message: str) -> str:
        """Run agent using Claude Agent SDK."""
        return asyncio.run(self._run_agent_async(user_message))

    async def _run_agent_async(self, user_message: str) -> str:
        """Async agent execution."""
        # Configure MCP server (use v2 for extended tools)
        mcp_servers = {
            "arena": {
                "type": "stdio",
                "command": "python",
                "args": ["-m", "arena.mcp_server_v2"]
            }
        }

        options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            mcp_servers=mcp_servers,
            permission_mode="bypassPermissions",  # Auto-allow tools
            max_turns=20
        )

        # Reset tracking
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self.tool_log = []
        response_text = ""

        try:
            async for event in query(prompt=user_message, options=options):
                # Handle AssistantMessage
                if isinstance(event, AssistantMessage):
                    # Extract content - it's directly on the event
                    content = event.content if hasattr(event, 'content') else []

                    for block in content:
                        block_type = type(block).__name__

                        # Handle TextBlock
                        if block_type == "TextBlock":
                            response_text += block.text

                        # Track ToolUseBlock
                        elif block_type == "ToolUseBlock":
                            tool_name = block.name

                            # Strip mcp__arena__ prefix if present
                            if tool_name.startswith("mcp__arena__"):
                                tool_name = tool_name.replace("mcp__arena__", "")

                            # Skip internal tools and admin tools
                            if tool_name not in ["ToolSearch"] and not tool_name.startswith("arena_"):
                                self.tool_log.append(tool_name)

                # Handle ResultMessage for token counting
                elif isinstance(event, ResultMessage):
                    if hasattr(event, 'usage') and isinstance(event.usage, dict):
                        usage = event.usage
                        self._total_input_tokens = usage.get('input_tokens', 0)
                        self._total_output_tokens = usage.get('output_tokens', 0)

        except Exception as e:
            # Fallback on error
            response_text = f"[Error: {str(e)}]"

        return response_text

    def get_token_usage(self) -> dict:
        """Return token usage."""
        return {
            "input_tokens": self._total_input_tokens,
            "output_tokens": self._total_output_tokens,
        }

    def get_tool_log(self) -> list:
        """Return tool call log."""
        return self.tool_log
