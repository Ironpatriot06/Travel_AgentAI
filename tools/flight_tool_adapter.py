from langchain.tools import tool
import re

@tool
def flight_tool_adapter(state: dict) -> str:
    """Handles flight search queries from user text input."""
    user_input = state.get("input", "")
    print("🛫 Tool invoked with input:", user_input)

    # Match 3-letter IATA codes
    origin_match = re.search(r"from\s+([A-Z]{3})", user_input.upper())
    destination_match = re.search(r"to\s+([A-Z]{3})", user_input.upper())
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", user_input)
    passengers = extracted_passengers or 1


    if not (origin_match and destination_match and date_match):
        return "Please provide origin, destination, and date in YYYY-MM-DD format."

    origin = origin_match.group(1)
    destination = destination_match.group(1)
    date = date_match.group(1)

    from agents.flight_agent import search_flights
    return search_flights(origin, destination, date)
