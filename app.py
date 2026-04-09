from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from langchain_groq import ChatGroq


# -----------------------------
# FLASK APP
# -----------------------------
app = Flask(__name__)


# -----------------------------
# ENV + KEYS
# -----------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing. Check your .env file.")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# -----------------------------
# EMBEDDINGS
# -----------------------------
def download_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device}
    )

embedding = download_embeddings()


# -----------------------------
# PINECONE + VECTOR STORE
# -----------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "carefusion"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


# -----------------------------
# LLM (GROQ)
# -----------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY
)


# -----------------------------
# RAG CHAIN
# -----------------------------
def format_docs(docs, max_chars: int = 4000) -> str:
    if not docs:
        return "No relevant context found."
    text = "\n\n".join(d.page_content for d in docs)
    return text[:max_chars]


prompt = ChatPromptTemplate.from_template("""
You are a helpful medical assistant. Use ONLY the retrieved context to answer.

Question:
{question}

Context:
{context}

Answer clearly, concisely, and avoid hallucinating.
""")

rag_chain = (
    {
        "question": lambda x: x["question"],
        "context": (
            RunnableLambda(lambda x: retriever.invoke(x["question"]))
            | RunnableLambda(format_docs)
        ),
    }
    | prompt
    | llm
    | StrOutputParser()
)


def ask_bot(query: str) -> str:
    return rag_chain.invoke({"question": query})


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg", "").strip()
    if not msg:
        return "Please enter a question."

    print("User:", msg)
    try:
        answer = ask_bot(msg)
    except Exception as e:
        print("Error in RAG chain:", e)
        return "An internal error occurred while generating the answer."

    print("Answer:", answer)
    return str(answer)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
