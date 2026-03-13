#!/usr/bin/env python3
"""Arena MCP Server - 5 tools for customer support triage."""
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("arena-support-tools")

# --- Tool call tracking (for Metric 3) ---
_tool_call_log: list[str] = []


@mcp.tool()
def get_customer(customer_id: str) -> str:
    """Look up a customer profile by ID."""
    _tool_call_log.append("get_customer")
    if customer_id == "CUST-001":
        return json.dumps({
            "id": "CUST-001",
            "name": "Jane Smith",
            "email": "jane.smith@email.com",
            "phone": "+1-555-0123",
            "tier": "premium",
            "account_since": "2023-01-15",
            "lifetime_orders": 47
        })
    return json.dumps({"error": "Customer not found"})


@mcp.tool()
def get_orders(customer_id: str) -> str:
    """Retrieve all orders for a customer."""
    _tool_call_log.append("get_orders")
    if customer_id == "CUST-001":
        return json.dumps([
            {
                "order_id": "ORD-1234",
                "product": "ProBook Laptop 15-inch",
                "amount": 1299.99,
                "status": "delivered",
                "order_date": "2026-03-09",
                "delivery_date": "2026-03-11",
                "refund_eligible": True
            },
            {
                "order_id": "ORD-5678",
                "product": "NoiseCancel Pro Headphones",
                "amount": 199.99,
                "status": "processing",
                "order_date": "2026-03-10",
                "delivery_date": None,
                "refund_eligible": False,
                "note": "Two charges of $199.99 recorded"
            },
            {
                "order_id": "ORD-9012",
                "product": "USB-C Hub 7-in-1",
                "amount": 49.99,
                "status": "shipped",
                "order_date": "2026-03-11",
                "delivery_date": None,
                "refund_eligible": False
            }
        ])
    return json.dumps([])


@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """Search the support knowledge base."""
    _tool_call_log.append("search_knowledge_base")
    # Simple keyword matching against 5 articles
    articles = [
        {
            "id": "KB-001",
            "title": "Refund Policy",
            "keywords": ["refund", "return", "damaged", "defective"],
            "content": "Refunds are available within 30 days of delivery for damaged or defective items. Premium customers receive expedited processing (1-2 business days). Standard refunds take 3-5 business days."
        },
        {
            "id": "KB-002",
            "title": "How to Change Shipping Address",
            "keywords": ["shipping", "address", "change", "update", "delivery"],
            "content": "To change your shipping address: 1) Go to Account Settings > Addresses. 2) Click Edit on the address. 3) For in-transit orders, contact support within 24 hours of shipment. Changes cannot be made once the package is out for delivery."
        },
        {
            "id": "KB-003",
            "title": "Billing Disputes",
            "keywords": ["billing", "charge", "charged", "twice", "double", "dispute", "overcharged"],
            "content": "Billing disputes require manual review by our finance team. Please escalate to a human agent who will initiate the investigation. Typical resolution: 5-7 business days. If confirmed, a full refund is issued."
        },
        {
            "id": "KB-004",
            "title": "Order Tracking",
            "keywords": ["track", "tracking", "where", "status", "delivery"],
            "content": "Track your order in Account > Orders. Status updates: processing, shipped, out for delivery, delivered."
        },
        {
            "id": "KB-005",
            "title": "Premium Membership Benefits",
            "keywords": ["premium", "membership", "benefits", "tier"],
            "content": "Premium members get: free 2-day shipping, priority support, extended 60-day return window, and exclusive deals."
        }
    ]

    query_lower = query.lower()
    results = []
    for article in articles:
        if any(kw in query_lower for kw in article["keywords"]):
            results.append({
                "id": article["id"],
                "title": article["title"],
                "keywords": article["keywords"],
                "content": article["content"]
            })

    return json.dumps(results)


@mcp.tool()
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    _tool_call_log.append("process_refund")
    if order_id == "ORD-1234":
        return json.dumps({
            "status": "approved",
            "refund_id": "REF-88421",
            "order_id": order_id,
            "amount": 1299.99,
            "processing_time": "1-2 business days (premium customer)",
            "method": "original payment method"
        })
    return json.dumps({"status": "denied", "reason": "Order not eligible for refund"})


@mcp.tool()
def escalate_to_human(ticket_id: str, summary: str) -> str:
    """Escalate issue to a human support agent."""
    _tool_call_log.append("escalate_to_human")
    return json.dumps({
        "status": "escalated",
        "ticket_id": ticket_id,
        "queue": "billing-disputes",
        "position": 3,
        "estimated_wait": "15 minutes",
        "reference_number": "ESC-20260312-001"
    })


# --- Admin tools (called by runner, not the agent) ---
@mcp.tool()
def arena_get_log() -> str:
    """[Admin] Return the tool call log."""
    return json.dumps(_tool_call_log)


@mcp.tool()
def arena_reset_log() -> str:
    """[Admin] Clear the tool call log."""
    _tool_call_log.clear()
    return json.dumps({"status": "reset"})


if __name__ == "__main__":
    mcp.run()
