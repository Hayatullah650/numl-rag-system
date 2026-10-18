
import os
from dotenv import load_dotenv
from google import genai
from retrieval import retrieve_documents

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"


def answer_question(question: str) -> dict:
    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    try:
        documents = retrieve_documents(question, top_k=8)
    except Exception as e:
        print(f"Retrieval error: {type(e).__name__}: {e}")
        return {
            "answer": "Document retrieval failed. Please try again.",
            "sources": []
        }

    if not documents:
        return {
            "answer": "I could not find relevant information in the NUML documents.",
            "sources": []
        }

    question_lower = question.lower()
    refund_terms = (
        "refund", "fee refund", "tuition refund",
        "fee return", "withdraw", "withdrawal",
        "semester freeze", "cancel admission"
    )
    is_refund_question = any(
        term in question_lower for term in refund_terms
    )

    if is_refund_question:
        relevant_terms = (
            "refund", "refundable", "non-refundable",
            "tuition fee", "admission fee", "withdrawal",
            "semester freeze", "fee deduction",
            "percentage", "within days"
        )

        matching_documents = [
            doc for doc in documents
            if any(term in doc["text"].lower() for term in relevant_terms)
        ]

        if matching_documents:
            documents = matching_documents

    context = "\n\n".join(
        f"[Source: {doc['source']}, Page: {doc['page']}]\n{doc['text']}"
        for doc in documents
    )

    prompt = f"""
You are the NUML University information assistant.

Answer the user's exact question using only the supplied document context.

RULES:
1. Identify the specific policy requested before answering.
2. For fee refund questions, focus on fee refund, withdrawal,
   admission cancellation, and semester-freeze rules.
3. Do not present scholarships or sponsored fee reimbursement
   as refund rules unless the question specifically asks about them.
4. Do not confuse paying a fee, reimbursing a fee, and refunding a fee.
5. Do not invent fees, percentages, deadlines, or university policies.
6. Include conditions and deadlines only when supported by the context.
7. Cite every factual policy claim using [Source: filename, Page: number].
8. If the context does not establish the requested rule, clearly say
   the available retrieved passages do not provide enough information.
9. Keep the answer focused and easy to understand.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

Answer:
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        answer = (response.text or "").strip()

        if not answer:
            answer = (
                "The retrieved documents did not produce a usable answer. "
                "Please try rephrasing your question."
            )

    except Exception as e:
        print(f"Gemini error: {type(e).__name__}: {e}")
        return {
            "answer": "The answer service is temporarily unavailable. Please try again.",
            "sources": []
        }

    sources = []
    seen = set()

    for doc in documents:
        key = (doc["source"], doc["page"])
        if key not in seen:
            seen.add(key)
            sources.append({
                "source": doc["source"],
                "page": doc["page"]
            })

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    question = input("Ask NUML: ").strip()
    result = answer_question(question)

    print("\nAnswer:\n")
    print(result["answer"])
    print("\nSources:")

    for source in result["sources"]:
        print(f"{source['source']} — Page {source['page']}")