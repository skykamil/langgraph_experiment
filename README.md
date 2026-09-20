# LangGraph Experiment

Small learning project for understanding LangGraph state, nodes, edges, conditional routing, and tool loops.

## Current scope

Session 1: a minimal offline `StateGraph` with typed state, nodes, edges, and conditional routing.

Session 2: a model-driven tool loop using `ChatOpenAI`, LangGraph state with message history, conditional routing, a local tool, and a return to the model for the final answer.

Session 3: added a recursion limit, local behavior checks, and compared the LangGraph flow with a manually orchestrated tool loop.

## Configuration

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

`graph.py` runs offline without an API key. `tool_loop.py` requires a valid key and makes paid API calls. The local behavior checks do not call the API, but importing `tool_loop.py` initializes the model client, so a key must still be configured.

Run locally:

```bash
python3 -m pip install -r requirements.txt
python3 graph.py
python3 tool_loop.py
```
## Checks

Run the local behavior checks:

```bash
python3 test_tool_loop.py
```
The checks cover:

- routing to `END` when no tool call is present;
- routing to the tool node when a tool call is present;
- execution of the local tool;
- handling multiple tool calls returned in one model response;
- matching each `ToolMessage` to the correct `tool_call_id`.

The recursion safeguard was also verified manually by lowering `recursion_limit` to `2` and confirming that LangGraph raised `GraphRecursionError`.

## Comparison with manual orchestration

In Patent Agent, a Python loop explicitly controls model calls, tool execution, and continuation. In this experiment, LangGraph executes that flow through nodes and edges, while conditional routing selects tool execution or completion.

The `add_messages` reducer merges message updates into the graph state. Tool execution and matching results to `tool_call_id` remain implemented in application code. LangGraph provides a recursion limit, but retry policies, error handling, and persistence still require explicit configuration or implementation.

## Known limitations

- The experiment uses only one local tool.
- Tool execution is intentionally implemented manually instead of using a prebuilt `ToolNode`.
- Unknown tool names are not handled explicitly.
- There is no persistence or checkpointing.
- There is no frontend, database, deployment, or production error handling.
