import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from openai import OpenAI
from app.config import settings
from app.agents.prompts import SYSTEM_PROMPT
from app.rag.retriever import retrieve_context
from app.database.sql_tool import execute_sql
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def agent_loop(user_input: str):

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    decision = json.loads(content)

    if decision["action"] == "rag":
        docs = retrieve_context(decision["query"])
        return {
            "type": "rag",
            "data": docs
        }

    elif decision["action"] == "sql":
        result = execute_sql(decision["query"])
        return {
            "type": "sql",
            "data": result
        }

    else:
        return {
            "type": "final",
            "data": decision.get("query")
        }