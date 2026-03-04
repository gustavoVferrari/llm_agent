import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from supabase import create_client, Client
from app.core.config import settings

# Inicializa o cliente Supabase
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY
)

def insert_document(content: str, embedding: list[float], topic: str):
    """
    Insere um documento na tabela 'documents' do Supabase.
    """
    data = {
        "content": content,
        "embedding": embedding,
        "topic": topic
    }
    response = supabase.table("documents").insert(data).execute()
    return response.data

def search_documents(query_embedding: list[float], match_threshold: float = 0.5, match_count: int = 5):
    """
    Realiza busca semântica utilizando a função RPC 'match_documents' no Supabase.
    """
    rpc_params = {
        "query_embedding": query_embedding,
        "match_threshold": match_threshold,
        "match_count": match_count
    }
    response = supabase.rpc("match_documents", rpc_params).execute()
    return response.data