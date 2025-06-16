import os
import requests
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel, Field

# 🔐 API key setup
os.environ["GOOGLE_API_KEY"] = "your-google-api-key"
GOOGLE_FLIGHTS_API_KEY = "your-rapidapi-key"

# 🛫 Define the flight search function
def search_flights(origin: str, destination: str, date: str, budget: str = None) -> str:
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"
    headers = {
        "X-RapidAPI-Key": GOOGLE_FLIGHTS_API_KEY,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    params = {
        "sourceAirportCode": origin,
        "destinationAirportCode": destination,
        "date": date,
        "itineraryType": "ONE_WAY",
        "sortOrder": "PRICE",
        "numAdults": "1",
        "currencyCode": "INR"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get("data", {}).get("flights", [])
        if not results:
            return "No flights found. Try changing your date or location."

        flight_options = []
        for i, flight in enumerate(results[:3]):  # Top 3 results
            price = flight.get("purchaseLinks", [{}])[0].get("totalPrice", {}).get("formatted", "N/A")
            airline = flight.get("segments", [{}])[0].get("flightLegs", [{}])[0].get("marketingCarrier", {}).get("displayName", "N/A")
            departure_time = flight.get("segments", [{}])[0].get("flightLegs", [{}])[0].get("departureDateTime", "N/A")
            flight_options.append(f"Option {i+1}: {airline}, Departs: {departure_time}, Price: {price}")

        return "\n".join(flight_options)

    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

# 📦 Define input schema for the tool
class FlightSearchInput(BaseModel):
    origin: str = Field(..., description="IATA code of the origin airport (e.g., DEL)")
    destination: str = Field(..., description="IATA code of the destination airport (e.g., DXB)")
    date: str = Field(..., description="Travel date in YYYY-MM-DD format")
    budget: str = Field(None, description="Maximum budget in INR (optional)")

# 🛠️ Tool setup
flight_tool = StructuredTool.from_function(
    name="search_flights",
    description="Searches for flights between two cities on a given date.",
    func=search_flights,
    args_schema=FlightSearchInput
)

# 🤖 LLM Setup
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

# 🧠 Agent Initialization
agent = initialize_agent(
    tools=[flight_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

