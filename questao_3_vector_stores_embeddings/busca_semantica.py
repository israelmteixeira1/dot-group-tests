#!/usr/bin/env python3
import os

import pdfplumber
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Evita crash de semáforos no macOS com tokenizers em paralelo
os.environ["TOKENIZERS_PARALLELISM"] = "false"

PDF_PATH = os.path.join(os.path.dirname(__file__), "500perguntasgadoleite.pdf")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "faiss_index")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 5

DEMO_QUERIES = [
    "Como cuidar do bezerro recém-nascido?",
    "Qual a produção média de leite por vaca?",
    "Como prevenir e tratar a mastite?",
    "Alimentação de vacas em lactação",
    "Quais raças bovinas são melhores para leite?",
]


def load_pdf(path: str) -> list[Document]:
    with pdfplumber.open(path) as pdf:
        return [
            Document(page_content=page.extract_text().strip(), metadata={"pagina": i + 1})
            for i, page in enumerate(pdf.pages)
            if page.extract_text() and page.extract_text().strip()
        ]


def build_index(embeddings: HuggingFaceEmbeddings) -> FAISS:
    docs = load_pdf(PDF_PATH)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"Indexando {len(chunks)} chunks no FAISS...")
    index = FAISS.from_documents(chunks, embeddings)
    index.save_local(INDEX_DIR)
    return index


def print_results(results: list[tuple[Document, float]], preview_len: int = 300) -> None:
    for i, (doc, score) in enumerate(results, 1):
        trecho = doc.page_content[:preview_len].replace("\n", " ")
        print(f"  [{i}] Score L2: {score:.4f} | Pág. {doc.metadata.get('pagina', '?')}")
        print(f"       {trecho}...")


def main() -> None:
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    if os.path.exists(INDEX_DIR):
        index = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    else:
        index = build_index(embeddings)

    print("\n" + "=" * 60)
    for query in DEMO_QUERIES:
        print(f'\nConsulta: "{query}"')
        print_results(index.similarity_search_with_score(query, k=3))

    print("\n" + "=" * 60)
    print("Modo interativo — digite 'sair' para encerrar")
    print("=" * 60)

    while True:
        try:
            query = input("\nConsulta: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if query.lower() in ("sair", "exit", "quit") or not query:
            break
        print_results(index.similarity_search_with_score(query, k=TOP_K), preview_len=400)


if __name__ == "__main__":
    main()
