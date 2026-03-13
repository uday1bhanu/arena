# Scenario 2: Complex Multi-Issue Customer Support

**Type**: Multi-Issue, Complex Resolution
**Complexity**: High (7-9 steps per scenario)
**Focus**: Context management, prioritization, and real-world complexity

---

## Overview

Scenario-2 tests agent frameworks on realistic, complex customer support cases where customers present multiple simultaneous issues. This scenario requires agents to:

- **Manage multiple contexts** across different orders and states
- **Prioritize issues** based on feasibility and urgency
- **Apply business logic** correctly to each specific case
- **Synthesize information** from multiple tool calls
- **Handle ambiguity** and make appropriate decisions

**Design Philosophy**: Test real-world support complexity beyond simple linear paths.

---

## Primary Test Scenario: "The Frustrated Premium Customer"

### User Message

```
Hi, this is customer CUST-001. I'm really frustrated. I have THREE issues:

1. My laptop order #ORD-1234 from 3 days ago arrived damaged
2. I have headphones #ORD-5678 processing, but I want to cancel it - I ordered the wrong model
3. My shipping address changed and I need to update it for the USB hub #ORD-9012 that's already shipped

Can you help me sort all this out?
```

---

## Expected Resolution Path

### Optimal Path (7-9 steps)

1. **`get_customer(CUST-001)`** - Verify premium customer status
   - Important for expedited processing on Issue #1

2. **`get_orders(CUST-001)`** - Retrieve all 3 orders to see states
   - ORD-1234: Delivered (eligible for refund)
   - ORD-5678: Processing (may be cancelable)
   - ORD-9012: Shipped (address change complicated)

3. **`process_refund(ORD-1234, "damaged")`** - Handle Issue #1 (straightforward)
   - Clear case: delivered + damaged = refund
   - Premium customer = 1-2 day processing

4. **`search_knowledge_base("cancel order")`** - Check cancellation policy for Issue #2
   - Determine if processing orders can be canceled
   - KB should indicate escalation needed

5. **`escalate_to_human(ticket, "Cancel ORD-5678")`** - Escalate Issue #2
   - Processing orders require manual intervention
   - Can't be canceled via simple tool

6. **`search_knowledge_base("change shipping address")`** - Check policy for Issue #3
   - KB article KB-002: "For in-transit orders, contact support within 24 hours"
   - Shipped orders = already in transit

7. **`escalate_to_human(ticket, "ORD-9012 address update")` OR provide guidance**
   - Option A: Escalate (safest, best service)
   - Option B: Inform customer it may be too late (per KB policy)

8. **Synthesize response** - Address all 3 issues coherently
   - Confirm refund approved for Issue #1
   - Confirm escalation for Issue #2
   - Provide status/escalation for Issue #3
   - Acknowledge premium status and frustration

---

## Correctness Criteria (8 criteria)

### Core Actions (5 criteria)

1. **looked_up_customer** (12.5%)
   ```python
   "get_customer" in tool_log
   ```

2. **retrieved_all_orders** (12.5%)
   ```python
   "get_orders" in tool_log
   ```

3. **handled_damaged_laptop** (25%)
   ```python
   "process_refund" in tool_log and "ORD-1234" in combined_context
   ```
   - Must correctly identify which order to refund
   - Most critical issue (already received damaged goods)

4. **addressed_cancellation** (20%)
   ```python
   ("search_knowledge_base" in tool_log or "escalate_to_human" in tool_log)
   and "ORD-5678" in combined_context
   ```
   - Can either search KB or directly escalate
   - Must reference correct order ID

5. **addressed_address_change** (15%)
   ```python
   "search_knowledge_base" in tool_log
   and ("address" in kb_query or "shipping" in kb_query)
   ```
   - Must attempt to find policy

### Response Quality (3 criteria)

6. **acknowledged_all_issues** (10%)
   ```python
   all(x in final_response.lower() for x in ["laptop", "headphones", "hub"])
   or all(x in final_response for x in ["1234", "5678", "9012"])
   ```
   - Must explicitly address all 3 problems
   - No cherry-picking easy issues

