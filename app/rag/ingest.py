import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine, text
from app.config import settings
from app.rag.embeddings import get_embedding
import json


print(settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL)

def insert_document(content: str, metadata: dict):

    embedding = get_embedding(content)

    sql = text("""
        INSERT INTO documents (content, metadata, embedding)
        VALUES (:content, :metadata, :embedding)
    """)

    with engine.begin() as conn:
        conn.execute(sql, {
            "content": content,
            "metadata": json.dumps(metadata),
            "embedding": embedding
        })

    print("Documento inserido com sucesso!")