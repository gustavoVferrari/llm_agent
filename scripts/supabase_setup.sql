-- Habilita a extensão pgvector para armazenamento e busca de embeddings vetoriais
CREATE EXTENSION IF NOT EXISTS vector;

-- Cria a tabela 'documents' para armazenar o conteúdo, seus embeddings e o tópico
CREATE TABLE documents (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL, -- O tamanho do embedding para text-embedding-3-small é 1536
    topic TEXT
);

-- Cria um índice HNSW para a coluna de embedding para otimizar a busca de vizinhos mais próximos
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Cria a função RPC 'match_documents' para realizar a busca semântica
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding vector(1536),
    match_threshold FLOAT,
    match_count INT
) RETURNS TABLE (
    id uuid,
    content TEXT,
    topic TEXT,
    similarity FLOAT
) LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        documents.id,
        documents.content,
        documents.topic,
        1 - (documents.embedding <=> query_embedding) AS similarity
    FROM
        documents
    WHERE
        1 - (documents.embedding <=> query_embedding) > match_threshold
    ORDER BY
        documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;