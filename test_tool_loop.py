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

state_with_two_tools: GraphState = {
    "messages": [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "lookup_case_status",
                    "args": {"case_id": "CASE-001"},
                    "id": "test-call-1",
                    "type": "tool_call",
                },
                {
                    "name": "lookup_case_status",
                    "args": {"case_id": "CASE-002"},
                    "id": "test-call-2",
                    "type": "tool_call",
                },
            ],
        )
    ]
}

two_tool_result = run_tool(state_with_two_tools)

assert two_tool_result is not None
assert len(two_tool_result["messages"]) == 2
assert two_tool_result["messages"][0].content == "pending"
assert two_tool_result["messages"][1].content == "granted"
assert two_tool_result["messages"][0].tool_call_id == "test-call-1"
assert two_tool_result["messages"][1].tool_call_id == "test-call-2"
