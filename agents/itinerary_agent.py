# agents/itinerary_agent.py
from langchain.tools import Tool

def get_itinerary_tool(qa_chain):
    def ask_itinerary(input: str) -> str:
        # Use dummy values or real session_state via injected context
        return qa_chain.run({
            "question": input,
            "num_days": "None",
            "child_age": "None",
            "budget": "None",
            "num_people": "None"
        })
    
    return Tool.from_function(
        func=ask_itinerary,
        name="ItineraryQA",
        description="Answer questions or generate itineraries using travel blog content",
        return_direct=True,
    )
