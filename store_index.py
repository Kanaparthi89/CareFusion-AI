from src.carefusion_ai.helper import (
    load_pdf_files,
    filter_to_minimal_docs,
    text_split,
    download_hugging_face_embeddings
)

from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load → Filter → Chunk
extracted_data = load_pdf_files("Data/")
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# Embeddings
embeddings = download_hugging_face_embeddings()

# Safety check
if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY is missing. Check your .env file.")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing. Check your .env file.")

# Set environment variables for downstream libraries
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

pc
from pinecone import ServerlessSpec

index_name = "carefusion"

# Create index only if it does NOT already exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # matches MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print("Index created successfully.")
else:
    print("Index already exists.")

# Connect to the index
index = pc.Index(index_name)
index
print(pc.list_indexes().names())
from langchain_pinecone import PineconeVectorStore

index_name = "carefusion"

# Load vector store only once
if "docsearch" not in globals():
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    print("VectorStore loaded and ready.")
else:
    print("VectorStore already loaded. Skipping reload.")

index = pc.Index("carefusion")
index.describe_index_stats()

from tqdm.auto import tqdm

index = pc.Index("carefusion")

# Check existing vector count
stats = index.describe_index_stats()
existing_count = stats.get("total_vector_count", 0)

expected_count = len(text_chunks)

print(f"Existing vectors: {existing_count}")
print(f"Expected vectors: {expected_count}")

# If already upserted → skip
if existing_count >= expected_count:
    print("✔️ Vectors already upserted. Skipping upsert.")
else:
    print("⏳ Upserting missing vectors...")

    batch_size = 200
    vectors = []

    for i, chunk in enumerate(tqdm(text_chunks, desc="Upserting to Pinecone")):
        # Skip if this ID already exists
        vector_id = f"chunk-{i}"
        if i < existing_count:
            continue

        vec = embeddings.embed_query(chunk.page_content)

        vectors.append({
            "id": vector_id,
            "values": vec,
            "metadata": {
                "text": chunk.page_content,
                **chunk.metadata
            }
        })

        if len(vectors) == batch_size:
            index.upsert(vectors)
            vectors = []

    if vectors:
        index.upsert(vectors)

    print("✔️ Upsert complete.")
