import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

load_dotenv(PROJECT_ROOT / ".env")

DATASET_PATH = PROJECT_ROOT / "evaluation" / "TestSet.json"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

TOP_K = 4
SAMPLE_SIZE = None


def evaluate():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    questions = [
        item
        for item in dataset["questions"]
        if item["question_type"] != "negative"
    ]

    if SAMPLE_SIZE is not None:
        questions = questions[:SAMPLE_SIZE]

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

    total = len(questions)
    hits = 0
    failed_questions = []

    print("\n========== RETRIEVAL EVALUATION ==========")

    for item in questions:
        results = vector_store.max_marginal_relevance_search(
            item["question"],
            k=TOP_K,
            fetch_k=40,
            lambda_mult=0.5,
    )

        expected_sources = {
            source.strip().replace("\\", "/")
            for source in item["source_document"].split("+")
        }

        retrieved_sources = {
            (
                f"{doc.metadata.get('department', '')}/"
                f"{doc.metadata.get('source_file', '')}"
            )
            for doc in results
        }

        matched_sources = expected_sources & retrieved_sources

        is_hit = expected_sources.issubset(retrieved_sources)

        if is_hit:
            hits += 1
        else:
            failed_questions.append({
                "id": item["id"],
                "question_type": item["question_type"],
                "expected": sorted(expected_sources),
                "retrieved": sorted(retrieved_sources),
            })

        status = "PASS" if is_hit else "FAIL"

        print(
            f"{item['id']} | {status} | "
            f"Matched: {len(matched_sources)}/{len(expected_sources)}"
        )

    hit_rate = (hits / total * 100) if total else 0

    print("\n========== RESULTS ==========")
    print(f"Questions evaluated: {total}")
    print(f"Top-K: {TOP_K}")
    print(f"Successful retrievals: {hits}")
    print(f"Failed retrievals: {total - hits}")
    print(f"Document Hit@{TOP_K}: {hit_rate:.2f}%")

    print("\n========== FAILED QUESTIONS ==========")

    for item in failed_questions:
        print(
            f"{item['id']} | {item['question_type']} | "
            f"Expected: {item['expected']}"
        )


if __name__ == "__main__":
    evaluate()