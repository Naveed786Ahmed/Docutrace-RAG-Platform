import re
from ingestion import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove repeated company header
        if line.startswith("AcmeTech Solutions Inc. —"):
            continue

        # Remove repeated document-control headers
        if line.startswith("Document ID:") and "Version:" in line:
            continue

        # Remove repeated confidentiality footer
        if line == "Internal Use Only":
            continue

        # Remove standalone page labels, e.g. "Page 1"
        if re.fullmatch(r"Page \d+", line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = []

    for doc in documents:
        # Skip cover pages and table of contents
        if doc["metadata"]["page_number"] in (1, 2):
            continue

        cleaned_content = clean_text(doc["text"])
        if not cleaned_content:
            continue

        text_chunks = splitter.split_text(cleaned_content)

        for index, chunk_text in enumerate(text_chunks):
            chunk_metadata = doc["metadata"].copy()
            chunk_metadata["chunk_index"] = index
            chunk_metadata["chunk_id"] = (
                f"{chunk_metadata['source_file']}_p{chunk_metadata['page_number']}_c{index}"
            )

            chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = create_chunks(documents)

    print(f"Total pages processed: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    if chunks:
        print("\nSample Chunk Metadata:")
        print(chunks[0]["metadata"])
        print("\nSample Chunk Text:")
        print(chunks[0]["text"][:300])


