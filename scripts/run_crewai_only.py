"""Run benchmark for CrewAI only."""
import json
import time
from statistics import median
from dotenv import load_dotenv

load_dotenv()

from arena.scenarios import SYSTEM_PROMPT, SCENARIOS
from arena.frameworks.crewai_agent import CrewAIAdapter
from arena.evaluator import evaluate_scenario
from arena.metrics import (
    measure_code_complexity,
    compute_step_efficiency,
    compute_cost,
    compute_consistency,
)


K = 3  # repetitions per scenario


def run_single_scenario(scenario_id: str):
    """Run one scenario once."""
    scenario = SCENARIOS[scenario_id]

    adapter = CrewAIAdapter(SYSTEM_PROMPT)
    adapter.start_mcp_server()
    adapter.connect_to_mcp()

    start = time.perf_counter()
    final_response = adapter.run_agent(scenario["user_message"])
    latency = time.perf_counter() - start

    usage = adapter.get_token_usage()
    tool_log = adapter.get_tool_log()

    adapter.stop_mcp_server()

    correctness_result = evaluate_scenario(scenario_id, tool_log, final_response)
    step_eff_result = compute_step_efficiency(scenario_id, tool_log)
    cost = compute_cost(usage["input_tokens"], usage["output_tokens"])

    return {
        "latency": latency,
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "correctness": correctness_result["correctness_score"],
        "step_efficiency": step_eff_result["step_efficiency_ratio"],
        "cost_usd": cost,
        "tool_count": len(tool_log),
    }


def main():
    """Run benchmark for CrewAI."""
    print("\n" + "="*70)
    print("ARENA: CrewAI Benchmark")
    print("="*70)

    # Measure code complexity
    complexity_result = measure_code_complexity("arena/frameworks/crewai_agent.py")

    results = {
        "lines_of_code": complexity_result["lines_of_code"],
        "cyclomatic_complexity": complexity_result["cyclomatic_complexity"],
        "scenarios": {}
    }

    for scenario_id in ["S1", "S2", "S3"]:
        print(f"\n--- Scenario {scenario_id} ---")
        runs = []

        for rep in range(1, K + 1):
            try:
                run_result = run_single_scenario(scenario_id)
                runs.append(run_result)
                print(f"  Rep {rep}/{K}... ✓ (correctness: {run_result['correctness']:.2f})")
            except Exception as e:
                print(f"  Rep {rep}/{K}... ✗ Error: {str(e)[:50]}")
                import traceback
                traceback.print_exc()
                continue

        if not runs:
            print(f"  All repetitions failed for {scenario_id}")
            continue

        # Compute medians
        latencies = [r["latency"] for r in runs]
        input_tokens = [r["input_tokens"] for r in runs]
        output_tokens = [r["output_tokens"] for r in runs]
        costs = [r["cost_usd"] for r in runs]
        step_effs = [r["step_efficiency"] for r in runs]
        correctnesses = [r["correctness"] for r in runs]

        consistency_result = compute_consistency(correctnesses)

        results["scenarios"][scenario_id] = {
            "median_latency": round(median(latencies), 2),
            "median_input_tokens": int(median(input_tokens)),
            "median_output_tokens": int(median(output_tokens)),
            "median_cost_usd": round(median(costs), 4),
            "median_step_efficiency": round(median(step_effs), 2),
            "consistency_pass3": consistency_result["consistency_pass3"],
            "per_run_correctness": [round(c, 2) for c in correctnesses],
        }

    # Load existing results and merge
    try:
        with open("arena/results/new_frameworks_results.json", "r") as f:
            all_results = json.load(f)
    except FileNotFoundError:
        all_results = {}

    all_results["crewai"] = results

    # Save results
    with open("arena/results/new_frameworks_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "="*70)
    print("Results saved to: arena/results/new_frameworks_results.json")
    print("="*70)

    # Print summary
    print("\nCrewAI Results:")
    print(f"  LoC: {results['lines_of_code']}, CC: {results['cyclomatic_complexity']:.1f}")
    for sid, sdata in results.get("scenarios", {}).items():
        print(f"  {sid}: tokens={sdata['median_input_tokens']}/{sdata['median_output_tokens']}, "
              f"correctness={sdata['per_run_correctness']}, pass³={sdata['consistency_pass3']:.2f}")


if __name__ == "__main__":
    main()
