import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="RAG API - FastAPI, OpenAI & Supabase",
    description="MVP de uma API de Retrieval-Augmented Generation (RAG) para ingestão e busca semântica.",
    version="1.0.0"
)

# Inclui os endpoints da API
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de RAG! Acesse /docs para documentação Swagger."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)