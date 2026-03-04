import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)

from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_rag_response(query: str, context: list[str]) -> str:
    """
    Gera uma resposta contextualizada utilizando o modelo gpt-4o-mini da OpenAI, 
    baseada exclusivamente no contexto recuperado.
    """
    context_text = "\n\n".join(context)
    
    prompt = f"""
Você é um assistente de IA especializado em responder perguntas com base exclusivamente no contexto fornecido abaixo.
Se a resposta não estiver contida no contexto, informe educadamente que não possui informações suficientes para responder.

Contexto:
{context_text}

Pergunta:
{query}

Resposta:
"""

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": "Você é um assistente útil que responde apenas com base no contexto fornecido."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()