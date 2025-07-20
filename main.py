from agents import Agent, Runner, function_tool
from connection import config
import requests
import os
import rich

# Get API URL from environment or default
API_URL = os.getenv("API_URL", "https://your-api-url.com/products")

# Custom tool to get products by name and price
@function_tool
def get_products(name: str = "", price: int = None) -> dict:
    """
    Fetch products filtered by optional name and max price.
    """
    try:
        params = {}
        if name:
            params["search"] = name

        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        products = response.json()

        # Apply price filtering if provided
        if price is not None:
            products = [p for p in products if p.get("price", 0) <= price]

        # Return structured product info
        product_info = [
            {"name": p.get("name", "N/A"), "price": p.get("price", "N/A")}
            for p in products
        ]

        return {"products": product_info}

    except Exception as e:
        return {"error": str(e)}

# Define the shopping agent
agent = Agent(
    name="shopping-agent",
    instructions="You are a shopping assistant. Help users find products by name or maximum price. Extract 'name' and 'price' from the user's query.",
    tools=[get_products]
)

# Natural language query
query = "Show me wood chairs under 2000"

# Run the agent synchronously
result = Runner.run_sync(agent, query, run_config=config)

# Display structured response
rich.print("[bold green]🛍 Agent JSON Response:[/bold green]")
rich.print(result.new_items)

# Final response to user
print("[FINAL OUTPUT]:", result.final_output)
