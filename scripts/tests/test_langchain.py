"""Test LangChain adapter."""
import os
os.environ["AWS_PROFILE"] = "prod-tools"

from dotenv import load_dotenv
load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.langchain_agent import LangChainAdapter
from arena.evaluator import evaluate_scenario


def test_scenario(scenario_id: str):
    """Test one scenario."""
    print(f"\n{'='*60}")
    print(f"Testing Scenario {scenario_id} with LangChain")
    print(f"{'='*60}")

    scenario = SCENARIOS[scenario_id]
    adapter = LangChainAdapter(SYSTEM_PROMPT)

    print("Starting agent...")
    adapter.start_mcp_server()
    adapter.connect_to_mcp()

    print(f"User: {scenario['user_message']}\n")
    print("Running...")

    final_response = adapter.run_agent(scenario["user_message"])

    print(f"\n✓ Complete")
    print(f"Response: {final_response[:200]}...")

    usage = adapter.get_token_usage()
    print(f"Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out")

    tool_log = adapter.get_tool_log()
    print(f"Tool calls: {tool_log}")

    eval_result = evaluate_scenario(scenario_id, tool_log, final_response)
    print(f"Correctness: {eval_result['correctness_score']:.2f}")

    adapter.stop_mcp_server()


if __name__ == "__main__":
    test_scenario("S1")
