
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

DB_DIR = "chroma_db"
COLLECTION_NAME = "numl_documents"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

embedding_model = SentenceTransformer(EMBEDDING_MODEL)
reranker = CrossEncoder(RERANKER_MODEL)


def retrieve_documents(question: str, top_k: int = 5) -> list[dict]:
    client = chromadb.PersistentClient(path=DB_DIR)

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        return []

    count = collection.count()
    if count == 0:
        return []

    query_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(20, count)
    )

    candidates = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if not text:
            continue

        candidates.append({
            "text": text,
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", "?"),
            "distance": round(float(distance), 4)
        })

    if not candidates:
        return []

    pairs = [(question, item["text"]) for item in candidates]
    scores = reranker.predict(pairs)

    for item, score in zip(candidates, scores):
        item["rerank_score"] = round(float(score), 4)

    candidates.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return candidates[:top_k]

if __name__ == "__main__":
    import chromadb

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.get(
        where={"source": "fee refund.pdf"},
        include=["documents", "metadatas"]
    )

    print(f"Refund PDF chunks found: {len(results['documents'])}")

    for index, (text, metadata) in enumerate(
        zip(results["documents"], results["metadatas"]), start=1
    ):
        print(f"\nChunk {index} | Page {metadata.get('page')}")
        print(text[:1200])
        print("-" * 60)
