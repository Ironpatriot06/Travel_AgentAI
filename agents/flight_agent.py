# agents/flight_agent.py

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional
import requests


# 🔐 Securely store or load these from env vars instead
AMADEUS_CLIENT_ID = "9CK1VIQVVnQNyMaGxhRzEXlFAGAMvyGf"
AMADEUS_CLIENT_SECRET = "LTIzChn6X3OX0wKk"

def get_amadeus_access_token(client_id, client_secret):
    response = requests.post(
        "https://test.api.amadeus.com/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )
    return response.json()["access_token"]

def search_flights(
    origin: str,
    destination: str,
    date: str,
    budget: Optional[int] = None,
    passengers: int = 1
) -> str:
    token = get_amadeus_access_token(AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET)

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": passengers,
        "currencyCode": "INR",
        "max": 5
    }

    response = requests.get(
        "https://test.api.amadeus.com/v2/shopping/flight-offers",
        headers={"Authorization": f"Bearer {token}"},
        params=params
    )

    data = response.json()
    flights = []
    for offer in data.get("data", []):
        price = offer["price"]["total"]
        carrier = offer["validatingAirlineCodes"][0]
        flights.append(f"🛫 {carrier} - ₹{price}")
    if not data.get("data"):
        return "No flights found via Amadeus API."

    return "\n".join(flights) if flights else "No flights found."
