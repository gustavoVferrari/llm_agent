import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.orchestrator import agent_loop

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(request: QueryRequest):
    result = agent_loop(request.question)
    return result

# http://127.0.0.1:8000/docs