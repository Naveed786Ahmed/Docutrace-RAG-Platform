import json
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "evaluation" / "TestSet.json"
DOCUMENTS_PATH = PROJECT_ROOT / "sample_documents"

REQUIRED_FIELDS = {
    "id",
    "question",
    "ground_truth_answer",
    "source_document",
    "category",
    "question_type",
    "difficulty",
}


def validate_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    questions = dataset["questions"]
    errors = []
    warnings = []

    question_ids = []

    for index, item in enumerate(questions, start=1):
        # Missing fields check (Fixed)
        missing = REQUIRED_FIELDS - item.keys()

        if missing:
            errors.append(
                f"Record {index}: Missing fields {sorted(missing)}"
            )
            continue

        question_ids.append(item["id"])

        if not isinstance(item["question"], str) or not item["question"].strip():
            errors.append(f"{item['id']}: Empty question")

        if not isinstance(item["ground_truth_answer"], str):
            errors.append(f"{item['id']}: Invalid ground truth")

        # --- UPDATED SOURCE VALIDATION LOGIC ---
        source = item["source_document"]
        question_type = item["question_type"]

        if not isinstance(source, str):
            errors.append(f"{item['id']}: Invalid source document")
            continue

        # Agar negative question hai, toh source "N/A" hona chahiye
        if question_type == "negative":
            if source.strip().upper() != "N/A":
                errors.append(
                    f"{item['id']}: Negative question should have N/A source"
                )
            continue

        # Multi-source splitting (e.g., "Doc1.pdf + Doc2.pdf")
        sources = [
            path.strip()
            for path in source.split("+")
            if path.strip()
        ]

        if not sources:
            errors.append(f"{item['id']}: No source documents specified")
            continue

        # Har ek source file ko validate karein
        for document in sources:
            source_path = (DOCUMENTS_PATH / document).resolve()

            if not source_path.is_relative_to(DOCUMENTS_PATH.resolve()):
                errors.append(
                    f"{item['id']}: Invalid source path: {document}"
                )
                continue

            if not source_path.is_file():
                warnings.append(
                    f"{item['id']}: Source not found: {document}"
                )
        # ---------------------------------------

    duplicates = [
        question_id
        for question_id, count in Counter(question_ids).items()
        if count > 1
    ]

    if duplicates:
        errors.append(f"Duplicate IDs: {duplicates}")

    print("\n========== DATASET INTEGRITY REPORT ==========")
    print("Declared questions:", dataset.get("num_questions"))
    print("Actual questions:", len(questions))
    print("Unique IDs:", len(set(question_ids)))
    print("Errors:", len(errors))
    print("Warnings:", len(warnings))

    print("\nQuestion types:")
    for question_type, count in Counter(
        item.get("question_type", "unknown")
        for item in questions
    ).items():
        print(f"  {question_type}: {count}")

    print("\nCategories:")
    for category, count in Counter(
        item.get("category", "unknown")
        for item in questions
    ).items():
        print(f"  {category}: {count}")

    if errors:
        print("\nERROR DETAILS:")
        for error in errors[:20]:
            print("-", error)

    if warnings:
        print("\nWARNING DETAILS:")
        for warning in warnings[:20]:
            print("-", warning)

    if not errors and not warnings:
        print("\nDataset integrity validation passed.")


if __name__ == "__main__":
    validate_dataset()