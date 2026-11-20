from pathlib import Path
import pymupdf

PDF_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "sample_documents"
)


def load_documents():
    documents = []

    for pdf_path in sorted(PDF_DIRECTORY.rglob("*.pdf")):
        with pymupdf.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if not text:
                    continue

                documents.append({
                    "text": text,
                    "metadata": {
                        "source_file": pdf_path.name,
                        "department": pdf_path.parent.name,
                        "page_number": page_number,
                        "source_path": pdf_path.relative_to(
                            PDF_DIRECTORY
                        ).as_posix()
                    }
                })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Total pages loaded: {len(documents)}")
    if documents:
        print("\nSample metadata:")
        print(documents[0]["metadata"])
        print("\nSample content:")
        print(documents[0]["text"][:300])