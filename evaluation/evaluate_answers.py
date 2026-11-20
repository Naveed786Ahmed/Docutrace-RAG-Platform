import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from rag_pipeline import answer_question

DATASET_PATH = PROJECT_ROOT / "evaluation" / "TestSet.json"
OUTPUT_PATH = PROJECT_ROOT / "evaluation" / "answer_evaluation.csv"

FALLBACK_MESSAGE = (
    "I cannot find this information in the company documents."
)


def select_questions(questions):
    single_hop = [
        q for q in questions
        if q["question_type"] == "single_hop"
    ][:8]

    multi_hop = [
        q for q in questions
        if q["question_type"] == "multi_hop"
    ][:4]

    negative = [
        q for q in questions
        if q["question_type"] == "negative"
    ]

    return single_hop + multi_hop + negative


def evaluate():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    questions = select_questions(dataset["questions"])
    results = []

    print("\n========== RAG ACCEPTANCE TEST ==========")

    for item in questions:
        question_id = item["id"]

        print(f"\nTesting {question_id}...")

        try:
            response = answer_question(item["question"])

            answer = response["answer"]
            citations = response.get("citations", [])

            is_negative = item["question_type"] == "negative"
            is_fallback = answer.strip() == FALLBACK_MESSAGE

            fallback_pass = (
                is_fallback and len(citations) == 0
                if is_negative
                else not is_fallback
            )

            expected_sources = {
                source.strip()
                for source in item["source_document"].split("+")
                if source.strip().upper() != "N/A"
            }

            cited_sources = {
                f"{c.get('department')}/{c.get('source_file')}"
                for c in citations
            }

            citation_match = (
                expected_sources.issubset(cited_sources)
                if not is_negative
                else len(citations) == 0
            )

            results.append({
                "id": question_id,
                "question_type": item["question_type"],
                "question": item["question"],
                "ground_truth_answer": item["ground_truth_answer"],
                "generated_answer": answer,
                "expected_sources": " | ".join(sorted(expected_sources)),
                "cited_sources": " | ".join(sorted(cited_sources)),
                "fallback_pass": fallback_pass,
                "citation_match": citation_match,
                "manual_answer_correct": "",
                "manual_citation_supported": "",
                "review_notes": "",
            })

            print(
                f"{question_id} | "
                f"Fallback: {fallback_pass} | "
                f"Citation match: {citation_match}"
            )

        except Exception as error:
            print(f"{question_id} | ERROR: {error}")

            results.append({
                "id": question_id,
                "question_type": item["question_type"],
                "question": item["question"],
                "ground_truth_answer": item["ground_truth_answer"],
                "generated_answer": "",
                "expected_sources": item["source_document"],
                "cited_sources": "",
                "fallback_pass": False,
                "citation_match": False,
                "manual_answer_correct": "",
                "manual_citation_supported": "",
                "review_notes": str(error),
            })

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n========== RESULTS ==========")
    print(f"Questions tested: {len(results)}")
    print(f"Report saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    evaluate()