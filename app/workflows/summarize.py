def split_text(state):
    text = state["text"]
    chunk_size = 200

    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    state["chunks"] = chunks
    return state


def generate_summaries(state):
    summaries = []
    for c in state["chunks"]:
        sentences = c.split(".")
        summaries.append(". ".join(sentences[:2]) + ".")
    state["summaries"] = summaries
    return state


def merge_summaries(state):
    summary = " ".join(state["summaries"])
    state["merged_summary"] = summary
    return state


def refine_summary(state):
    summary = state["merged_summary"]
    words = summary.split()
    refined = [w for w in words if len(w) < 10]
    state["refined_summary"] = " ".join(refined)
    return state
