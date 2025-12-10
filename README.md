# AI Workflow Engine (FastAPI)

Small backend project for running AI-style workflows as graphs.

Two example workflows:

1. **Summarize text** – split → summarize → merge → refine (with looping if too long)
2. **Code review** – extract → check complexity → detect issues → improve (loop until quality is OK)

---

## How to run

```bash
cd ai-engine
pip install fastapi uvicorn
uvicorn app.main:app --reload
