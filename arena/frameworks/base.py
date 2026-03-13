"""Abstract base class for framework adapters."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class FrameworkAdapter(ABC):
    """Abstract base: MCP lifecycle."""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.mcp_process = None
        self._total_input_tokens = 0
        self._total_output_tokens = 0

    @abstractmethod
    def start_mcp_server(self):
        """Start the MCP server as a subprocess (stdio transport)."""
        pass

    @abstractmethod
    def connect_to_mcp(self):
        """Connect to the MCP server and list/filter tools."""
        pass

    @abstractmethod
    def run_agent(self, user_message: str) -> str:
        """Run the agent with the system prompt and user message.

        Returns the final text response from the agent.
        """
        pass

    @abstractmethod
    def get_token_usage(self) -> Dict[str, int]:
        """Return cumulative token usage after a run.

        Returns:
            {"input_tokens": int, "output_tokens": int}
        """
        pass

    def get_tool_log(self, mcp_client) -> list[str]:
        """Call arena_get_log via the MCP client to retrieve the tool call sequence."""
        result = mcp_client.call_tool("arena_get_log", {})
        import json
        return json.loads(result.content[0].text)

    def reset_tool_log(self, mcp_client):
        """Call arena_reset_log to clear the tool call log."""
        mcp_client.call_tool("arena_reset_log", {})

    def stop_mcp_server(self):
        """Stop the MCP server subprocess."""
        if self.mcp_process:
            self.mcp_process.terminate()
            self.mcp_process.wait()
            self.mcp_process = None
