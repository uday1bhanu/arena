# Scenario 1: Simple Linear Customer Support

**Type**: Single-Issue, Linear Resolution
**Complexity**: Low (3-4 steps per scenario)
**Focus**: Basic tool usage and straightforward problem-solving

---

## Overview

Scenario-1 tests agent frameworks on simple, single-issue customer support cases with clear, linear resolution paths. Each test scenario focuses on one specific problem that requires a deterministic sequence of tool calls.

**Design Philosophy**: Validate basic competency before testing complex scenarios.

---

## Test Scenarios (S1, S2, S3)

### S1: Damaged Laptop Refund

**User Message:**
```
Hi, this is customer CUST-001. I ordered a laptop 3 days ago and it arrived damaged.
Order #ORD-1234. I want a refund.
```

**Expected Resolution Path:**
1. `get_customer(CUST-001)` - Verify customer identity
2. `get_orders(CUST-001)` - Retrieve order details
3. `process_refund(ORD-1234)` - Process the refund

**Optimal Steps**: 3

**Correctness Criteria** (4/4 = 100%):
- ✅ Looked up customer profile
- ✅ Retrieved orders
- ✅ Processed refund for damaged item
- ✅ Confirmed refund amount ($1,299) to customer

**Key Testing Points:**
- Basic tool sequencing
- Order state validation (delivered, eligible)
- Premium customer handling (expedited processing)

---

### S2: Shipping Address Change

**User Message:**
```
Hi, I'm customer CUST-001. How do I change my shipping address for an upcoming delivery?
```

**Expected Resolution Path:**
1. `get_customer(CUST-001)` - Look up customer
2. `get_orders(CUST-001)` - Check for pending orders
3. `search_knowledge_base("change shipping address")` - Find instructions

**Optimal Steps**: 3

**Correctness Criteria** (6/6 = 100%):
- ✅ Looked up customer
- ✅ Retrieved orders
- ✅ Searched knowledge base
- ✅ Provided instructions (account settings/addresses)
- ❌ Did NOT process refund (negative criteria)
- ❌ Did NOT escalate (negative criteria)

**Key Testing Points:**
- Information retrieval (no actions required)
- Knowledge base usage
- Negative criteria (avoiding wrong actions)

---

### S3: Billing Dispute

**User Message:**
```
Hello, this is customer CUST-001. I was charged twice for my last order #ORD-5678.
Can you help?
```

**Expected Resolution Path:**
1. `get_customer(CUST-001)` - Look up customer
2. `get_orders(CUST-001)` - Verify the double charge (note in order data)
3. `search_knowledge_base("billing dispute")` - Check policy
4. `escalate_to_human(ticket_id, summary)` - Escalate for manual review

**Optimal Steps**: 4

**Correctness Criteria** (4/4 = 100%):
- ✅ Looked up order
- ✅ Searched knowledge base for policy
- ✅ Escalated to human agent
- ✅ Confirmed escalation to customer

**Key Testing Points:**
- Policy lookup before action
- Proper escalation (billing disputes require human review)
- Premium customer acknowledgment

---

## Tools Required (5 tools)

1. **get_customer(customer_id)** - Customer profile lookup
2. **get_orders(customer_id)** - Retrieve customer orders
3. **search_knowledge_base(query)** - Search support KB (5 articles)
4. **process_refund(order_id, reason)** - Process refund
5. **escalate_to_human(ticket_id, summary)** - Escalate to human agent

---

## MCP Server Configuration

**Server**: `arena/mcp_server.py`
- FastMCP-based tool server
- Simulated data for CUST-001
- 3 orders with different states:
  - ORD-1234: Delivered laptop ($1,299) - refund eligible
  - ORD-5678: Processing headphones ($199.99) - double charge noted
  - ORD-9012: Shipped USB hub ($49.99)

**Knowledge Base Articles**: 5 KB articles covering:
- Refund policy
- Shipping address changes
- Billing disputes
- Order tracking
- Premium membership benefits

---

## Benchmark Configuration

### Model Settings
- **Model**: Claude Sonnet 4.5 (AWS Bedrock)
- **Temperature**: 0 (deterministic results)
- **Provider**: AWS Bedrock (us-west-2)
- **Profile**: prod-tools

### Test Parameters
- **Repetitions (K)**: 3 runs per scenario
- **Frameworks Tested**: 4 (Google ADK, AWS Strands, Claude SDK, CrewAI)
- **Total Runs per Iteration**: 36 (4 frameworks × 3 scenarios × 3 runs)

