from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rag_pipeline import answer_question
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from urllib.parse import quote
from fastapi.responses import FileResponse
import logging
import fitz
from collections import Counter
from config import settings
from chromadb import PersistentClient

logger = logging.getLogger(__name__)

app = FastAPI(
    title="DocuTrace API",
    description="Evidence-Grounded Enterprise Knowledge Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

class Citation(BaseModel):
    source_id: int
    source_file: str  # Note: ensure keys match what rag_pipeline returns
    department: str
    page_number: int

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DocuTrace API"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = answer_question(request.question)

        return ChatResponse(
            answer=result["answer"],
            citations=result["citations"]
        )

    except Exception:
        logger.exception(
            "RAG request processing failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process the request. Please try again later."
        )
    
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIRECTORY = PROJECT_ROOT / "sample_documents"


@app.get("/documents/{department}/{filename}")
def get_document(department: str, filename: str):
    # Only serve PDF files from approved dataset directories.
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF documents are supported."
        )

    document_path = (
        DOCUMENTS_DIRECTORY / department / filename
    ).resolve()

    # Prevent directory traversal outside the dataset.
    if not document_path.is_relative_to(
        DOCUMENTS_DIRECTORY.resolve()
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid document path."
        )

    if not document_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return FileResponse(
        path=document_path,
        media_type="application/pdf",
        filename=filename,
        content_disposition_type="inline",
    )

@app.get("/knowledge-base")
def get_knowledge_base():
    documents = []

    for pdf_path in sorted(DOCUMENTS_DIRECTORY.rglob("*.pdf")):
        relative_path = pdf_path.relative_to(DOCUMENTS_DIRECTORY)

        if len(relative_path.parts) != 2:
            continue

        department, filename = relative_path.parts

        with fitz.open(pdf_path) as pdf:
            page_count = len(pdf)

        documents.append({
            "filename": filename,
            "department": department,
            "pages": page_count,
            "url": f"/documents/{quote(department)}/{quote(filename)}",
        })

    client = PersistentClient(path=settings.CHROMA_DB_PATH)

    try:
        collection = client.get_collection(
            name=settings.CHROMA_COLLECTION
        )
        indexed_chunks = collection.count()
    except ValueError:
        indexed_chunks = 0

    departments = dict(
        sorted(Counter(
            document["department"] for document in documents
        ).items())
    )

    return {
        "summary": {
            "documents": len(documents),
            "pages": sum(doc["pages"] for doc in documents),
            "indexed_chunks": indexed_chunks,
        },
        "departments": departments,
        "documents": documents,
    }