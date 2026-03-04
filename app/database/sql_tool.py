from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

FORBIDDEN_KEYWORDS = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER"]

def validate_sql(query: str):
    upper_query = query.upper()
    if any(word in upper_query for word in FORBIDDEN_KEYWORDS):
        raise ValueError("Operação não permitida.")
    if not upper_query.strip().startswith("SELECT"):
        raise ValueError("Apenas SELECT permitido.")

def execute_sql(query: str):
    validate_sql(query)

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]