from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()

model = ChatOpenAI(
    model="gpt-5.6-luna",
    use_responses_api=True
    )

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

@tool
def lookup_case_status(case_id: str) -> str:
    """Return the status of a patent case for a given case_id."""
    cases = {
            "CASE-001": "pending",
            "CASE-002": "granted",
            "CASE-003": "closed",
        }
    if case_id in cases:
        return cases[case_id]
    else:
        return "Case not found"

model_with_tools = model.bind_tools([lookup_case_status])

def call_model(state: GraphState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def route_after_model(state: GraphState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tool"
    return "end"

def run_tool(state: GraphState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]
        if tool_call["name"] == "lookup_case_status":
            status = lookup_case_status.invoke(tool_call["args"])
            tool_message = ToolMessage(content=status, tool_call_id=tool_call["id"])
            return {"messages": [tool_message]}

builder = StateGraph(GraphState)

builder.add_node("call_model", call_model)
builder.add_node("run_tool", run_tool)

builder.add_edge(START, "call_model")

builder.add_conditional_edges(
    "call_model",
    route_after_model,
    {
        "tool": "run_tool",
        "end": END
     },
)

builder.add_edge("run_tool", "call_model")

graph = builder.compile()

if __name__ == "__main__":

    initial_state: GraphState = {
        "messages": [HumanMessage(content="What is the status of CASE-002?")]
    }

    result = graph.invoke(
        initial_state,
        {"recursion_limit": 6},
    )

    print(result)
