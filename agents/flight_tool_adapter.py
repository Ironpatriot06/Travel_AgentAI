from langchain.tools import tool
import re
from agents.flight_agent import search_flights

@tool
def flight_tool_adapter(state: dict) -> str:
    """
    Extracts flight query parameters from user input and returns search results.
    Requires: origin, destination, date. Optional: budget, passengers.
    """
    user_input = state.get("input", "")
    print("🛫 Tool invoked with input:", user_input)

    origin = re.search(r"\bfrom\s+([A-Z]{3})\b", user_input.upper())
    destination = re.search(r"\bto\s+([A-Z]{3})\b", user_input.upper())
    date = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", user_input)

    passengers_match = re.search(r"\b(\d+)\s*(people|adults|travellers?)", user_input.lower())
    budget_match = re.search(r"\b(\d{4,6})\s*(INR|₹|USD|\$|AED)?\b", user_input.upper())

    if not (origin and destination and date):
        return "Before I can show you flights, please provide origin, destination, and date (YYYY-MM-DD)."

    passengers = int(passengers_match.group(1)) if passengers_match else 1
    budget = int(budget_match.group(1)) if budget_match else None

    return search_flights(
        origin=origin.group(1),
        destination=destination.group(1),
        date=date.group(1),
        passengers=passengers,
        budget=budget
    )
