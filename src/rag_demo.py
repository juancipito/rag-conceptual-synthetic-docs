from pathlib import Path
import sys

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_synthetic_data.csv"


def chunk_documents(df: pd.DataFrame) -> pd.DataFrame:
    chunks = []
    for _, row in df.iterrows():
        sentences = [part.strip() for part in row["text"].split(".") if part.strip()]
        for idx, sentence in enumerate(sentences, start=1):
            chunks.append(
                {
                    "chunk_id": f"{row['doc_id']}-C{idx}",
                    "doc_id": row["doc_id"],
                    "title": row["title"],
                    "text": sentence,
                }
            )
    return pd.DataFrame(chunks)


def retrieve(query: str, chunks: pd.DataFrame, top_k: int = 3) -> pd.DataFrame:
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks["text"])
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    ranked = chunks.copy()
    ranked["score"] = scores
    return ranked.sort_values("score", ascending=False).head(top_k)


def main() -> None:
    query = " ".join(sys.argv[1:]) or "How should adherence exceptions be documented?"
    docs = pd.read_csv(DATA_PATH)
    chunks = chunk_documents(docs)
    results = retrieve(query, chunks)
    print(f"Query: {query}\n")
    for _, row in results.iterrows():
        print(f"{row['chunk_id']} | {row['title']} | score={row['score']:.3f}")
        print(f"  {row['text']}")


if __name__ == "__main__":
    main()
