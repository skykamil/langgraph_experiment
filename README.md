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
