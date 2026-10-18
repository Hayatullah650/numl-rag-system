
import chromadb
from sentence_transformers import SentenceTransformer
from chunking import chunk_documents
from ingest import ingest_pdfs

DB_DIR = "chroma_db"
COLLECTION_NAME = "numl_documents"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():
    pages = ingest_pdfs()
    chunks = chunk_documents(pages)

    if not chunks:
        print("No chunks available.")
        return

    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=DB_DIR)

    existing = [
        item.name for item in client.list_collections()
    ]

    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(COLLECTION_NAME)

    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        embeddings = model.encode(
            [chunk["text"] for chunk in batch],
            normalize_embeddings=True
        ).tolist()

        collection.add(
            ids=[f"chunk_{chunk['chunk_id']}" for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "chunk_id": chunk["chunk_id"]
                }
                for chunk in batch
            ]
        )

    print(f"\nStored chunks: {collection.count()}")
    print(f"Database location: {DB_DIR}")


if __name__ == "__main__":
    build_vector_store()
