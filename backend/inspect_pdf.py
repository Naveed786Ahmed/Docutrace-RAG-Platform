from pathlib import Path
import pymupdf

# 1. Recursive search: sample_documents aur uske sabhi department subfolders se PDFs dhundna
pdf_files = sorted(Path("sample_documents").rglob("*.pdf"))

print(f"Total PDFs found: {len(pdf_files)}")

if not pdf_files:
    raise SystemExit("No PDF files found.")

# 2. Pehli PDF ko inspect karna
pdf_path = pdf_files[0]

# Context manager ('with') use kar rahe hain taake file read hone ke baad memory se safely close ho jaye
with pymupdf.open(pdf_path) as document:
    print(f"\nDocument: {pdf_path.name}")
    print(f"Department: {pdf_path.parent.name}")
    print(f"Total pages: {len(document)}")

    # 0-based indexing hoti hai, isliye document[0] ka matlab Page 1 hai
    first_page = document[0]
    text = first_page.get_text("text")

    print("\n--- First Page Text ---")
    print(text[:1000])  # Sirf pehle 1000 characters print kar rahe hain preview ke liye

    print(f"\nExtracted characters: {len(text.strip())}")   