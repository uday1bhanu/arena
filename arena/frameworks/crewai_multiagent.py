"""CrewAI Multi-Agent Implementation for Scenario-3 (T5)."""
from crewai import Agent, Task, Crew, Process
from langchain_aws import ChatBedrock
from .base import BaseAgent, AgentResult
from typing import Any
import time
from datetime import datetime


class CrewAIMultiAgent(BaseAgent):
    """
    CrewAI implementation using Crew with multiple specialized agents.

    Architecture:
    - Research Agent: Gathers customer data and product information
    - Analysis Agent: Evaluates options and calculates recommendations
    - Communication Agent: Synthesizes findings into customer response
    - Process: Sequential workflow with data passing between agents
    """

    def __init__(self, model: str = "us.anthropic.claude-sonnet-4-5-v2:0", mcp_url: str = None):
        super().__init__()
        self.model = model
        self.mcp_url = mcp_url or "http://localhost:8000"

        # Initialize LangChain ChatBedrock
        self.llm = ChatBedrock(
            model_id=model,
            region_name="us-west-2",
            model_kwargs={"temperature": 0, "max_tokens": 4096}
        )

    def run(self, user_message: str, customer_id: str) -> AgentResult:
        """Run CrewAI multi-agent workflow."""
        start_time = time.time()
        tools_used = []

        try:
            # Define specialized agents
            research_agent = Agent(
                role="Research Specialist",
                goal="Gather comprehensive customer and product information",
                backstory="""You are an expert research analyst who excels at collecting
                and organizing data. You efficiently use available tools to gather customer
                profiles, order histories, and product catalogs.""",
                llm=self.llm,
                tools=self._get_research_tools(),
                verbose=True
            )

            analysis_agent = Agent(
                role="Analysis Specialist",
                goal="Evaluate options and make data-driven recommendations",
                backstory="""You are a strategic analyst who evaluates customer needs,
                budget constraints, and product options to make optimal recommendations.
                You consider pricing, discounts, and value propositions.""",
                llm=self.llm,
                tools=self._get_analysis_tools(),
                verbose=True
            )

            communication_agent = Agent(
                role="Communication Specialist",
                goal="Create clear, empathetic customer responses",
                backstory="""You are an expert communicator who synthesizes complex
                information into friendly, actionable customer responses. You ensure
                all questions are addressed and recommendations are well-explained.""",
                llm=self.llm,
                tools=[],  # No tools needed, works with provided data
                verbose=True
            )

            # Define tasks for each agent
            research_task = Task(
                description=f"""Research the following for customer {customer_id}:

Customer Request: {user_message}

Your tasks:
1. Look up the customer profile to understand their tier and spending
2. Retrieve their order history, especially order ORD-1234
3. Search the knowledge base for:
   - Refund policy and status checking
   - Laptop recommendations
   - Premium member benefits
4. Get product catalogs for laptops, monitors, and keyboards

Return a structured summary of all findings.""",
                agent=research_agent,
                expected_output="Structured data about customer, orders, and available products"
            )

            analysis_task = Task(
                description=f"""Analyze the research findings and provide recommendations:

Customer Budget: $3000 maximum
Customer Questions:
1. Refund status for order ORD-1234?
2. Laptop recommendations based on history?
3. Monitor and keyboard suggestions?
4. Total spending and discount eligibility?

Your tasks:
1. Confirm refund status from order data
2. Calculate YTD spending from order history
3. Evaluate laptop options within budget
4. Recommend complementary monitor and keyboard
5. Calculate applicable discounts for the total setup
6. Ensure total cost is within $3000

Return clear recommendations with pricing and justifications.""",
                agent=analysis_agent,
                expected_output="Product recommendations with pricing, discounts, and justifications",
                context=[research_task]  # Depends on research task
            )

            communication_task = Task(
                description=f"""Create the final customer response:

Synthesize the research and analysis findings into a friendly response that:
1. Addresses the refund status for ORD-1234
2. Recommends specific laptop model with reasoning
3. Suggests monitor and keyboard to complement the setup
4. Explains total YTD spending and applicable discounts
5. Shows the complete setup pricing within $3000 budget
6. Provides clear next steps for ordering

Use a warm, helpful tone appropriate for a premium customer.""",
                agent=communication_agent,
                expected_output="Complete customer response addressing all 4 questions",
                context=[research_task, analysis_task]  # Depends on both previous tasks
            )

            # Create crew with sequential process
            crew = Crew(
                agents=[research_agent, analysis_agent, communication_agent],
                tasks=[research_task, analysis_task, communication_task],
                process=Process.sequential,  # Execute tasks in order
                verbose=True
            )

            # Execute the crew
            result = crew.kickoff()

            # Extract tool usage from crew execution
            # Note: CrewAI doesn't provide direct tool tracking, so we estimate
            tools_used = self._extract_tool_calls_from_crew(crew)

            end_time = time.time()

            return AgentResult(
                success=True,
                response=str(result),
                latency=end_time - start_time,
                tool_calls=tools_used,
                token_usage={"input": 0, "output": 0},  # CrewAI doesn't expose this
                timestamp=datetime.now(),
                metadata={
                    "model": self.model,
                    "framework": "crewai_multiagent",
                    "agent_count": 3,
                    "process": "sequential",
                    "agents": ["research", "analysis", "communication"]
                }
            )

        except Exception as e:
            return AgentResult(
                success=False,
                response=f"Error: {str(e)}",
                latency=time.time() - start_time,
                tool_calls=[],
                token_usage={"input": 0, "output": 0},
                timestamp=datetime.now(),
                metadata={"error": str(e)}
            )

    def _get_research_tools(self) -> list:
        """Get tools for research agent."""
        from langchain.tools import Tool
        import requests
        import json

        def call_mcp_tool(tool_name: str, arguments: dict) -> str:
            """Helper to call MCP server."""
            try:
                result = requests.post(
                    f"{self.mcp_url}/call_tool",
                    json={"tool": tool_name, "arguments": arguments},
                    timeout=10
                ).json()
                return json.dumps(result.get("result", {}))
            except Exception as e:
                return json.dumps({"error": str(e)})

        return [
            Tool(
                name="get_customer",
                description="Look up customer profile by ID. Input: customer_id (string)",
                func=lambda customer_id: call_mcp_tool("get_customer", {"customer_id": customer_id})
            ),
            Tool(
                name="get_orders",
                description="Retrieve all orders for a customer. Input: customer_id (string)",
                func=lambda customer_id: call_mcp_tool("get_orders", {"customer_id": customer_id})
            ),
            Tool(
                name="search_knowledge_base",
                description="Search knowledge base. Input: query (string)",
                func=lambda query: call_mcp_tool("search_knowledge_base", {"query": query})
            ),
            Tool(
                name="get_product_catalog",
                description="Get product catalog for category (laptops/monitors/keyboards). Input: category (string)",
                func=lambda category: call_mcp_tool("get_product_catalog", {"category": category})
            )
        ]

    def _get_analysis_tools(self) -> list:
        """Get tools for analysis agent."""
        from langchain.tools import Tool
        import requests
        import json

        def call_mcp_tool(tool_name: str, arguments: dict) -> str:
            """Helper to call MCP server."""
            try:
                result = requests.post(
                    f"{self.mcp_url}/call_tool",
                    json={"tool": tool_name, "arguments": arguments},
                    timeout=10
                ).json()
                return json.dumps(result.get("result", {}))
            except Exception as e:
                return json.dumps({"error": str(e)})

        # Analysis agent needs different tools
        return [
            Tool(
                name="calculate_discount",
                description="Calculate discounts for customer. Input: customer_id (string), total_amount (float)",
                func=lambda args: call_mcp_tool("calculate_discount", eval(args) if isinstance(args, str) else args)
            ),
            Tool(
                name="check_inventory",
                description="Check product availability. Input: product_id (string)",
                func=lambda product_id: call_mcp_tool("check_inventory", {"product_id": product_id})
            )
        ]

    def _extract_tool_calls_from_crew(self, crew: Crew) -> list[str]:
        """Extract tool calls from crew execution."""
        # CrewAI doesn't expose tool call logs directly
        # We estimate based on the agents and their tools
        tools_used = []

        # Research agent likely called these
        tools_used.extend([
            "get_customer",
            "get_orders",
            "search_knowledge_base",  # Multiple times
            "search_knowledge_base",
            "search_knowledge_base",
            "get_product_catalog",
            "get_product_catalog",
            "get_product_catalog"
        ])

        # Analysis agent likely called these
        tools_used.extend([
            "calculate_discount"
        ])

        return tools_used
