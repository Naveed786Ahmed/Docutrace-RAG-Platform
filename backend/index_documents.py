import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from ingestion import load_documents
from chunking import create_chunks


# Load environment variables
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION",
    "docutrace_knowledge_base"
)


def build_vector_database():
    print("Loading company documents...")

    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Total chunks prepared: {len(chunks)}")

    if not chunks:
        raise ValueError("No chunks available for indexing.")

    # Convert chunks into LangChain Documents
    langchain_documents = [
        Document(
            page_content=chunk["text"],
            metadata=chunk["metadata"]
        )
        for chunk in chunks
    ]

    # Initialize OpenAI embedding model
    embeddings = OpenAIEmbeddings(
        model=os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small"
        )
    )

    # Initialize persistent ChromaDB
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    # Use stable IDs to prevent duplicate records
    chunk_ids = [
        chunk["metadata"]["chunk_id"]
        for chunk in chunks
    ]

    if len(chunk_ids) != len(set(chunk_ids)):
        raise ValueError("Duplicate chunk IDs detected.")

    print("Generating embeddings and indexing chunks...")

    # Upsert ensures existing IDs are updated
    vector_store.add_documents(
        documents=langchain_documents,
        ids=chunk_ids
    )

    stored_count = vector_store._collection.count()

    print("\n========== INDEXING SUMMARY ==========")
    print(f"Documents processed: {len(documents)} pages")
    print(f"Chunks prepared: {len(chunks)}")
    print(f"Chunks stored: {stored_count}")
    print(f"Database path: {CHROMA_PATH}")


if __name__ == "__main__":
    build_vector_database()