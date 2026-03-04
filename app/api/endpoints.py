import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)


from fastapi import APIRouter, HTTPException
from app.schemas.document import IngestRequest, IngestResponse, RAGRequest, RAGResponse
from app.core.embeddings import generate_embedding
from app.core.database import insert_document, search_documents
from app.core.llm import generate_rag_response

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """
    Endpoint para ingestão de textos:
    1. Gera embedding do conteúdo.
    2. Armazena no Supabase com tópico.
    """
    try:
        embedding = generate_embedding(request.content)
        result = insert_document(request.content, embedding, request.topic)
        return IngestResponse(message="Documento ingerido com sucesso!", id=result[0].get("id") if result else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rag", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """
    Endpoint para RAG:
    1. Gera embedding da pergunta.
    2. Busca documentos similares no Supabase.
    3. Gera resposta contextualizada com GPT-4o-mini.
    """
    try:
        query_embedding = generate_embedding(request.query)
        matches = search_documents(query_embedding, request.match_threshold, request.match_count)
        
        if not matches:
            return RAGResponse(answer="Desculpe, não encontrei informações relevantes no meu banco de dados para responder à sua pergunta.", context_used=[])
        
        context_list = [match["content"] for match in matches]
        answer = generate_rag_response(request.query, context_list)
        
        return RAGResponse(answer=answer, context_used=context_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))