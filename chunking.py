
from ingest import ingest_pdfs

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text: str) -> list[str]:
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        while len(paragraph) > CHUNK_SIZE:
            if current:
                chunks.append(current)
                current = ""

            split_at = paragraph.rfind(" ", 0, CHUNK_SIZE)

            if split_at < CHUNK_SIZE // 2:
                split_at = CHUNK_SIZE

            chunks.append(paragraph[:split_at].strip())
            paragraph = paragraph[max(0, split_at - CHUNK_OVERLAP):].strip()

        candidate = f"{current}\n{paragraph}".strip()

        if len(candidate) <= CHUNK_SIZE:
            current = candidate
        else:
            if current:
                chunks.append(current)

            overlap = current[-CHUNK_OVERLAP:] if current else ""
            current = f"{overlap}\n{paragraph}".strip()

            if len(current) > CHUNK_SIZE:
                current = current[-CHUNK_SIZE:]

    if current:
        chunks.append(current)

    return chunks


def chunk_documents(pages: list[dict]) -> list[dict]:
    chunks = []

    for page in pages:
        for text in split_text(page["text"]):
            chunks.append({
                "text": text,
                "source": page["source"],
                "page": page["page"],
                "chunk_id": len(chunks)
            })

    return chunks


if __name__ == "__main__":
    pages = ingest_pdfs()
    chunks = chunk_documents(pages)

    print(f"\nPages processed: {len(pages)}")
    print(f"Total chunks: {len(chunks)}")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0]["text"])
        print(f"Source: {chunks[0]['source']}")
        print(f"Page: {chunks[0]['page']}")
