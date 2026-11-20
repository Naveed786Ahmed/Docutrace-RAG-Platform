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

TOP_K = 4
CANDIDATE_K = 10
RRF_K = 60


def reciprocal_rank_fusion(result_lists, top_k=4):
    scores = {}
    documents = {}

    for results in result_lists:
        for rank, document in enumerate(results, start=1):
            chunk_id = document.metadata.get("chunk_id")

            if not chunk_id:
                raise ValueError("Missing chunk_id in document metadata")

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (RRF_K + rank)
            )

            documents[chunk_id] = document

    ranked_ids = sorted(
        scores,
        key=lambda chunk_id: scores[chunk_id],
        reverse=True
    )

    return [
        documents[chunk_id]
        for chunk_id in ranked_ids[:top_k]
    ]


def evaluate():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    questions = [
        item
        for item in dataset["questions"]
        if item["question_type"] != "negative"
    ]

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

    hits = 0
    failed = []

    print("\n========== HYBRID RETRIEVAL ==========")

    for item in questions:
        similarity_results = vector_store.similarity_search(
            item["question"],
            k=CANDIDATE_K
        )

        mmr_results = vector_store.max_marginal_relevance_search(
            item["question"],
            k=CANDIDATE_K,
            fetch_k=20,
            lambda_mult=0.5,
        )

        results = reciprocal_rank_fusion(
            [similarity_results, mmr_results],
            top_k=TOP_K
        )

        expected = {
            source.strip()
            for source in item["source_document"].split("+")
        }

        retrieved = {
            (
                f"{doc.metadata.get('department')}/"
                f"{doc.metadata.get('source_file')}"
            )
            for doc in results
        }

        passed = expected.issubset(retrieved)

        if passed:
            hits += 1
        else:
            failed.append(item["id"])

        print(
            f"{item['id']} | "
            f"{'PASS' if passed else 'FAIL'}"
        )

    total = len(questions)

    print("\n========== RESULTS ==========")
    print(f"Questions evaluated: {total}")
    print(f"Successful retrievals: {hits}")
    print(f"Failed retrievals: {total - hits}")
    print(f"Document Hit@{TOP_K}: {hits / total * 100:.2f}%")
    print(f"Failed question IDs: {failed}")


if __name__ == "__main__":
    evaluate()