7. **correct_order_handling** (5%)
   ```python
   not ("ORD-5678" in refund_calls or "ORD-9012" in refund_calls)
   ```
   - Negative criteria: shouldn't refund wrong orders
   - Tests order state understanding

8. **premium_acknowledgement** (bonus)
   ```python
   "premium" in final_response.lower() or "expedited" in final_response.lower()
   ```
   - Optional: acknowledge premium status for better service

---

## Scoring

### Full Credit (100%)
- All 8 criteria met
- All 3 issues addressed correctly
- Proper tool selection for each case
- Coherent synthesized response

### Partial Credit Examples

**87.5%** (7/8):
- Handled laptop refund ✅
- Addressed cancellation ✅
- Addressed address change ✅
- Acknowledged all issues ✅
- Correct order handling ✅
- Retrieved orders ✅
- Looked up customer ✅
- Missed premium acknowledgement ❌

**75%** (6/8):
- Core actions correct ✅
- Forgot to address one issue ❌
- No premium acknowledgement ❌

**50%** (4/8):
- Only handled 1-2 issues
- Missing KB searches
- Incomplete response

---

## Why This Tests Frameworks Differently

### Context Management
- **Challenge**: Must track 3 order IDs, 3 states, 3 different policies
- **Tests**: Memory management, context window usage
- **Differentiator**: Frameworks with poor context handling will mix up orders

### Prioritization
- **Challenge**: Which issue to handle first? (Hint: easiest = refund)
- **Tests**: Planning vs. reactive behavior
- **Differentiator**: Planned frameworks should sequence optimally

### Business Logic
- **Challenge**: Different rules for delivered/processing/shipped orders
- **Tests**: Understanding of order states and policies
- **Differentiator**: Frameworks that overgeneralize will make mistakes

### Ambiguity
- **Challenge**: "Cancel" isn't a direct tool - requires escalation
- **Tests**: Tool selection and fallback strategies
- **Differentiator**: Simple frameworks may get stuck

### Token Efficiency
- **Challenge**: Longer conversation = more tokens
- **Tests**: Prompt engineering and efficiency
- **Differentiator**: Verbose frameworks will cost more

---

## Tools Required (Same 5 tools)

1. **get_customer(customer_id)** - Customer profile lookup
2. **get_orders(customer_id)** - Retrieve customer orders
3. **search_knowledge_base(query)** - Search support KB (5 articles)
4. **process_refund(order_id, reason)** - Process refund
5. **escalate_to_human(ticket_id, summary)** - Escalate to human agent

**Note**: No new tools needed! Just more complex usage patterns.

---

## Order Data (Same as Scenario-1)

### CUST-001 Orders

**ORD-1234** - ProBook Laptop
- Status: Delivered (2026-03-11)
- Amount: $1,299.99
- Refund Eligible: ✅ True
- Issue: Arrived damaged

