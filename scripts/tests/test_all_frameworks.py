"""Quick test to verify all 6 frameworks can initialize."""
from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.claude_sdk_agent import ClaudeSDKAdapter
from arena.frameworks.langchain_agent import LangChainAdapter
from arena.frameworks.langgraph_agent import LangGraphAdapter
from arena.frameworks.aws_strands_agent import AWSStrandsAdapter
from arena.frameworks.crewai_agent import CrewAIAdapter
from arena.frameworks.google_adk_agent import GoogleADKAdapter

frameworks = {
    "Claude SDK": ClaudeSDKAdapter,
    "LangChain": LangChainAdapter,
    "LangGraph": LangGraphAdapter,
    "AWS Strands": AWSStrandsAdapter,
    "CrewAI": CrewAIAdapter,
    "Google ADK": GoogleADKAdapter,
}

print("\n" + "="*70)
print("FRAMEWORK INITIALIZATION TEST")
print("="*70 + "\n")

for name, adapter_class in frameworks.items():
    try:
        print(f"Testing {name}...", end=" ", flush=True)
        adapter = adapter_class(SYSTEM_PROMPT)
        adapter.start_mcp_server()
        adapter.connect_to_mcp()
        print(f"✓ Initialized")
        adapter.stop_mcp_server()
    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")

print("\n" + "="*70)
print("Test complete!")
print("="*70 + "\n")
