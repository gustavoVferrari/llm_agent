import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from supabase import create_client
from app.config import settings
from app.rag.embeddings import get_embedding

def insert_document(content: str, metadata: dict):

    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )

    embedding = get_embedding(content)

    data = {
        "content": content,
        "metadata": metadata,
        "embedding": embedding
    }

    response = supabase.table("documents").insert(data).execute()

    print("Documento inserido!")
    print(response)


if __name__ == "__main__":

    doc = """
    Política de Reembolso:
    O cliente pode solicitar reembolso em até 30 dias após a compra.
    O valor será devolvido integralmente caso o produto não tenha sido utilizado.
    """

    metadata = {
        "source": "manual_interno",
        "category": "financeiro"
    }

    insert_document(doc, metadata)