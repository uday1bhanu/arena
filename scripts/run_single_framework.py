"""Run complete benchmark for a single framework."""
import json
import time
from statistics import median
from dotenv import load_dotenv

load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.claude_sdk_agent import ClaudeSDKAdapter
from arena.evaluator import evaluate_scenario
from arena.metrics import (
    measure_code_complexity,
    compute_step_efficiency,
    compute_cost,
    compute_consistency,
)


def run_scenario_repetitions(adapter_class, scenario_id: str, repetitions: int = 3):
    """Run a scenario multiple times and collect metrics."""
    scenario = SCENARIOS[scenario_id]
    runs = []

    print(f"\n{'='*60}")
    print(f"Scenario {scenario_id}: {repetitions} repetitions")
    print(f"{'='*60}")

    for rep in range(1, repetitions + 1):
        print(f"  Rep {rep}/{repetitions}...", end=" ", flush=True)

        try:
            adapter = adapter_class(SYSTEM_PROMPT)
            adapter.start_mcp_server()
            adapter.connect_to_mcp()

            start = time.perf_counter()
            final_response = adapter.run_agent(scenario["user_message"])
            latency = time.perf_counter() - start

            usage = adapter.get_token_usage()
            tool_log = adapter.get_tool_log()
            adapter.stop_mcp_server()

            # Evaluate correctness
            eval_result = evaluate_scenario(scenario_id, tool_log, final_response)

            # Compute metrics
            step_eff = compute_step_efficiency(scenario_id, tool_log)
            cost = compute_cost(
                usage["input_tokens"],
                usage["output_tokens"],
                "claude_sonnet"
            )

            run_result = {
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "total_tokens": usage["input_tokens"] + usage["output_tokens"],
                "tool_calls": tool_log,
                "num_tool_calls": len(tool_log),
                "optimal_tool_calls": step_eff["optimal_tool_calls"],
                "step_efficiency_ratio": step_eff["step_efficiency_ratio"],
                "latency_seconds": round(latency, 2),
                "correctness_score": eval_result["correctness_score"],
                "correctness_details": eval_result["correctness_details"],
                "cost_usd": cost,
                "final_response": final_response[:100] + "..."
            }

            runs.append(run_result)
            print(f"✓ (correctness: {eval_result['correctness_score']:.2f})")

        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
            runs.append({"error": str(e), "correctness_score": 0.0})

    # Compute aggregates
    if runs:
        correctness_scores = [r.get("correctness_score", 0) for r in runs]
        consistency = compute_consistency(correctness_scores)

        latencies = [r.get("latency_seconds", 0) for r in runs if "latency_seconds" in r]
        input_tokens_list = [r.get("input_tokens", 0) for r in runs if "input_tokens" in r]
        output_tokens_list = [r.get("output_tokens", 0) for r in runs if "output_tokens" in r]
        costs = [r.get("cost_usd", 0) for r in runs if "cost_usd" in r]
        step_ratios = [r.get("step_efficiency_ratio", 1.0) for r in runs if "step_efficiency_ratio" in r]

        return {
            "per_run_results": runs,
            "median_latency": round(median(latencies), 2) if latencies else 0,
            "median_input_tokens": int(median(input_tokens_list)) if input_tokens_list else 0,
            "median_output_tokens": int(median(output_tokens_list)) if output_tokens_list else 0,
            "median_cost_usd": round(median(costs), 4) if costs else 0,
            "median_step_efficiency": round(median(step_ratios), 2) if step_ratios else 1.0,
            "consistency_pass3": consistency["consistency_pass3"],
            "per_run_correctness": consistency["per_run_correctness"],
        }

    return {}


def run_framework(framework_name: str, adapter_class, adapter_file: str):
    """Run full benchmark for one framework."""
    print(f"\n{'='*70}")
    print(f"BENCHMARKING: {framework_name}")
    print(f"{'='*70}")

    results = {"scenarios": {}}

    # Run each scenario 3 times
    for scenario_id in ["S1", "S2", "S3"]:
        scenario_results = run_scenario_repetitions(adapter_class, scenario_id, repetitions=3)
        results["scenarios"][scenario_id] = scenario_results

    # Measure code complexity
    complexity = measure_code_complexity(adapter_file)
    results["lines_of_code"] = complexity["lines_of_code"]
    results["cyclomatic_complexity"] = complexity["cyclomatic_complexity"]

    # Print summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: {framework_name}")
    print(f"{'='*70}")
    print(f"  Code: {results['lines_of_code']} LoC, CC {results['cyclomatic_complexity']}")

    for sid, sdata in results["scenarios"].items():
        print(f"\n  {sid}:")
        print(f"    Median latency: {sdata['median_latency']}s")
        print(f"    Median tokens: {sdata['median_input_tokens']} in / {sdata['median_output_tokens']} out")
        print(f"    Median cost: ${sdata['median_cost_usd']}")
        print(f"    Median step eff: {sdata['median_step_efficiency']}")
        print(f"    Consistency (pass³): {sdata['consistency_pass3']}")
        print(f"    Per-run correctness: {sdata['per_run_correctness']}")

    return results


if __name__ == "__main__":
    # Test with Claude SDK
    results = run_framework(
        "claude_sdk",
        ClaudeSDKAdapter,
        "arena/frameworks/claude_sdk_agent.py"
    )

    # Save results
    with open("arena/results/claude_sdk_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to arena/results/claude_sdk_results.json")
