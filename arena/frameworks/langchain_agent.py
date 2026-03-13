"""LangChain framework adapter."""
import os
import asyncio
import json
import boto3
from arena.frameworks.base import FrameworkAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class LangChainAdapter(FrameworkAdapter):
    """LangChain with Bedrock Claude and manual MCP integration."""

    def __init__(self, system_prompt: str):
        super().__init__(system_prompt)
        self.server_params = None
        self.tools = []
        self.tool_log = []

    def start_mcp_server(self):
        """MCP server setup."""
        self.server_params = StdioServerParameters(
            command="python",
            args=["arena/mcp_server.py"],
            env=None
        )

    def connect_to_mcp(self):
        """Connect and load MCP tools."""
        async def _get_tools():
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()

                    tools = []
                    for tool_def in tools_result.tools:
                        if not tool_def.name.startswith("arena_"):
                            tools.append({
                                "name": tool_def.name,
                                "description": tool_def.description,
                                "parameters": tool_def.inputSchema
                            })
                    return tools

        self.tools = asyncio.run(_get_tools())

    def run_agent(self, user_message: str) -> str:
        """Run LangChain agent."""
        return asyncio.run(self._run_agent_async(user_message))

    async def _run_agent_async(self, user_message: str) -> str:
        """Async agent execution."""
        from langchain_aws import ChatBedrock
        from langchain_core.tools import StructuredTool
        from langchain_core.messages import HumanMessage
        from langgraph.prebuilt import create_react_agent

        # Reset MCP log
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                await session.call_tool("arena_reset_log", {})

        # Create tool calling function
        async def call_mcp_tool(tool_name: str, **kwargs):
            """Call MCP tool."""
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, kwargs)
                    return result.content[0].text

        # Convert MCP tools to LangChain tools
        lc_tools = []
        for tool_def in self.tools:
            tool_name = tool_def["name"]

            # Create sync wrapper
            def make_tool_func(tn):
                def tool_func(**kwargs):
                    return asyncio.run(call_mcp_tool(tn, **kwargs))
                return tool_func

            lc_tool = StructuredTool.from_function(
                func=make_tool_func(tool_name),
                name=tool_name,
                description=tool_def["description"]
            )
            lc_tools.append(lc_tool)

        # Create Bedrock LLM
        llm = ChatBedrock(
            model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            credentials_profile_name=os.getenv("AWS_PROFILE", "prod-tools"),
            model_kwargs={"temperature": 0}
        )

        # Create agent using LangGraph's create_react_agent
        agent = create_react_agent(
            llm,
            lc_tools,
            prompt=self.system_prompt
        )

        # Run agent
        try:
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content=user_message)]}
            )

            # Extract response from messages
            response_text = ""
            messages = result.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    response_text = last_message.content
                else:
                    response_text = str(last_message)

            # Get tool log
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    log_result = await session.call_tool("arena_get_log", {})
                    self.tool_log = json.loads(log_result.content[0].text)

            # Extract token usage from all AI messages in the result
            total_input = 0
            total_output = 0
            for msg in messages:
                if hasattr(msg, 'response_metadata'):
                    metadata = msg.response_metadata
                    if 'usage' in metadata:
                        usage = metadata['usage']
                        # Bedrock uses prompt_tokens and completion_tokens
                        total_input += usage.get('prompt_tokens', 0)
                        total_output += usage.get('completion_tokens', 0)

            # Store tokens
            self._total_input_tokens = total_input
            self._total_output_tokens = total_output

            return response_text

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"[Error: {str(e)}]"

    def get_token_usage(self) -> dict:
        """Return token usage."""
        return {
            "input_tokens": self._total_input_tokens,
            "output_tokens": self._total_output_tokens,
        }

    def get_tool_log(self) -> list:
        """Return tool log."""
        return self.tool_log
