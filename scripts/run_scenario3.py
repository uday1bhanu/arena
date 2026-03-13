#!/usr/bin/env python3
"""
Run Scenario-3 (T5) - Multi-Agent Product Investigation & Recommendation

This script tests all 4 frameworks on the complex multi-agent scenario
where multiple specialized agents must collaborate to handle a customer's
request for product recommendations.

Usage:
    python scripts/run_scenario3.py 1  # Run iteration 1
    python scripts/run_scenario3.py 2  # Run iteration 2
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from arena.scenarios import SCENARIOS
from arena.evaluator import evaluate_scenario
from arena.frameworks.claude_sdk_multiagent import ClaudeSDKMultiAgent
from arena.frameworks.crewai_multiagent import CrewAIMultiAgent
from arena.frameworks.google_adk_multiagent import GoogleADKMultiAgent
from arena.frameworks.aws_strands_multiagent import AWSStrandsMultiAgent


def run_framework(framework_name: str, framework_class, scenario_name: str, run_number: int):
    """Run a single framework on the scenario."""
    print(f"\n{'='*80}")
    print(f"Framework: {framework_name} | Scenario: {scenario_name} | Run: {run_number}")
    print(f"{'='*80}")

    scenario = SCENARIOS[scenario_name]
    agent = framework_class()

    try:
        # Run the agent
        result = agent.run(
            user_message=scenario["user_message"],
            customer_id=scenario["customer_id"]
        )

        # Evaluate correctness
        correctness_score, criteria_results = evaluate_scenario(
            scenario_name=scenario_name,
            tool_log=result.tool_calls,
            final_response=result.response
        )

        # Print results
        print(f"\n✅ Success!")
        print(f"Correctness: {correctness_score:.1f}%")
        print(f"Latency: {result.latency:.2f}s")
        print(f"Tool Calls: {len(result.tool_calls)}")
        print(f"Tools Used: {', '.join(set(result.tool_calls))}")

        # Save results
        output_dir = Path(f"scenarios/scenario-3/iterations/iteration-{run_number}")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{framework_name.lower().replace(' ', '_')}_t5_r{run_number}.json"
        output_data = {
            "framework": framework_name,
            "scenario": scenario_name,
            "run_number": run_number,
            "timestamp": result.timestamp.isoformat(),
            "correctness_score": correctness_score,
            "latency": result.latency,
            "tool_calls": result.tool_calls,
            "tool_count": len(result.tool_calls),
            "unique_tools": list(set(result.tool_calls)),
            "token_usage": result.token_usage,
            "criteria_results": criteria_results,
            "response": result.response,
            "metadata": result.metadata
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"Results saved to: {output_file}")

        return {
            "framework": framework_name,
            "correctness": correctness_score,
            "latency": result.latency,
            "tool_calls": len(result.tool_calls),
            "success": True
        }

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "framework": framework_name,
            "correctness": 0.0,
            "latency": 0.0,
            "tool_calls": 0,
            "success": False,
            "error": str(e)
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_scenario3.py <iteration_number>")
        print("Example: python scripts/run_scenario3.py 1")
        sys.exit(1)

    iteration = int(sys.argv[1])
    scenario_name = "T5"
    repetitions = 3  # Run each framework 3 times

    print("="*80)
    print(f"SCENARIO-3 BENCHMARK - ITERATION {iteration}")
    print(f"Scenario: {scenario_name} (Multi-Agent Product Investigation)")
    print(f"Repetitions: {repetitions} per framework")
    print(f"Total Runs: {4 * repetitions} (4 frameworks × {repetitions} runs)")
    print("="*80)

    frameworks = [
        ("Claude SDK (Multi-Agent)", ClaudeSDKMultiAgent),
        ("CrewAI (Multi-Agent)", CrewAIMultiAgent),
        ("Google ADK (Multi-Agent)", GoogleADKMultiAgent),
        ("AWS Strands (Multi-Agent)", AWSStrandsMultiAgent)
    ]

    all_results = []
    start_time = time.time()

    for rep in range(1, repetitions + 1):
        print(f"\n\n{'#'*80}")
        print(f"REPETITION {rep}/{repetitions}")
        print(f"{'#'*80}")

        for framework_name, framework_class in frameworks:
            result = run_framework(framework_name, framework_class, scenario_name, iteration)
            result["repetition"] = rep
            all_results.append(result)

            # Brief pause between frameworks
            time.sleep(2)

    total_time = time.time() - start_time

    # Generate summary
    print(f"\n\n{'='*80}")
    print(f"ITERATION {iteration} SUMMARY")
    print(f"{'='*80}")
    print(f"Total execution time: {total_time:.2f}s")
    print(f"\nFramework Results (averaged across {repetitions} runs):\n")

    # Calculate averages per framework
    framework_stats = {}
    for framework_name, _ in frameworks:
        fw_results = [r for r in all_results if r["framework"] == framework_name]
        if fw_results:
            avg_correctness = sum(r["correctness"] for r in fw_results) / len(fw_results)
            avg_latency = sum(r["latency"] for r in fw_results) / len(fw_results)
            avg_tools = sum(r["tool_calls"] for r in fw_results) / len(fw_results)
            success_rate = sum(1 for r in fw_results if r["success"]) / len(fw_results) * 100

            framework_stats[framework_name] = {
                "correctness": avg_correctness,
                "latency": avg_latency,
                "tools": avg_tools,
                "success_rate": success_rate
            }

            print(f"{framework_name:35} | Correctness: {avg_correctness:5.1f}% | "
                  f"Latency: {avg_latency:6.2f}s | Tools: {avg_tools:4.1f} | "
                  f"Success: {success_rate:5.1f}%")

    # Save iteration summary
    summary_dir = Path(f"scenarios/scenario-3/iterations/iteration-{iteration}")
    summary_file = summary_dir / f"ITERATION_{iteration}_SUMMARY.md"

    with open(summary_file, 'w') as f:
        f.write(f"# Scenario-3 Iteration {iteration} Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Scenario**: T5 (Multi-Agent Product Investigation)\n")
        f.write(f"**Repetitions**: {repetitions} per framework\n")
        f.write(f"**Total Runs**: {len(all_results)}\n")
        f.write(f"**Total Time**: {total_time:.2f}s\n\n")

        f.write("## Framework Performance\n\n")
        f.write("| Framework | Correctness | Latency | Tool Calls | Success Rate |\n")
        f.write("|-----------|-------------|---------|------------|-------------|\n")

        for framework_name in sorted(framework_stats.keys(), key=lambda x: framework_stats[x]["correctness"], reverse=True):
            stats = framework_stats[framework_name]
            f.write(f"| {framework_name} | {stats['correctness']:.1f}% | "
                   f"{stats['latency']:.2f}s | {stats['tools']:.1f} | "
                   f"{stats['success_rate']:.0f}% |\n")

        f.write("\n## Key Findings\n\n")
        f.write("- Multi-agent coordination effectiveness varies by framework\n")
        f.write("- Tool call efficiency is critical for performance\n")
        f.write("- Context passing between agents impacts correctness\n")

    print(f"\nSummary saved to: {summary_file}")
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
