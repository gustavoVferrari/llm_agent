# RAG API com FastAPI, OpenAI e Supabase

Este projeto implementa uma API de Retrieval-Augmented Generation (RAG) utilizando FastAPI para a estrutura da API, OpenAI para geração de embeddings e respostas, e Supabase como banco de dados vetorial e relacional. O objetivo é fornecer um MVP funcional, modular e escalável para ingestão de documentos, busca semântica e geração de respostas contextualizadas.

## Arquitetura do Projeto

A arquitetura do projeto é dividida em módulos lógicos para garantir a separação de responsabilidades, manutenibilidade e escalabilidade. A estrutura de diretórios reflete essa modularidade:

```
rag_api/
├── app/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da aplicação FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py    # Definição dos endpoints da API (ingestão, busca RAG)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py       # Configurações da aplicação (variáveis de ambiente)
│   │   ├── embeddings.py   # Lógica para geração de embeddings com OpenAI
│   │   ├── database.py     # Conexão e operações com Supabase (PostgreSQL)
│   │   └── llm.py          # Lógica para interação com o modelo GPT-4o-mini
│   └── schemas/
│       ├── __init__.py
│       └── document.py     # Modelos Pydantic para validação de dados (Documento, Requisições, Respostas)
├── scripts/
│   └── supabase_setup.sql  # Script SQL para configurar o Supabase (tabela documents, função match_documents)
├── .env.example            # Exemplo de arquivo de variáveis de ambiente
├── requirements.txt        # Dependências do projeto Python
└── README.md               # Documentação do projeto
```

## Módulos e Responsabilidades

### `app/main.py`

Define a aplicação FastAPI principal, incluindo a montagem dos roteadores de API definidos em `app/api/endpoints.py`.

### `app/api/endpoints.py`

Contém as definições dos endpoints da API:
- **`/ingest` (POST)**: Para ingestão de novos textos, categorização por tópico, geração de embeddings e armazenamento no Supabase.
- **`/rag` (POST)**: Para realizar busca semântica no Supabase e gerar uma resposta contextualizada usando o modelo GPT-4o-mini.

### `app/core/config.py`

Gerencia as configurações da aplicação, carregando variáveis de ambiente necessárias para chaves de API (OpenAI, Supabase) e URLs de serviço.

### `app/core/embeddings.py`

Encapsula a lógica para interagir com a API de embeddings da OpenAI, utilizando o modelo `text-embedding-3-small` para transformar textos em vetores numéricos.

### `app/core/database.py`

Responsável pela conexão com o Supabase (PostgreSQL) e pelas operações de banco de dados, como inserção de documentos e execução da função RPC `match_documents` para busca vetorial.

### `app/core/llm.py`

Contém a lógica para interagir com o modelo de linguagem `gpt-4o-mini` da OpenAI, formatando prompts e garantindo que as respostas sejam geradas exclusivamente com base no contexto fornecido pela busca RAG.

### `app/schemas/document.py`

Define os modelos de dados Pydantic para as requisições e respostas da API, garantindo a validação e serialização/desserialização dos dados. Inclui modelos para `Document` (estrutura do documento a ser armazenado), `IngestRequest`, `IngestResponse`, `RAGRequest` e `RAGResponse`.

### `scripts/supabase_setup.sql`

Contém o script SQL necessário para configurar o banco de dados no Supabase, incluindo a criação da tabela `documents` com a coluna de vetor e a função `match_documents` para busca semântica.

## Próximos Passos

1. Configurar as variáveis de ambiente no arquivo `.env`.
2. Instalar as dependências Python listadas em `requirements.txt`.
3. Executar o script `supabase_setup.sql` no seu projeto Supabase.
4. Iniciar a aplicação FastAPI.
5. Testar os endpoints de ingestão e RAG.
