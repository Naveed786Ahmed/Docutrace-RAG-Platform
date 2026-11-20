import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

DATASET_PATH = PROJECT_ROOT / "evaluation" / "TestSet.json"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

FAILED_IDS = [
    "Q030", "Q041", "Q044", "Q046",
    "Q066", "Q080", "Q088", "Q092",
    "Q124", "Q125", "Q127", "Q130",
    "Q131", "Q132", "Q137", "Q139",
    "MH003", "MH004", "MH006",
    "MH009", "MH010", "MH012",
]

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    dataset = json.load(file)

questions = {
    item["id"]: item
    for item in dataset["questions"]
}

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
    persist_directory=str(CHROMA_PATH),
)

print("\n========== RETRIEVAL FAILURE DIAGNOSIS ==========")

for question_id in FAILED_IDS:
    item = questions[question_id]

    expected = {
        source.strip()
        for source in item["source_document"].split("+")
    }

    results = vector_store.similarity_search(
        item["question"],
        k=10
    )

    retrieved = [
        (
            f"{doc.metadata.get('department')}/"
            f"{doc.metadata.get('source_file')}"
        )
        for doc in results
    ]

    top4 = set(retrieved[:4])
    top10 = set(retrieved)

    hit4 = expected.issubset(top4)
    hit10 = expected.issubset(top10)

    print(f"\n{question_id}: {item['question']}")
    print(f"Expected: {sorted(expected)}")
    print(f"Hit@4: {hit4}")
    print(f"Hit@10: {hit10}")

    for rank, source in enumerate(retrieved, start=1):
        marker = "*" if source in expected else " "
        print(f"  {rank:02d}. {marker} {source}")