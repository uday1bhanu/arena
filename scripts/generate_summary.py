"""Generate comprehensive summary from combined results."""
import json
from statistics import mean

# Load combined results
with open("arena/results/combined_results.json", "r") as f:
    data = json.load(f)

frameworks = data["frameworks"]

print("\n" + "="*80)
print("ARENA BENCHMARK - COMPREHENSIVE RESULTS")
print("="*80)
print(f"Model: {data['model_config']['claude_model']}")
print(f"Date: {data['run_date']}")
print(f"Repetitions: {data['summary']['repetitions_per_scenario']} per scenario")
print("="*80)

# Framework Complexity
print("\n📊 FRAMEWORK IMPLEMENTATION COMPLEXITY")
print("-" * 80)
print(f"{'Framework':<15} {'LoC':>6} {'CC':>6} {'Status'}")
print("-" * 80)
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data:
        loc = fw_data["lines_of_code"]
        cc = fw_data["cyclomatic_complexity"]
        status = "✅ Working"
        print(f"{fw_name:<15} {loc:>6} {cc:>6.1f} {status}")
print()

# Scenario Results
scenarios = ["S1", "S2", "S3"]
scenario_names = {
    "S1": "Damaged Laptop Refund",
    "S2": "Shipping Address Change",
    "S3": "Billing Dispute"
}

for scenario_id in scenarios:
    print(f"\n{'='*80}")
    print(f"SCENARIO {scenario_id}: {scenario_names[scenario_id]}")
    print("="*80)
    print(f"{'Framework':<15} {'Latency':>10} {'In Tok':>9} {'Out Tok':>9} {'Cost':>8} {'StepEff':>8} {'Correct':>8} {'Pass³':>7}")
    print("-" * 80)

    for fw_name, fw_data in frameworks.items():
        if "error" not in fw_data and scenario_id in fw_data["scenarios"]:
            s = fw_data["scenarios"][scenario_id]
            latency = s["median_latency"]
            in_tok = s["median_input_tokens"]
            out_tok = s["median_output_tokens"]
            cost = s["median_cost_usd"]
            step_eff = s["median_step_efficiency"]
            correct = mean(s["per_run_correctness"])
            pass3 = s["consistency_pass3"]

            in_tok_str = f"{in_tok:,}" if in_tok > 0 else "0*"
            out_tok_str = f"{out_tok:,}" if out_tok > 0 else "0*"
            cost_str = f"${cost:.4f}" if cost > 0 else "$0.00*"

            print(f"{fw_name:<15} {latency:>9.2f}s {in_tok_str:>9} {out_tok_str:>9} {cost_str:>8} {step_eff:>8.2f} {correct:>8.2f} {pass3:>7.2f}")

# Overall Rankings
print(f"\n{'='*80}")
print("OVERALL RANKINGS")
print("="*80)

# Average latency
print("\n🏆 LATENCY (Average across all scenarios)")
print("-" * 80)
latencies = {}
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data:
        avg_latency = mean([
            fw_data["scenarios"][s]["median_latency"]
            for s in scenarios
            if s in fw_data["scenarios"]
        ])
        latencies[fw_name] = avg_latency

for i, (fw_name, lat) in enumerate(sorted(latencies.items(), key=lambda x: x[1]), 1):
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    print(f"{medal} {i}. {fw_name:<15} {lat:>8.2f}s")

# Average correctness
print("\n🎯 CORRECTNESS (Average across all scenarios)")
print("-" * 80)
correctness = {}
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data:
        avg_correct = mean([
            mean(fw_data["scenarios"][s]["per_run_correctness"])
            for s in scenarios
            if s in fw_data["scenarios"]
        ])
        correctness[fw_name] = avg_correct

for i, (fw_name, corr) in enumerate(sorted(correctness.items(), key=lambda x: x[1], reverse=True), 1):
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    print(f"{medal} {i}. {fw_name:<15} {corr:>8.2%}")

# Consistency
print("\n✅ CONSISTENCY (Pass³ - scenarios with 100% consistency)")
print("-" * 80)
consistency = {}
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data:
        pass3_count = sum([
            1 for s in scenarios
            if s in fw_data["scenarios"] and fw_data["scenarios"][s]["consistency_pass3"] == 1.0
        ])
        consistency[fw_name] = pass3_count

for i, (fw_name, count) in enumerate(sorted(consistency.items(), key=lambda x: x[1], reverse=True), 1):
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    pct = (count / len(scenarios)) * 100
    print(f"{medal} {i}. {fw_name:<15} {count}/3 scenarios ({pct:>5.1f}%)")

# Total cost
print("\n💰 COST EFFICIENCY (Total cost across all scenarios)")
print("-" * 80)
costs = {}
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data:
        total_cost = sum([
            fw_data["scenarios"][s]["median_cost_usd"]
            for s in scenarios
            if s in fw_data["scenarios"]
        ])
        costs[fw_name] = total_cost

for i, (fw_name, cost) in enumerate(sorted(costs.items(), key=lambda x: x[1]), 1):
    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
    cost_str = f"${cost:.4f}" if cost > 0 else "$0.0000*"
    print(f"{medal} {i}. {fw_name:<15} {cost_str:>10}")

print("\n* Token tracking returns 0 (implementation limitation)")

# Key Insights
print(f"\n{'='*80}")
print("KEY INSIGHTS")
print("="*80)

fastest = min(latencies.items(), key=lambda x: x[1])
most_correct = max(correctness.items(), key=lambda x: x[1])
most_consistent = max(consistency.items(), key=lambda x: x[1])

print(f"\n⚡ Fastest Framework: {fastest[0]} ({fastest[1]:.2f}s avg latency)")
print(f"🎯 Most Correct: {most_correct[0]} ({most_correct[1]:.2%} avg correctness)")
print(f"✅ Most Consistent: {most_consistent[0]} ({most_consistent[1]}/3 scenarios 100% consistent)")

print("\n📝 Implementation Notes:")
for fw_name, fw_data in frameworks.items():
    if "error" not in fw_data and "notes" in fw_data:
        print(f"  • {fw_name}: {fw_data['notes']}")

print("\n" + "="*80)
print("Results saved to:")
print("  - arena/results/combined_results.json")
print("  - arena/results/combined_results_table.md")
print("="*80 + "\n")
