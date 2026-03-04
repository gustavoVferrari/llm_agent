import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine, text
from app.config import settings
from app.rag.embeddings import get_embedding

engine = create_engine(settings.DATABASE_URL)

def retrieve_context(query: str, top_k: int = 5):
    query_embedding = get_embedding(query)

    sql = text("""
        SELECT content, metadata,
               embedding <-> :embedding AS distance
        FROM documents
        ORDER BY embedding <-> :embedding
        LIMIT :top_k
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {
            "embedding": query_embedding,
            "top_k": top_k
        })
        return [dict(row._mapping) for row in result]