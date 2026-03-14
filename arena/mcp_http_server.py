#!/usr/bin/env python3
"""HTTP REST API wrapper for Arena MCP tools - for CrewAI, Google ADK, AWS Strands."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import uvicorn

app = FastAPI(title="Arena MCP HTTP API")

# --- Tool call tracking ---
_tool_call_log: list[str] = []


# --- Request/Response Models ---
class ToolRequest(BaseModel):
    tool: str
    arguments: dict


class ToolResponse(BaseModel):
    result: dict | str


# --- MCP Tools (duplicated from mcp_server_v2.py for HTTP access) ---

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
            "lifetime_orders": 47,
            "ytd_spending": 8450.32
        })
    return json.dumps({"error": "Customer not found"})


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
                "refund_eligible": True,
                "refund_status": "processing",
                "refund_amount": 1299.99,
                "issue": "Damaged on arrival - screen cracked"
            },
            {
                "order_id": "ORD-5678",
                "product": "NoiseCancel Pro Headphones",
                "amount": 299.99,
                "status": "delivered",
                "order_date": "2026-02-20"
            },
            {
                "order_id": "ORD-9012",
                "product": "USB-C Hub Pro",
                "amount": 79.99,
                "status": "shipped",
                "order_date": "2026-03-12"
            }
        ])
    return json.dumps([])


def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    _tool_call_log.append("search_knowledge_base")
    kb_data = {
        "refund": "Refunds are processed within 3-5 business days. Check order status for eligibility.",
        "laptop": "We offer TechPro Elite, ProBook Ultra, and BudgetBook Air laptops with different specs.",
        "premium": "Premium members get 10% discount on orders over $500 and priority support.",
        "discount": "Discounts: Premium tier 10%, high spenders get additional 5% on large purchases."
    }

    query_lower = query.lower()
    results = []
    for key, value in kb_data.items():
        if key in query_lower:
            results.append({"topic": key, "content": value})

    return json.dumps({"query": query, "results": results, "count": len(results)})


def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    _tool_call_log.append("process_refund")
    return json.dumps({
        "order_id": order_id,
        "refund_status": "processed",
        "refund_amount": 1299.99,
        "message": f"Refund processed for order {order_id}. Reason: {reason}"
    })


def escalate_to_human(issue_summary: str, priority: str = "normal") -> str:
    """Escalate an issue to human support."""
    _tool_call_log.append("escalate_to_human")
    return json.dumps({
        "ticket_id": "TICKET-789",
        "status": "escalated",
        "priority": priority,
        "message": "Issue escalated to human support team."
    })


def get_product_catalog(category: str) -> str:
    """Get product catalog for a category."""
    _tool_call_log.append("get_product_catalog")

    catalogs = {
        "laptops": [
            {"product_id": "LAP-001", "name": "TechPro Elite 16", "price": 1899.00,
             "specs": "Intel i9, 32GB RAM, 1TB SSD, RTX 4070", "rating": 4.8, "stock": "in_stock"},
            {"product_id": "LAP-002", "name": "ProBook Ultra 15", "price": 1599.00,
             "specs": "Intel i7, 16GB RAM, 512GB SSD, RTX 4060", "rating": 4.6, "stock": "in_stock"},
            {"product_id": "LAP-003", "name": "BudgetBook Air 14", "price": 899.00,
             "specs": "Intel i5, 8GB RAM, 256GB SSD, Integrated Graphics", "rating": 4.3, "stock": "low_stock"}
        ],
        "monitors": [
            {"product_id": "MON-001", "name": "UltraView 4K 27-inch", "price": 599.00,
             "specs": "4K 60Hz, IPS, HDR400", "rating": 4.7, "stock": "in_stock"},
            {"product_id": "MON-002", "name": "ProDisplay 32-inch", "price": 799.00,
             "specs": "4K 75Hz, IPS, HDR600, USB-C", "rating": 4.9, "stock": "in_stock"}
        ],
        "keyboards": [
            {"product_id": "KEY-001", "name": "MechPro RGB", "price": 149.00,
             "specs": "Mechanical, Cherry MX Brown, RGB", "rating": 4.8, "stock": "in_stock"},
            {"product_id": "KEY-002", "name": "SilentType Pro", "price": 89.00,
             "specs": "Membrane, Quiet, Wireless", "rating": 4.5, "stock": "in_stock"}
        ]
    }

    category_lower = category.lower()
    if category_lower in catalogs:
        return json.dumps({"category": category, "products": catalogs[category_lower]})

    return json.dumps({"error": f"Category '{category}' not found"})


def calculate_discount(customer_id: str, total_amount: float) -> str:
    """Calculate applicable discounts."""
    _tool_call_log.append("calculate_discount")

    if customer_id == "CUST-001":
        discounts = []
        total_discount = 0.0

        if total_amount > 500:
            premium_discount = total_amount * 0.10
            discounts.append({"type": "premium_tier", "name": "Premium Member 10% Discount",
                            "amount": round(premium_discount, 2)})
            total_discount += premium_discount

        if total_amount > 1000:
            loyalty_discount = total_amount * 0.05
            discounts.append({"type": "loyalty_bonus", "name": "Loyal Customer 5% Bonus",
                            "amount": round(loyalty_discount, 2)})
            total_discount += loyalty_discount

        return json.dumps({
            "customer_id": customer_id,
            "original_amount": total_amount,
            "discounts": discounts,
            "total_discount": round(total_discount, 2),
            "final_amount": round(total_amount - total_discount, 2)
        })

    return json.dumps({"customer_id": customer_id, "original_amount": total_amount,
                      "discounts": [], "total_discount": 0.0, "final_amount": total_amount})


def check_inventory(product_id: str) -> str:
    """Check product availability."""
    _tool_call_log.append("check_inventory")

    inventory = {
        "LAP-001": {"stock": 47, "status": "in_stock", "delivery": "1-2 business days"},
        "LAP-002": {"stock": 32, "status": "in_stock", "delivery": "1-2 business days"},
        "LAP-003": {"stock": 8, "status": "low_stock", "delivery": "2-3 business days"},
        "MON-001": {"stock": 156, "status": "in_stock", "delivery": "1-2 business days"},
        "MON-002": {"stock": 89, "status": "in_stock", "delivery": "1-2 business days"},
        "KEY-001": {"stock": 203, "status": "in_stock", "delivery": "1-2 business days"},
        "KEY-002": {"stock": 145, "status": "in_stock", "delivery": "1-2 business days"}
    }

    if product_id in inventory:
        return json.dumps({"product_id": product_id, **inventory[product_id]})

    return json.dumps({"product_id": product_id, "status": "not_found"})


# --- API Endpoints ---

@app.post("/call_tool", response_model=ToolResponse)
async def call_tool(request: ToolRequest):
    """Call a tool with arguments."""
    tool_map = {
        "get_customer": get_customer,
        "get_orders": get_orders,
        "search_knowledge_base": search_knowledge_base,
        "process_refund": process_refund,
        "escalate_to_human": escalate_to_human,
        "get_product_catalog": get_product_catalog,
        "calculate_discount": calculate_discount,
        "check_inventory": check_inventory
    }

    if request.tool not in tool_map:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool}' not found")

    try:
        result = tool_map[request.tool](**request.arguments)
        return ToolResponse(result=json.loads(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {
        "tools": [
            {"name": "get_customer", "description": "Look up customer profile by ID"},
            {"name": "get_orders", "description": "Retrieve all orders for a customer"},
            {"name": "search_knowledge_base", "description": "Search knowledge base"},
            {"name": "process_refund", "description": "Process a refund"},
            {"name": "escalate_to_human", "description": "Escalate to human support"},
            {"name": "get_product_catalog", "description": "Get product catalog"},
            {"name": "calculate_discount", "description": "Calculate discounts"},
            {"name": "check_inventory", "description": "Check product availability"}
        ]
    }


@app.get("/tool_log")
async def get_tool_log():
    """Get tool call log."""
    return {"log": _tool_call_log.copy()}


@app.post("/reset_log")
async def reset_log():
    """Reset tool call log."""
    _tool_call_log.clear()
    return {"status": "cleared"}


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
