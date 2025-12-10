# app/main.py
from fastapi import FastAPI
import uuid

from app.graph_engine import GRAPHS, RUNS, Graph, Node
from app.schemas import SummarizeBody, CodeReviewBody
from app.workflows.summarize import (
    split_text,
    generate_summaries,
    merge_summaries,
    refine_summary,
)
from app.workflows.code_review import (
    extract_functions,
    check_complexity,
    detect_issues,
    suggest_improvements,
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI workflow engine is running 🚀",
        "workflows": [
            "summarize",
            "code_review",
        ],
        "docs": "/docs",
    }


# ---------- helpers to build graphs ----------


def build_summarize_graph():
    nodes = {
        "split": Node("split", split_text),
        "summaries": Node("summaries", generate_summaries),
        "merge": Node("merge", merge_summaries),
        "refine": Node("refine", refine_summary),
    }

    edges = {
        "split": "summaries",
        "summaries": "merge",
        "merge": "refine",
        "refine": None,
    }

    # loop if refined summary is still too long
    loop_config = {
        "loop_node": "refine",
        "restart_from": "split",
        "max_loops": 5,
        "condition": lambda state: len(
            state.get("refined_summary", "")
        ) > state.get("max_length", 200),
    }

    return Graph(nodes, edges, loop_config=loop_config)


def build_code_review_graph():
    nodes = {
        "extract": Node("extract", extract_functions),
        "complexity": Node("complexity", check_complexity),
        "detect": Node("detect", detect_issues),
        "improve": Node("improve", suggest_improvements),
    }

    edges = {
        "extract": "complexity",
        "complexity": "detect",
        "detect": "improve",
        "improve": None,
    }

    loop_config = {
        "loop_node": "improve",
        "restart_from": "extract",
        "max_loops": 3,
        "condition": lambda state: state.get("quality_score", 0) < state.get(
            "threshold", 7
        ),
    }

    return Graph(nodes, edges, loop_config=loop_config)


# ---------- create graphs ----------


@app.post("/graph/create/summarize")
def create_summarize_graph():
    graph = build_summarize_graph()
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = graph
    return {"graph_id": graph_id, "workflow": "summarize"}


@app.post("/graph/create/code-review")
def create_code_review_graph():
    graph = build_code_review_graph()
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = graph
    return {"graph_id": graph_id, "workflow": "code_review"}


# ---------- run graphs ----------


@app.post("/graph/run/summarize")
def run_summarize(graph_id: str, body: SummarizeBody):
    graph = GRAPHS[graph_id]
    initial_state = body.model_dump()
    final_state, log = graph.run(initial_state)

    run_id = str(uuid.uuid4())
    RUNS[run_id] = final_state

    return {"run_id": run_id, "workflow": "summarize", "final_state": final_state, "log": log}


@app.post("/graph/run/code-review")
def run_code_review(graph_id: str, body: CodeReviewBody):
    graph = GRAPHS[graph_id]
    initial_state = body.model_dump()
    final_state, log = graph.run(initial_state)

    run_id = str(uuid.uuid4())
    RUNS[run_id] = final_state

    return {"run_id": run_id, "workflow": "code_review", "final_state": final_state, "log": log}


# ---------- fetch stored state ----------


@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    return RUNS.get(run_id, {})
