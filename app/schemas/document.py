from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    content: str
    topic: str

class IngestResponse(BaseModel):
    message: str
    id: Optional[str] = None

class RAGRequest(BaseModel):
    query: str
    match_threshold: Optional[float] = 0.5
    match_count: Optional[int] = 5

class RAGResponse(BaseModel):
    answer: str
    context_used: List[str]