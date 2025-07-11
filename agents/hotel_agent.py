# agents/hotel_agent.py
from langchain.tools import StructuredTool

def search_hotels(city: str, checkin: str, checkout: str, budget: int) -> str:
    return f"🏨 Sample hotels in {city} from {checkin} to {checkout} under ₹{budget}"

hotel_tool = StructuredTool.from_function(
    func=search_hotels,
    name="HotelSearch",
    description="Search hotels in a city with dates and budget",
    return_direct=True,
)
