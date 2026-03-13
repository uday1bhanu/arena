"""Metrics helpers for Arena benchmark."""
import ast
from radon.complexity import cc_visit


# Metric 1: Lines of Code + Cyclomatic Complexity
def measure_code_complexity(filepath: str) -> dict:
    """Measure LoC and Cyclomatic Complexity for a file."""
    with open(filepath) as f:
        source = f.read()

    # LoC: non-blank, non-comment lines
    loc = sum(
        1 for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )

    # CC: radon returns a list of complexity results per function/method
    # Average them
    cc_results = cc_visit(source)
    if cc_results:
        avg_cc = sum(r.complexity for r in cc_results) / len(cc_results)
    else:
        avg_cc = 1.0  # no functions = trivially simple

    return {
        "lines_of_code": loc,
        "cyclomatic_complexity": round(avg_cc, 1)
    }


# Metric 3: Step Efficiency Ratio
OPTIMAL_STEPS = {"T1": 3, "T2": 3, "T3": 4, "T4": 8}


def compute_step_efficiency(scenario_id: str, tool_log: list[str]) -> dict:
    """Compute step efficiency ratio."""
    actual = len(tool_log)
    optimal = OPTIMAL_STEPS[scenario_id]
    return {
        "tool_calls": tool_log,
        "num_tool_calls": actual,
        "optimal_tool_calls": optimal,
        "step_efficiency_ratio": round(actual / optimal, 1),
    }


# Metric 6: Cost per Task ($)
PRICING = {
    "claude_sonnet": {
        "input_per_M": 3.00,  # $/1M input tokens
        "output_per_M": 15.00,  # $/1M output tokens
    },
    "gemini_flash": {
        "input_per_M": 0.10,
        "output_per_M": 0.40,
    },
}


def compute_cost(input_tokens: int, output_tokens: int, model: str = "claude_sonnet") -> float:
    """Compute USD cost for a single run."""
    p = PRICING[model]
    cost = (input_tokens / 1_000_000) * p["input_per_M"] + \
           (output_tokens / 1_000_000) * p["output_per_M"]
    return round(cost, 4)


# Metric 7: Consistency (pass³)
CONSISTENCY_THRESHOLD = 0.75  # minimum correctness to "pass"
K = 3  # number of repetitions


def compute_consistency(per_run_scores: list[float]) -> dict:
    """Compute pass³ consistency."""
    assert len(per_run_scores) == K
    all_passed = all(s >= CONSISTENCY_THRESHOLD for s in per_run_scores)
    return {
        "per_run_correctness": per_run_scores,
        "consistency_pass3": 1.0 if all_passed else 0.0,
    }