**ORD-5678** - NoiseCancel Pro Headphones
- Status: Processing
- Amount: $199.99
- Refund Eligible: ❌ False (not yet shipped)
- Issue: Customer wants to cancel (wrong model)
- Note: "Two charges of $199.99 recorded" (for S1's S3 scenario)

**ORD-9012** - USB-C Hub 7-in-1
- Status: Shipped (in transit)
- Amount: $49.99
- Refund Eligible: ❌ False (not delivered)
- Issue: Customer wants to update shipping address

---

## Knowledge Base Articles (Same KB)

**KB-002**: How to Change Shipping Address
- Keywords: shipping, address, change, update, delivery
- Content: "For in-transit orders, contact support within 24 hours of shipment. Changes cannot be made once the package is out for delivery."

**KB-003**: Billing Disputes
- Keywords: billing, charge, charged, twice, double, dispute
- Content: "Billing disputes require manual review by our finance team. Please escalate to a human agent."

*Note: No "cancel order" article - tests agent's ability to handle missing KB info*

---

## Benchmark Configuration

### Same as Scenario-1
- **Model**: Claude Sonnet 4.5 (AWS Bedrock)
- **Temperature**: 0 (deterministic)
- **Repetitions (K)**: 3 runs
- **Frameworks**: 4 (Google ADK, AWS Strands, Claude SDK, CrewAI)

### Key Difference
- **Expected Steps**: 7-9 (vs. 3-4 in Scenario-1)
- **Correctness Criteria**: 8 (vs. 4-6 in Scenario-1)
- **Complexity**: Multi-issue (vs. single-issue)

---

## Expected Outcomes

### Hypotheses to Test

1. **Context Management Matters**
   - Frameworks with better context handling score higher
   - Expect: Google ADK, AWS Strands maintain lead

2. **Partial Credit Reveals More**
   - Scenario-1 had ceiling effect (91.67% for top 3)
   - Scenario-2 should show more differentiation
   - Expect: Wider score distribution (50%-100%)

3. **Token Usage Amplified**
   - Longer scenarios = more tokens
   - Expect: 2-3x token usage vs. Scenario-1

4. **Latency Increases**
   - More tool calls = longer execution
   - Expect: 1.5-2x latency vs. Scenario-1

5. **Consistency Challenged**
   - More complexity = more variance
   - Expect: Lower pass³ rates (especially CrewAI)

### Success Metrics

**Benchmark is working if:**
- ✅ Scores range from 50%-100% (differentiation)
- ✅ Top frameworks from Scenario-1 adapt well
- ✅ CrewAI shows limitations with complexity
- ✅ Results remain reproducible (K=3 consistency)

---

## Implementation Status

### Current Status: 🚧 Ready to Implement

**Completed**:
- ✅ Scenario design finalized
- ✅ Correctness criteria defined
- ✅ Documentation written
- ✅ Directory structure created

**Next Steps**:
1. Update `arena/scenarios.py` with new S4 scenario
2. Update evaluator to handle 8 criteria
3. Run Iteration 1 for Scenario-2
4. Compare with Scenario-1 results
5. Analyze framework performance differences

---

## Running Scenario-2

### Quick Start

```bash
# Run iteration 1 for Scenario-2
# (After implementation)
python scripts/run_iteration_scenario2.py 1

# View results
cat scenarios/scenario-2/iterations/iteration-1/ITERATION_1_SUMMARY.md
```

### Comparison with Scenario-1

```bash
# Generate cross-scenario comparison
python scripts/compare_scenarios.py
```

---

## Research Questions

### Questions Scenario-2 Will Answer

1. **How do frameworks handle multi-issue complexity?**
   - Do scores drop significantly?
   - Which frameworks adapt better?

2. **Is context management a differentiator?**
   - Do some frameworks mix up order IDs?
   - How does token usage correlate with correctness?

3. **Does complexity reveal weaknesses?**
   - Does CrewAI's lower S1 scores amplify?
   - Do top frameworks maintain consistency?

4. **What's the cost of complexity?**
   - How much do tokens increase?
   - Is the latency increase proportional to steps?

5. **Is the benchmark still reproducible?**
   - Do we maintain K=3 consistency?
   - Or does complexity introduce variance?

---

## Comparison with Scenario-1

| Aspect | Scenario-1 | Scenario-2 |
|--------|-----------|-----------|
| **Issues per case** | 1 | 3 |
| **Optimal steps** | 3-4 | 7-9 |
| **Correctness criteria** | 4-6 | 8 |
| **Complexity** | Linear | Multi-branch |
| **Context management** | Simple | Complex |
| **Ambiguity** | None | High |
| **Expected token usage** | ~4,500 | ~10,000-15,000 |
| **Expected latency** | ~13s | ~20-25s |
| **Differentiation** | Moderate | High |

---

**Scenario Type**: Complex / Multi-Issue
**Status**: 🚧 Ready to Implement
**Dependencies**: Same tools and MCP server as Scenario-1
**Expected Timeline**: 1-2 hours implementation + 1 hour first iteration