### Metrics Measured
1. **Lines of Code** (LoC) - Framework adapter size
2. **Cyclomatic Complexity** (CC) - Code complexity
3. **Token Usage** - Input/output tokens (where available)
4. **Step Efficiency** - Optimal steps / actual steps
5. **Latency** - End-to-end execution time
6. **Correctness** - % of criteria met
7. **Consistency (pass³)** - All 3 runs achieve 100% correctness

---

## Results Summary (Iterations 1 & 2)

### Overall Winner: Google ADK

**Iteration 1** (March 12, 2026):
- Latency: 12.34s avg
- Correctness: 91.67%
- Consistency: 100% pass³

**Iteration 2** (March 13, 2026):
- Latency: 12.57s avg
- Correctness: 91.67%
- Consistency: 100% pass³

**Consistency Validated**: ✅
- Correctness scores: 100% identical
- Tool calling patterns: 100% identical
- Latency variance: +1.9% (excellent)

### Framework Rankings

| Rank | Framework | Avg Latency | Correctness | Pass³ |
|------|-----------|-------------|-------------|-------|
| 🥇 | Google ADK | 12.46s | 91.67% | 100% |
| 🥈 | AWS Strands | 13.71s | 91.67% | 100% |
| 🥉 | Claude SDK | 15.60s | 91.67% | 100% |
| 4th | CrewAI | 13.84s | 80.67% | 67% |

---

## Known Issues

### Critical: None

### Important:
1. **Token Tracking**: AWS Strands & Google ADK return 0 tokens
   - Workaround: Use Claude SDK or CrewAI for cost tracking

2. **Claude SDK Token Anomaly**: Dramatic drop in Iteration 2
   - Iteration 1: 4,998 avg input tokens
   - Iteration 2: 15 avg input tokens
   - Likely measurement bug

### Minor:
1. **S3 Knowledge Base Search**: All frameworks skip KB search (75% correctness)
   - System prompt may need clarification
   - Frameworks directly escalate without checking policy

2. **CrewAI S2 Correctness**: Consistently 67%
   - Reproducible design issue
   - Not random variance

---

## Key Findings

### Strengths of Simple Scenarios ✅
- **High Reproducibility**: Deterministic results with temperature=0
- **Clear Differentiation**: Speed differences clearly visible
- **Baseline Validation**: Confirms basic competency
- **Easy Debugging**: Simple paths make issues obvious

### Limitations 🔄
- **Too Linear**: Real support isn't this straightforward
- **Single-Issue Focus**: Customers often have multiple problems
- **Limited Context**: No conversation history or state management
- **Ceiling Effect**: All top frameworks hit 91.67% (limited differentiation)

---

## Transition to Scenario-2

**Why We Need Scenario-2:**

Scenario-1 successfully validates basic capabilities but doesn't test:
- Multi-issue complexity
- Context management across issues
- Prioritization and sequencing
- Ambiguity resolution
- Real-world support workflow

**See**: `../scenario-2/SCENARIO_2_DESCRIPTION.md` for the complex multi-issue scenario.

---

## Iteration Details

### Completed Iterations
- **Iteration 1**: March 12, 2026 - Complete ✅
  - See: `iterations/iteration-1/ITERATION_CONDITIONS.md`
  - Results: `iterations/iteration-1/results/`

- **Iteration 2**: March 13, 2026 - Complete ✅
  - See: `iterations/iteration-2/ITERATION_CONDITIONS.md`
  - Results: `iterations/iteration-2/results/`

### Comparison Analysis
- See: `iterations/ITERATION_COMPARISON.md`
- Validated reproducibility across 72 data points
- Confirmed benchmark validity

---

## Quick Start

### View Results
```bash
# Latest iteration
cat scenarios/scenario-1/iterations/iteration-2/ITERATION_2_SUMMARY.md

# Comparison
cat scenarios/scenario-1/iterations/ITERATION_COMPARISON.md

# Full results
cat scenarios/scenario-1/iterations/iteration-2/results/combined_results.json
```

### Run New Iteration (Scenario-1)
```bash
# From project root
python scripts/run_iteration.py 3
```

---

**Scenario Type**: Baseline / Simple
**Status**: ✅ Production Ready (2 iterations validated)
**Next**: See Scenario-2 for complex multi-issue testing
