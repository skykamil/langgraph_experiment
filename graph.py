from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    text: str
    length: int
    category: str

def measure_text(state: GraphState):
    return {"length": len(state["text"])}

def classify_text(state: GraphState):
    if state["length"] <= 5:
        category = "short"
    else:
        category = "long"
    return category

def handle_short(state: GraphState):
    return {"category": "short"}

def handle_long(state: GraphState):
    return {"category": "long"}

builder = StateGraph(GraphState)

builder.add_node("measure_text", measure_text)
builder.add_node("handle_short", handle_short)
builder.add_node("handle_long", handle_long)

builder.add_conditional_edges(
    "measure_text",
    classify_text,
    {
        "short": "handle_short",
        "long": "handle_long",
    }
)

builder.add_edge(START, "measure_text")
builder.add_edge("handle_short", END)
builder.add_edge("handle_long", END)

graph = builder.compile()

initial_state: GraphState = {
    "text": "hello",
    "length": 0,
    "category": ""
}

result = graph.invoke(initial_state)

print(result)
