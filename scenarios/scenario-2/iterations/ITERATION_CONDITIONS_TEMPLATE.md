# Scenario-2 Iteration Conditions

**Purpose**: Document test conditions for reproducibility and comparison

---

## Scenario Configuration

### Scenario Type
- **Name**: Scenario-2 - Complex Multi-Issue Customer Support
- **Test Case**: S4 - The Frustrated Premium Customer
- **Complexity**: High (7-9 steps expected)

### Test Scenario (S4)

**User Message**:
```
Hi, this is customer CUST-001. I'm really frustrated. I have THREE issues:

1. My laptop order #ORD-1234 from 3 days ago arrived damaged
2. I have headphones #ORD-5678 processing, but I want to cancel it - I ordered the wrong model
3. My shipping address changed and I need to update it for the USB hub #ORD-9012 that's already shipped

Can you help me sort all this out?
```

**Simultaneous Issues**:
1. Damaged product (needs refund)
2. Wrong product ordered (needs cancellation)
3. Address change (in-transit order)

---

## Model Configuration

### Claude Sonnet 4.5
- **Model ID**: `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
- **Provider**: AWS Bedrock
- **Region**: us-west-2
- **Temperature**: 0 (deterministic)
- **AWS Profile**: prod-tools

### Pricing (for cost calculation)
- **Input**: $3.00 per 1M tokens
- **Output**: $15.00 per 1M tokens

---

## Framework Configuration

### Frameworks Under Test (4)

1. **Google ADK** (`arena/frameworks/google_adk.py`)
   - Version: Latest
   - Integration: AWS Bedrock
   - Expected: Strong context management

2. **AWS Strands** (`arena/frameworks/aws_strands.py`)
   - Version: Latest
   - Integration: AWS Bedrock (native)
   - Expected: Reliable performance

3. **Claude SDK** (`arena/frameworks/claude_sdk.py`)
   - Version: Latest
   - Integration: AWS Bedrock
   - Expected: Good observability

4. **CrewAI** (`arena/frameworks/crewai.py`)
   - Version: Latest (with GitHub PR fixes)
   - Integration: AWS Bedrock
   - Expected: May struggle with complexity

---

## Test Parameters

### Benchmark Settings
- **Repetitions (K)**: 3 runs per scenario
- **Scenarios**: 1 (S4 only)
- **Total Runs**: 12 (4 frameworks × 1 scenario × 3 runs)

### Success Criteria
- **Optimal Steps**: 7-9 tool calls
- **Correctness Criteria**: 8 checks (see below)
- **Pass³ Definition**: All 3 runs achieve 100% correctness

---

## Correctness Criteria (8 Checks)

### Core Actions (62.5%)

1. **looked_up_customer** (12.5%)
   - Verified customer identity and premium status

2. **retrieved_all_orders** (12.5%)
   - Retrieved all orders to see states

3. **handled_damaged_laptop** (25%)
   - Processed refund for ORD-1234
   - Most critical issue

4. **addressed_cancellation** (20%)
   - Searched KB or escalated for ORD-5678 cancellation

5. **addressed_address_change** (15%)
   - Searched KB for address change policy

### Response Quality (37.5%)

6. **acknowledged_all_issues** (10%)
   - Response mentions all 3 issues/orders

7. **correct_order_handling** (5%)
   - Didn't refund ORD-5678 or ORD-9012 incorrectly

8. **premium_acknowledgement** (bonus)
   - Acknowledged premium status for expedited service

---

## MCP Server Configuration

### Server Details
- **Implementation**: `arena/mcp_server.py`
- **Framework**: FastMCP
- **Tools**: 5 customer support tools

### Tools Available

1. **get_customer(customer_id)**
   - Returns: Profile, tier, account info
   - CUST-001: Premium member since 2023

2. **get_orders(customer_id)**
   - Returns: All customer orders with states
   - 3 orders for CUST-001 (different states)

3. **search_knowledge_base(query)**
   - Returns: Matching KB articles
   - 5 articles available

4. **process_refund(order_id, reason)**
   - Returns: Refund approval/denial
   - ORD-1234: Eligible ($1,299.99)

5. **escalate_to_human(ticket_id, summary)**
   - Returns: Escalation confirmation
   - Required for cancellations and complex cases

### Test Data

**Customer: CUST-001 (Jane Smith)**
- Tier: Premium
- Account Since: 2023-01-15
- Lifetime Orders: 47

**Orders**:
- **ORD-1234**: Laptop, $1,299.99, Delivered (2026-03-11), Refund Eligible ✅
- **ORD-5678**: Headphones, $199.99, Processing, Not Refund Eligible ❌
- **ORD-9012**: USB Hub, $49.99, Shipped (in transit), Not Refund Eligible ❌

**Knowledge Base**:
- KB-001: Refund Policy
- KB-002: How to Change Shipping Address
- KB-003: Billing Disputes
- KB-004: Order Tracking
- KB-005: Premium Membership Benefits

---

## Metrics Measured

### Per-Run Metrics
1. **Latency** - End-to-end execution time (seconds)
2. **Token Usage** - Input/output tokens (where available)
3. **Cost** - Calculated from token usage
4. **Tool Calls** - Sequence and count
5. **Correctness** - % of 8 criteria met
6. **Step Efficiency** - Optimal steps / actual steps

### Aggregated Metrics (K=3)
- **Median Latency** - Stable performance measure
- **Average Correctness** - Overall accuracy
- **Consistency (pass³)** - 1.0 if all runs ≥100%, else 0.0

---

## Expected Outcomes

### Hypotheses

1. **Increased Latency**
   - Expected: 1.5-2x vs Scenario-1
   - Reason: More tool calls (8 vs 3-4)

2. **Wider Score Distribution**
   - Scenario-1: 80%-92% (12% range)
   - Scenario-2: 50%-100% (expected 50% range)
   - Reason: More ways to fail, partial credit possible

3. **Higher Token Usage**
   - Expected: 2-3x vs Scenario-1
   - Reason: Longer prompt, more context, multi-issue

4. **Context Management Matters**
   - Frameworks with better context handling should score higher
   - Expected: Google ADK, AWS Strands maintain lead

5. **CrewAI Struggles**
   - Scenario-1: 80.67% (lowest)
   - Scenario-2: May drop further with complexity

### Success Metrics

**Benchmark succeeds if:**
- ✅ Results are reproducible (K=3)
- ✅ Scores show differentiation (not all same)
- ✅ Top frameworks adapt to complexity
- ✅ Metrics make sense (latency/tokens up, efficiency down)

---

## Environment

### System
- **OS**: macOS (Darwin)
- **Python**: 3.11+
- **Shell**: zsh

### Dependencies
- AWS Bedrock SDK
- FastMCP
- Framework-specific libraries

---

## Comparison Baseline (Scenario-1)

### Scenario-1 Results (for reference)

**S1 (Simple Refund)**:
- Winner: Google ADK (10.83s-12.40s, 100%)
- All frameworks: 100% correctness

**S2 (Address Change)**:
- Winner: Google ADK (12.14s-13.09s, 100%)
- CrewAI: 67% (consistent weakness)

**S3 (Billing Dispute)**:
- All frameworks: 75% (KB search skipped)
- Google ADK: Fastest (13.10s-13.16s)

**Overall Scenario-1**:
- Google ADK: 12.46s avg, 91.67%
- AWS Strands: 13.71s avg, 91.67%
- Claude SDK: 15.60s avg, 91.67%
- CrewAI: 13.84s avg, 80.67%

---

## Running the Benchmark

### Command
```bash
python scripts/run_scenario2.py 1
```

### Output Files
- `scenarios/scenario-2/iterations/iteration-1/results/combined_results.json`
- `scenarios/scenario-2/iterations/iteration-1/ITERATION_1_SUMMARY.md`

---

## Notes

### Key Differences from Scenario-1
1. **Single test case** (S4) vs 3 test cases (S1/S2/S3)
2. **Multi-issue complexity** vs single-issue simplicity
3. **8 criteria** vs 4-6 criteria
4. **Longer execution** (~20-25s expected vs ~13s)
5. **More ambiguity** (no direct cancel tool)

### What This Tests
- Context management across multiple orders
- Prioritization and sequencing
- Business logic application per order state
- Ambiguity resolution
- Response synthesis

---

**Template Status**: Ready for Iteration 1
**Last Updated**: 2026-03-13
**Scenario**: Complex Multi-Issue Support
