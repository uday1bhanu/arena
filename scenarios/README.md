# Arena Benchmark Scenarios

This directory contains different scenario types for benchmarking agent frameworks.

---

## Scenario Organization

```
scenarios/
├── README.md (this file)
├── scenario-1/                    # Simple linear scenarios
│   ├── SCENARIO_1_DESCRIPTION.md
│   └── iterations/
│       ├── iteration-1/
│       ├── iteration-2/
│       └── ITERATION_COMPARISON.md
└── scenario-2/                    # Complex multi-issue scenarios
    ├── SCENARIO_2_DESCRIPTION.md
    └── iterations/
        └── (to be populated)
```

---

## Scenario Comparison

| Feature | Scenario-1 | Scenario-2 |
|---------|-----------|-----------|
| **Type** | Single-Issue | Multi-Issue |
| **Complexity** | Low (3-4 steps) | High (7-9 steps) |
| **Test Cases** | 3 (S1, S2, S3) | 1 (S4 - multi-issue) |
| **Focus** | Basic competency | Complex reasoning |
| **Context Management** | Simple | Complex (3 orders) |
| **Ambiguity** | None | High |
| **Status** | ✅ Complete (2 iterations) | 🚧 Ready to run |

---

## Scenario-1: Simple Linear

**Purpose**: Baseline validation of framework capabilities

### Test Scenarios

**S1: Damaged Laptop Refund**
- Single issue: damaged product
- Clear resolution: process refund
- 3 tool calls

**S2: Shipping Address Change**
- Single issue: information request
- Clear resolution: KB lookup
- 3 tool calls

**S3: Billing Dispute**
- Single issue: double charge
- Clear resolution: escalate to human
- 4 tool calls

### Key Results
- **Winner**: Google ADK (12.46s avg, 91.67% correct)
- **Validated**: 2 iterations, 100% reproducibility
- **Ceiling Effect**: Top 3 frameworks all hit 91.67%

**See**: `scenario-1/SCENARIO_1_DESCRIPTION.md`

---

## Scenario-2: Complex Multi-Issue

**Purpose**: Test real-world complexity and context management

### Test Scenario

**S4: The Frustrated Premium Customer**
- 3 simultaneous issues:
  1. Damaged laptop (needs refund)
  2. Wrong headphones ordered (needs cancellation)
  3. Address changed (needs update for in-transit order)
- Complex resolution: prioritize, handle each differently
- 7-9 tool calls

### Why This Tests More

1. **Context Management**: Track 3 order IDs and states
2. **Prioritization**: Sequence issues by feasibility
3. **Business Logic**: Apply different rules per order state
4. **Ambiguity**: No direct "cancel" tool - requires reasoning
5. **Synthesis**: Coherent response addressing all issues

### Expected Outcomes
- **Wider score distribution** (50%-100% vs. 67%-100%)
- **Better differentiation** between frameworks
- **Context management** becomes critical
- **Token usage** 2-3x higher
- **Latency** 1.5-2x higher

**See**: `scenario-2/SCENARIO_2_DESCRIPTION.md`

---

## Running Scenarios

### Scenario-1 (Simple)

```bash
# Run new iteration
python scripts/run_iteration.py 3

# View results
cat scenarios/scenario-1/iterations/iteration-2/ITERATION_2_SUMMARY.md
```

### Scenario-2 (Complex)

```bash
# Run first iteration (after implementation)
python scripts/run_scenario2.py 1

# View results
cat scenarios/scenario-2/iterations/iteration-1/ITERATION_1_SUMMARY.md
```

### Compare Scenarios

```bash
# Cross-scenario analysis
python scripts/compare_scenarios.py
```

---

## Research Questions

### Scenario-1 Answered ✅
- ✓ Can frameworks handle basic support tasks?
- ✓ Which is fastest? (Google ADK)
- ✓ Are results reproducible? (Yes, 100%)

### Scenario-2 Will Answer 🚧
- ? How do frameworks handle multi-issue complexity?
- ? Does context management differentiate frameworks?
- ? What's the cost (tokens/latency) of complexity?
- ? Does complexity reduce consistency?
- ? Which frameworks scale to real-world cases?

---

## Benchmark Philosophy

### Progressive Complexity

1. **Scenario-1**: Validate basics
   - If you can't do simple cases, stop here
   - Establishes baseline performance

2. **Scenario-2**: Test real-world capability
   - Builds on Scenario-1 tools/data
   - Reveals context management quality
   - Better differentiates frameworks

3. **Future Scenarios** (potential):
   - Scenario-3: Conversational (multi-turn)
   - Scenario-4: Error recovery
   - Scenario-5: Parallel tool calls

---

## Implementation Notes

### Shared Infrastructure
Both scenarios use:
- Same MCP server (`arena/mcp_server.py`)
- Same 5 tools
- Same customer/order data
- Same model configuration

### Different Test Cases
- Scenario-1: Simple, single-issue prompts
- Scenario-2: Complex, multi-issue prompt

### Independent Results
Each scenario has its own:
- Iterations directory
- Results tracking
- Analysis documentation

---

## Status

### Completed ✅
- **Scenario-1**: 2 iterations, validated, documented
  - 72 benchmark runs
  - Statistical validation complete
  - Winner identified (Google ADK)

### In Progress 🚧
- **Scenario-2**: Designed, documented, ready to implement
  - Scenario definition complete
  - Need to update evaluator
  - Need to run first iteration

### Planned 📋
- Cross-scenario comparison analysis
- Framework performance profiling
- Token efficiency deep dive

---

**Quick Links**:
- [Scenario-1 Details](scenario-1/SCENARIO_1_DESCRIPTION.md)
- [Scenario-2 Details](scenario-2/SCENARIO_2_DESCRIPTION.md)
- [Project Structure](../PROJECT_STRUCTURE.md)
- [Overall Status](../STATUS.md)
