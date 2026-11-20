import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_PATH = PROJECT_ROOT / "chroma_db"

embeddings = OpenAIEmbeddings(
    model=os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        "text-embedding-3-small"
    )
)

vector_store = Chroma(
    collection_name=os.getenv(
        "CHROMA_COLLECTION",
        "docutrace_knowledge_base"
    ),
    embedding_function=embeddings,
    persist_directory=str(CHROMA_PATH)
)

question = "When should a support ticket be escalated to Tier 2?"

results = vector_store.similarity_search_with_score(
    question,
    k=4
)

print(f"\nQuestion: {question}")
print(f"Retrieved chunks: {len(results)}")

for index, (document, distance) in enumerate(results, start=1):
    print(f"\n========== RESULT {index} ==========")
    print("Document:", document.metadata["source_file"])
    print("Department:", document.metadata["department"])
    print("Page:", document.metadata["page_number"])
    print("Distance:", round(distance, 4))
    print("Content:", document.page_content[:500])