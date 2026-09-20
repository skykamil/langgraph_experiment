from langchain_core.messages import AIMessage, ToolMessage
from tool_loop import route_after_model, GraphState, run_tool

state: GraphState = {
    "messages": [AIMessage(content="Hello!")]
}

assert route_after_model(state) == "end"

state_with_tool: GraphState = {
    "messages": [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "lookup_case_status",
                    "args": {"case_id": "CASE-002"},
                    "id": "test-call-1",
                    "type": "tool_call",
                }
            ],
        )
    ]
}

assert route_after_model(state_with_tool) == "tool"

tool_result = run_tool(state_with_tool)

assert tool_result is not None
assert tool_result["messages"][0].content == "granted"
tool_message = tool_result["messages"][0]

assert isinstance(tool_message, ToolMessage)
assert tool_message.tool_call_id == "test-call-1"
