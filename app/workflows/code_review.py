# app/workflows/code_review.py

def extract_functions(state):
    code = state["code"]
    # toy example: pretend we found two functions
    state["functions"] = ["func_one", "func_two"]
    return state


def check_complexity(state):
    code = state["code"]
    # toy complexity based on length
    complexity = min(10, max(1, len(code) // 50))
    state["complexity"] = complexity
    return state


def detect_issues(state):
    code = state["code"]
    issues = 0
    if "print(" in code:
        issues += 1
    if "TODO" in code:
        issues += 1
    state["issues"] = issues
    return state


def suggest_improvements(state):
    complexity = state.get("complexity", 5)
    issues = state.get("issues", 0)

    score = max(0, 10 - complexity - issues)
    state["quality_score"] = score

    suggestions = []

    if complexity > 5:
        suggestions.append("Refactor long or complex code into smaller functions.")
    if issues > 0:
        suggestions.append("Remove debug prints and TODO comments before committing.")
    if score >= 7:
        suggestions.append("Overall code quality looks good.")

    state["suggestions"] = suggestions
    return state
