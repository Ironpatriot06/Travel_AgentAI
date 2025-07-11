# orchestrator.py

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt.tool_node import ToolNode
from agents.hotel_agent import hotel_tool
from agents.itinerary_agent import get_itinerary_tool
from agents.flight_tool_adapter import flight_tool_adapter

class GraphState(TypedDict):
    input: str
    result: str

def get_orchestrator(qa_chain):
    itinerary_tool = get_itinerary_tool(qa_chain)

    def start_node(state: GraphState) -> GraphState:
        return {"input": state["input"], "result": ""}

    def router(state: GraphState) -> str:
        text = state["input"].lower()
        print("🧭 Routing input:", text)
        if any(word in text for word in ["flight", "plane", "ticket", "fare"]):
            return "flight_tool"
        if "hotel" in text:
            return "hotel_tool"
        return "itinerary_tool"


    graph = StateGraph(GraphState)

    graph.add_node("start", start_node)
    graph.add_node("flight_tool", ToolNode([flight_tool_adapter]))
    graph.add_node("hotel_tool", ToolNode([hotel_tool]))
    graph.add_node("itinerary_tool", ToolNode([itinerary_tool]))

    graph.set_entry_point("start")
    graph.add_conditional_edges("start", router)
    for node in ["flight_tool", "hotel_tool", "itinerary_tool"]:
        graph.add_edge(node, END)

    return graph.compile()
