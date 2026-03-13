"""Test CrewAI with S1 scenario."""
from dotenv import load_dotenv
load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.crewai_agent import CrewAIAdapter

# Test scenario S1
scenario = SCENARIOS["S1"]
print(f"Testing CrewAI with scenario: {scenario['user_message']}")
print(f"Expected tools: {scenario['expected_tools']}")
print()

adapter = CrewAIAdapter(SYSTEM_PROMPT)
adapter.start_mcp_server()
adapter.connect_to_mcp()

print("Running agent...")
response = adapter.run_agent(scenario["user_message"])

print(f"\nResponse: {response}")
print(f"\nTool log: {adapter.get_tool_log()}")
print(f"\nToken usage: {adapter.get_token_usage()}")

adapter.stop_mcp_server()
