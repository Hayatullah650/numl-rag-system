# NUML RAG System — AI-Powered University Information Assistant

I'm building the NUML RAG System to make university information easier to find. Instead of searching through multiple PDF documents manually, students can ask a question in normal language and receive an answer based on retrieved university documents.

This project is part of my journey as an AI Engineer, where I'm learning to build practical AI applications rather than just experimenting with language models.

## Why I Built This

University documents contain useful information about admissions, examinations, scholarships, student policies, and other academic matters. Finding the exact information can take time.

I wanted to build a system that helps users search these documents through a simple chat interface and see where the answer came from.

## What It Can Do

- Accept questions in natural language.
- Process university PDF documents.
- Convert document text into embeddings.
- Search for relevant passages using a vector database.
- Rerank retrieved passages to improve relevance.
- Generate answers using Google Gemini.
- Display source document names and page numbers.
- Provide a React frontend connected to a FastAPI backend.
- Support OCR-based extraction for scanned PDFs when Tesseract OCR is configured.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | Backend API |
| React + Vite | User interface |
| Google Gemini 2.5 Flash | Answer generation |
| ChromaDB | Vector storage and search |
| Sentence Transformers | Text embeddings |
| Cross-Encoder | Document reranking |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | Text extraction from scanned pages |

## How It Works

1. **Document ingestion:** Load PDF documents and extract their text.
2. **Chunking:** Split the text into smaller sections.
3. **Embedding:** Convert the sections into numerical representations.
4. **Storage:** Store the sections and embeddings in ChromaDB.
5. **Retrieval:** Find passages relevant to the user's question.
6. **Reranking:** Reorder passages based on their relevance to the question.
7. **Answer generation:** Send the retrieved context to Gemini.
8. **Source references:** Return the answer with document names and page numbers.

## Project Structure

```text
numl-rag-system/
├── data/                 # Local PDF documents
├── chroma_db/            # Local vector database
├── frontend/             # React application
├── ingest.py             # PDF text extraction
├── chunking.py           # Text chunking
├── vector_store.py       # Embedding and indexing
├── retrieval.py           # Search and reranking
├── rag.py                 # Answer generation
├── api.py                 # FastAPI endpoints
├── .env                   # API keys (never commit)
├── requirements.txt       # Python dependencies
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd numl-rag-system
```

### 2. Set up Python

```bash
python -m venv autonomous-agent
```

On Windows PowerShell:

```powershell
.\autonomous-agent\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Use your own API key. Never upload this file to GitHub.

### 4. Add documents and build the index

Place documents you are authorized to use in the configured data folder.

```bash
python ingest.py
python vector_store.py
```

### 5. Start the backend

```bash
python -m uvicorn api:app --reload
```

Backend API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown in your terminal.

## What I'm Learning

Building this project has helped me work with the full RAG pipeline, including PDF processing, embeddings, vector search, reranking, LLM integration, API development, and frontend integration.

It has also shown me why reliable AI systems need more than good-looking answers. The retrieved evidence must be relevant, source references must be accurate, and the system should clearly communicate when it cannot find enough information.

## Current Limitations

- Answer quality depends on document quality and retrieval accuracy.
- Scanned PDFs and tables need careful extraction and verification.
- The system still needs broader evaluation of answer correctness, retrieval quality, and citations.
- The current version is a local prototype, not a production university service.

## Future Improvements

- Improve retrieval for fee structures, refunds, and other specific policies.
- Add automated RAG evaluation.
- Improve scanned PDF and table extraction.
- Add document versioning and update workflows.
- Introduce authentication and access controls.
- Deploy the application and add monitoring.

## Project Goal

My goal is to keep improving this project into a reliable, source-grounded university information assistant while developing practical AI engineering skills relevant to real-world AI products.

**Note:** This is an independent project. It is not an official NUML application and is not endorsed by NUML unless separately confirmed.

Built as part of my AI Engineering learning journey.
