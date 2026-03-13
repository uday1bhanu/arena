"""Correctness evaluator for Arena benchmark."""
from arena.scenarios import SCENARIOS


def evaluate_t1(tool_log: list[str], final_response: str) -> dict:
    """Score Test T1: Damaged Laptop Refund."""
    checks = {
        "looked_up_customer": "get_customer" in tool_log,
        "retrieved_orders": "get_orders" in tool_log,
        "processed_refund": "process_refund" in tool_log,
        "confirmed_to_customer": any(kw in final_response.lower() for kw in ["1299", "1,299", "refund"]),
    }
    score = sum(checks.values()) / len(checks)
    return {
        "correctness_score": round(score, 2),
        "correctness_details": checks,
    }


def evaluate_t2(tool_log: list[str], final_response: str) -> dict:
    """Score Test T2: Shipping Address Change."""
    checks = {
        "looked_up_customer": "get_customer" in tool_log,
        "retrieved_orders": "get_orders" in tool_log,
        "searched_kb": "search_knowledge_base" in tool_log,
        "provided_instructions": "account settings" in final_response.lower() or "addresses" in final_response.lower(),
        # Negative criteria
        "did_not_refund": "process_refund" not in tool_log,
        "did_not_escalate": "escalate_to_human" not in tool_log,
    }
    score = sum(checks.values()) / len(checks)
    return {
        "correctness_score": round(score, 2),
        "correctness_details": checks,
    }


def evaluate_t3(tool_log: list[str], final_response: str) -> dict:
    """Score Test T3: Double Charge / Billing Dispute."""
    checks = {
        "looked_up_order": "get_orders" in tool_log,
        "searched_kb": "search_knowledge_base" in tool_log,
        "escalated_to_human": "escalate_to_human" in tool_log,
        "provided_confirmation": any(kw in final_response.lower() for kw in ["esc", "human", "agent"]),
    }
    score = sum(checks.values()) / len(checks)
    return {
        "correctness_score": round(score, 2),
        "correctness_details": checks,
    }


def evaluate_t4(tool_log: list[str], final_response: str) -> dict:
    """Score Test T4: The Frustrated Premium Customer (Multi-Issue)."""
    tool_log_str = str(tool_log)
    final_response_lower = final_response.lower()

    # Check if refund was called with wrong order IDs
    refund_calls_str = str([call for call in tool_log if 'process_refund' in str(call)])

    checks = {
        # Core Actions (62.5% total)
        "looked_up_customer": "get_customer" in tool_log,
        "retrieved_all_orders": "get_orders" in tool_log,
        "handled_damaged_laptop": "process_refund" in tool_log and "1234" in tool_log_str,
        "addressed_cancellation": ("search_knowledge_base" in tool_log or "escalate_to_human" in tool_log) and ("5678" in final_response or "5678" in tool_log_str),
        "addressed_address_change": "search_knowledge_base" in tool_log,
        # Response Quality (37.5% total)
        "acknowledged_all_issues": (
            ("laptop" in final_response_lower or "1234" in final_response) and
            ("headphones" in final_response_lower or "5678" in final_response) and
            ("hub" in final_response_lower or "9012" in final_response)
        ),
        "correct_order_handling": "5678" not in refund_calls_str and "9012" not in refund_calls_str,
        "premium_acknowledgement": "premium" in final_response_lower or "expedited" in final_response_lower,
    }
    score = sum(checks.values()) / len(checks)
    return {
        "correctness_score": round(score, 2),
        "correctness_details": checks,
    }


EVALUATORS = {
    "T1": evaluate_t1,
    "T2": evaluate_t2,
    "T3": evaluate_t3,
    "T4": evaluate_t4,
}


def evaluate_scenario(scenario_id: str, tool_log: list[str], final_response: str) -> dict:
    """Route to the appropriate evaluator."""
    return EVALUATORS[scenario_id](tool_log, final_response)
