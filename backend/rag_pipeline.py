import os
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from config import settings

# 1. Environment aur Paths setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_PATH = PROJECT_ROOT / "chroma_db"

# 2. Vector Store initialize karein
vector_store = Chroma(
    collection_name=settings.CHROMA_COLLECTION,
    embedding_function=OpenAIEmbeddings(
        model=settings.OPENAI_EMBEDDING_MODEL
    ),
    persist_directory=settings.CHROMA_DB_PATH
)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

llm = ChatOpenAI(
    model=settings.OPENAI_CHAT_MODEL,
    temperature=0
)

# 3. Standardized Fallback Message Constant
FALLBACK_MESSAGE = "I cannot find this information in the company documents."

# 4. Strict System Prompt with Numbered Sources
SYSTEM_PROMPT = """You are DocuTrace, an internal enterprise knowledge assistant.

Rules:
1. Answer the user's question using ONLY the provided document context below.
2. Never invent company policies, procedures, or facts.
3. If the context does not contain sufficient information, you must explicitly state: "I cannot find this information in the company documents."
4. Whenever you use information from a context chunk, cite it using its exact source tag (e.g., [Source 1], [Source 2]). Do not invent source numbers.

Context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

def format_docs_with_sources(docs):
    """
    Retrieved chunks ko [Source 1], [Source 2] ke taur par tag karta hai
    taake LLM precise citations de sake.
    """
    formatted = []
    citations = []
    
    for idx, doc in enumerate(docs, start=1):
        source_id = idx
        source_file = doc.metadata.get("source_file", "Unknown")
        department = doc.metadata.get("department", "Unknown")
        page_number = doc.metadata.get("page_number", "Unknown")
        
        citations.append({
            "source_id": source_id,
            "source_file": source_file,
            "department": department,
            "page_number": page_number
        })
        
        content = doc.page_content
        formatted.append(f"[Source {source_id}] (File: {source_file}, Page: {page_number})\n{content}\n")
        
    return "\n---\n".join(formatted), citations

def answer_question(question: str):
    # Step A: Retrieve relevant chunks
    retrieved_docs = retriever.invoke(question)
    context_text, citations = format_docs_with_sources(retrieved_docs)
    
    # Step B: Generate response from LLM
    messages = prompt.format_messages(context=context_text, question=question)
    response = llm.invoke(messages)
    
    answer = response.content.strip()
    
    # Step C: Normalize unsupported-answer responses (Catch variations from LLM)
    fallback_phrases = [
        "cannot find this information",
        "could not find this information",
        "not available in the provided documents",
        "not mentioned in the provided documents",
        "insufficient information"
    ]
    if any(phrase in answer.lower() for phrase in fallback_phrases):
        return {
            "answer": FALLBACK_MESSAGE,
            "citations": []
        }
    
    # Step D: Normalize citation format (e.g., [Source1] -> [Source 1])
    answer = re.sub(
        r"\[Source\s*(\d+)\]",
        r"[Source \1]",
        answer,
        flags=re.IGNORECASE
    )
    
    # Step E: Extract referenced source IDs using Regex
    referenced_ids = {
        int(source_id)
        for source_id in re.findall(
            r"\[Source (\d+)\]",
            answer
        )
    }
    
    # Step F: Validation guardrail (Reject if non-existent source is cited)
    valid_ids = {item["source_id"] for item in citations}
    if referenced_ids and not referenced_ids.issubset(valid_ids):
        return {
            "answer": FALLBACK_MESSAGE,
            "citations": []
        }
        
    # Step G: Filter and return only the sources actually referenced in the answer
    verified_citations = [
        citation
        for citation in citations
        if citation["source_id"] in referenced_ids
    ]
    
    return {
        "answer": answer,
        "citations": verified_citations
    }

if __name__ == "__main__":
    test_question = "What is AcmeTech's office address in Tokyo?"
    print(f"\nQuerying RAG Pipeline with Standardized Fallback...")
    print(f"Question: {test_question}\n")
    
    result = answer_question(test_question)
    
    print("========== RAG ANSWER ==========")
    print(result["answer"])
    print("================================")
    
    print("\nVerified Citations:")
    if result["citations"]:
        for cit in result["citations"]:
            print(f" - [Source {cit['source_id']}] {cit['source_file']} (Page {cit['page_number']})")
    else:
        print(" - No citations returned.")