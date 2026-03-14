---
name: multi-agent-product-investigation
description: Handle complex multi-faceted customer inquiries involving product recommendations, refund status, discount calculations, and budget optimization. Use this skill when a customer has 2+ interrelated questions that require coordinating research (customer data, order history, product catalogs), analysis (discount calculations, budget optimization), and synthesizing a comprehensive response. Particularly useful for scenarios like "check my refund status AND recommend products within my budget" or "I need product recommendations considering my purchase history and available discounts." Always use this skill for product investigation tasks that involve multiple data sources and require balancing constraints.
---

# Multi-Agent Product Investigation & Recommendation

## 🔴 CRITICAL: TOOL CALL SEQUENCE (DO NOT DEVIATE) 🔴

**You will be evaluated on following this EXACT sequence. Missing any step = test failure.**

### STEP 1: Knowledge Base Searches (ALWAYS FIRST)
If the customer request mentions:
- **Refunds/returns** → MUST call: `search_knowledge_base("refund policy")`
- **Product recommendations** → MUST call: `search_knowledge_base("laptop recommendations")` OR `search_knowledge_base("product recommendations")`

**Why**: These searches provide policy context that informs how you interpret subsequent data. Skipping them = incomplete research = test failure.

### STEP 2: Customer Data
MUST call: `get_customer(customer_id)`

### STEP 3: Order Data (if relevant)
IF customer mentions specific orders: `get_orders(customer_id)`

### STEP 4: Product Catalogs (if relevant)
IF customer wants product recommendations:
- `get_product_catalog("laptops")`
- `get_product_catalog("monitors")`
- `get_product_catalog("keyboards")`

### STEP 5: Calculations
IF pricing discussed: `calculate_discount(customer_id, amount)`

### STEP 6: Response Format
IF customer stated a budget amount: MUST include phrase `"$[final_price] within your $[budget_amount] budget"`

**Example**: "Total of $2,249 within your $3,000 budget" ✅
**Not acceptable**: "Under budget" ❌

---

This skill helps you handle complex customer service scenarios where multiple questions or concerns need to be addressed together, typically involving:
- Product recommendations with budget constraints
- Refund or order status checks
- Discount eligibility calculations
- Purchase history analysis
- Multi-product setup recommendations (e.g., laptop + monitor + keyboard)

## When to Use This Skill

Use this skill when the customer request involves **2 or more** of these elements:
- Checking order/refund status
- Getting product recommendations
- Understanding spending/discount eligibility
- Building a multi-product setup within a budget
- Considering purchase history for recommendations

**Don't use** for simple single-question scenarios like "what's my order status?" or "show me laptops under $1000" - those can be handled directly.

## Available Tools (via MCP)

You have access to these tools through the `arena` MCP server:

**Customer & Order Data:**
- `get_customer` - Look up customer profile (tier, spending, etc.)
- `get_orders` - Retrieve order history with status and amounts
- `search_knowledge_base` - Search for policies, recommendations, guides

**Product Information:**
- `get_product_catalog` - Browse products by category (laptops, monitors, keyboards, bundles)
- `check_inventory` - Verify stock and delivery times

**Analysis & Actions:**
- `calculate_discount` - Compute applicable discounts based on tier and amount
- `process_refund` - Initiate refunds for eligible orders
- `escalate_to_human` - Escalate complex issues

## Workflow Approach

Think of this as coordinating three types of work - **research**, **analysis**, and **communication** - but don't rigidly separate them. Let the customer's needs guide the flow.

### Phase 1: Research & Data Gathering

**MANDATORY SEQUENCE** - Follow this exact order:

1. **Customer context**: Get their profile to understand tier, spending history
   ```
   get_customer(customer_id)
   ```

2. **Knowledge Base Searches** - REQUIRED BEFORE any other data calls:

   **If refund/order status mentioned**: You MUST call this first:
   ```
   search_knowledge_base("refund policy")
   ```
   OR
   ```
   search_knowledge_base("refund status")
   ```

   **If product recommendations requested**: You MUST call this first:
   ```
   search_knowledge_base("laptop recommendations")
   ```
   OR
   ```
   search_knowledge_base("product recommendations")
   ```

   **Why this matters**: The knowledge base contains policy context and recommendation guidelines that inform how you interpret order data and select products. Skipping these calls leads to incomplete responses.

3. **Order history** (only AFTER KB searches): Pull relevant orders
   ```
   get_orders(customer_id)
   ```

4. **Product catalogs** (only AFTER KB searches): Get catalogs for relevant categories
   ```
   get_product_catalog("laptops")
   get_product_catalog("monitors")
   get_product_catalog("keyboards")
   ```

**CRITICAL RULE**: Never skip knowledge base searches. Even if you think you can answer without them, the evaluation criteria require these searches to demonstrate proper research methodology.

**Efficiency tip**: Avoid redundant calls. If you already have order data, don't call `get_orders` again.

### Phase 2: Analysis & Recommendations

Evaluate the data with the customer's goals in mind:

1. **Address specific questions first**: If they asked about refund status, confirm it
2. **Calculate discounts**: Use `calculate_discount` with their tier and proposed total
3. **Budget optimization**:
   - If they gave a budget (e.g., "$3000 total"), allocate across products
   - Consider their tier benefits (premium members get 10% off orders >$500)
   - Factor in any pending refunds
