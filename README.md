# LangGraph Experiment

Small learning project for understanding LangGraph state, nodes, edges, conditional routing, and tool loops.

## Current scope

Session 1: a minimal offline `StateGraph` with typed state, nodes, edges, and conditional routing.

Session 2: a model-driven tool loop using `ChatOpenAI`, LangGraph state with message history, conditional routing, a local tool, and a return to the model for the final answer.

Session 3: added a recursion limit, local behavior checks, and compared the LangGraph flow with a manually orchestrated tool loop.

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

## Known limitations

- The experiment uses only one local tool.
- Tool execution is intentionally implemented manually instead of using a prebuilt `ToolNode`.
- Unknown tool names are not handled explicitly.
- There is no persistence or checkpointing.
- There is no frontend, database, deployment, or production error handling.
