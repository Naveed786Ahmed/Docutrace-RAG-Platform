from pathlib import Path
import pymupdf

PDF_DIRECTORY = Path("sample_documents")

total_documents = 0
total_pages = 0
empty_pages = 0
failed_documents = []

for pdf_path in sorted(PDF_DIRECTORY.rglob("*.pdf")):
    try:
        with pymupdf.open(pdf_path) as document:
            total_documents += 1
            total_pages += len(document)
            document_empty_pages = 0

            for page in document:
                text = page.get_text("text").strip()
                if not text:
                    empty_pages += 1
                    document_empty_pages += 1

            print(
                f"[OK] {pdf_path.parent.name}/"
                f"{pdf_path.name} | "
                f"Pages: {len(document)} | "
                f"Empty: {document_empty_pages}"
            )

    except Exception as error:
        failed_documents.append(
            {"file": str(pdf_path), "error": str(error)}
        )
        print(f"[FAILED] {pdf_path.name}: {error}")

print("\n========== DATASET AUDIT ==========")
print(f"Documents processed: {total_documents}")
print(f"Total pages: {total_pages}")
print(f"Empty pages: {empty_pages}")
print(f"Failed documents: {len(failed_documents)}")