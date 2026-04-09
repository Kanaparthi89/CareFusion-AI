from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List
import os

# 1. Load PDFs
def load_pdf_files(folder_path: str) -> List[Document]:
    loader = DirectoryLoader(
        folder_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    docs = loader.load()
    docs = sorted(docs, key=lambda d: d.metadata.get("source", ""))
    return docs

# 2. Minimal docs
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    return [
        Document(
            page_content=doc.page_content,
            metadata={"source": doc.metadata.get("source")}
        )
        for doc in docs
    ]

# 3. Chunking
def text_split(docs: List[Document], chunk_size=500, chunk_overlap=20) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_documents(docs)

# 4. Embeddings
def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
