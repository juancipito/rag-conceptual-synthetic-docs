# RAG Conceptual Architecture

1. Ingest synthetic policy notes.
2. Split documents into small chunks.
3. Create retrievable text vectors with TF-IDF for a local demo.
4. Retrieve top chunks for a user question.
5. Return citations so the answer can be checked.
6. Evaluate retrieval by asking whether the expected document appears in the top results.

This is intentionally not a production vector database. It is a junior-friendly concept demo.
