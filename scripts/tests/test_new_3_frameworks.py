"""Quick test of the 3 new frameworks."""
from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.aws_strands_agent import AWSStrandsAdapter
from arena.frameworks.crewai_agent import CrewAIAdapter
from arena.frameworks.google_adk_agent import GoogleADKAdapter

frameworks = {
    "AWS Strands": AWSStrandsAdapter,
    "CrewAI": CrewAIAdapter,
    "Google ADK": GoogleADKAdapter,
}

print("\n" + "="*70)
print("QUICK TEST: 3 NEW FRAMEWORKS")
print("="*70 + "\n")

for fw_name, adapter_class in frameworks.items():
    print(f"\n{'='*70}")
    print(f"Testing {fw_name}")
    print(f"{'='*70}")

    try:
        adapter = adapter_class(SYSTEM_PROMPT)
        adapter.start_mcp_server()
        adapter.connect_to_mcp()

        # Test S1 only
        print(f"\nRunning S1 (Damaged laptop refund)...")
        response = adapter.run_agent(SCENARIOS['S1']['user_message'])
        usage = adapter.get_token_usage()
        tools = adapter.get_tool_log()

        print(f"✓ Response length: {len(response)} chars")
        print(f"✓ Input tokens: {usage['input_tokens']}")
        print(f"✓ Output tokens: {usage['output_tokens']}")
        print(f"✓ Cost: ${(usage['input_tokens'] * 3.0 / 1_000_000) + (usage['output_tokens'] * 15.0 / 1_000_000):.4f}")
        print(f"✓ Tools called: {tools if tools else 'None (tracking broken)'}")
        print(f"✓ {fw_name} working!")

        adapter.stop_mcp_server()

    except Exception as e:
        print(f"✗ {fw_name} failed: {str(e)[:100]}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("Test complete!")
print("="*70 + "\n")