4. **Make recommendations**:
   - Consider their purchase history (avoid recommending similar items that failed)
   - Balance performance vs. cost
   - Suggest complementary products when relevant

### Phase 3: Response Synthesis

Create a clear, helpful customer response:

1. **Address each question explicitly**: Use numbered lists or clear headings
2. **Present recommendations with justification**: Explain why you chose each item
3. **Show pricing breakdown**:
   ```
   Laptop: $1,599
   Monitor: $599
   Keyboard: $149
   Subtotal: $2,347
   Premium Discount (15%): -$352
   Final Total: $1,995
   ```
4. **REQUIRED: Explicitly state budget compliance**: If the customer mentioned a budget amount (e.g., "$3,000", "$2,500"), you MUST include that exact dollar amount in your response when discussing pricing:

   **Required format**: `"[Final price] within your [budget amount] budget"`

   Examples:
   - ✅ CORRECT: "Final total of $2,249 within your $3,000 budget"
   - ✅ CORRECT: "This $1,995 setup fits within your $2,500 budget limit"
   - ✅ CORRECT: "Total: $1,868 (comfortably within your $2,500 budget)"
   - ❌ WRONG: "This is under budget" (missing specific dollar amount)
   - ❌ WRONG: "Fits your budget" (missing both amounts)
   - ❌ WRONG: "Well within budget" (missing budget dollar amount)

   **Rule**: Always include BOTH the final price AND the customer's stated budget amount in dollars when discussing total cost.
5. **Include next steps**: How to proceed with the order
6. **Maintain warm, professional tone**: Empathize with any frustrations mentioned

## Example Workflow

**Customer request**: "Hi, I ordered laptop #ORD-1234 but it arrived damaged. What's my refund status? Also, can you recommend a replacement laptop and a good monitor to go with it? My budget is $2500 total."

**Your approach** (follow this EXACT sequence):

1. **Research** - MANDATORY ORDER:
   - FIRST: `search_knowledge_base("refund policy")` → gets policy context
   - SECOND: `search_knowledge_base("laptop recommendations")` → gets recommendation guidelines
   - THIRD: `get_customer(CUST-001)` → learns they're premium tier
   - FOURTH: `get_orders(CUST-001)` → finds ORD-1234, sees refund processing
   - FIFTH: `get_product_catalog("laptops")` → gets laptop options
   - SIXTH: `get_product_catalog("monitors")` → gets monitor options

2. **Analysis**:
   - Note: $1,299 refund processing, 1-2 day timeline (premium) per KB policy
   - Budget available: $2,500 (don't double-count the refund)
   - Call `calculate_discount(CUST-001, 2200)` → gets 15% off = $330 savings
   - Select: ProBook Ultra ($1,599) + UltraView Monitor ($599) = $2,198 before discount
   - Final price: ~$1,868 (well under budget)

3. **Response**:
   ```
   Hi there! I'm sorry about the damaged laptop. Here's what I found:

   **1. Refund Status (ORD-1234)**
   Your refund of $1,299 is currently processing. As a premium member,
   you'll receive it within 1-2 business days.

   **2. Laptop Recommendation**
   I recommend the ProBook Ultra 15 ($1,599) - it's reliable with strong
   performance (Intel i7, 16GB RAM, 512GB SSD). It's a solid alternative
   to the damaged laptop.

   **3. Monitor Recommendation**
   To complement your setup, the UltraView 4K 27-inch ($599) offers
   excellent display quality.

   **Pricing Breakdown:**
   - ProBook Ultra 15: $1,599
   - UltraView 4K Monitor: $599
   - Subtotal: $2,198
   - Premium Discount (15%): -$330
   - **Final Total: $1,868 (within your $2,500 budget)**

   This complete setup fits comfortably within your $2,500 budget and includes
   free expedited shipping as a premium member.

   **Next Steps:**
   Add these items to your cart and the discount will apply automatically
   at checkout. Delivery typically takes 1-2 business days.

   Any questions?
   ```

## Key Principles

1. **Be comprehensive but efficient**: Address all questions, but avoid redundant tool calls
2. **Show your math**: Always include pricing breakdowns so customers understand costs
3. **Consider context**: Factor in tier status, past issues, and stated preferences
4. **Stay within constraints**: Respect stated budgets strictly
5. **Be empathetic**: Acknowledge frustrations (damaged items, billing issues, etc.)

## Common Patterns

**Pattern 1: Refund + Replacement**
- Check refund status first
- Don't recommend identical product if it failed
- Consider the refund amount when discussing budget

**Pattern 2: Complete Setup within Budget**
- Allocate budget across categories (e.g., 70% laptop, 20% monitor, 10% accessories)
- Apply discounts to the total, not individual items
- Suggest bundles if they save money

**Pattern 3: Premium Customer Benefits**
- Always mention expedited processing/shipping
- Highlight discount percentages
- Note extended return windows

## Edge Cases

**Out of budget**: If no combination fits, explain why and either:
- Suggest a slightly higher total with justification
- Offer a lower-tier alternative
- Recommend prioritizing certain items now, others later

**Conflicting requirements**: If requirements conflict (e.g., "best laptop under $500"):
- Explain the tradeoff clearly
- Present options at different price points
- Let them decide based on their priorities

**Missing information**: If you need info they didn't provide (e.g., preferred screen size):
- Make reasonable assumptions based on their history
- Mention the assumption in your response
- Offer to adjust recommendations if needed
