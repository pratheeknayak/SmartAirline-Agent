import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# ============================================================
# PATHS
# BASE_DIR = the Airline_Chatbot folder
# PDF_PATH = the Spain visa PDF inside Data/
# DB_PATH  = where ChromaDB will store the vector database
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Data", "SPAIN-VISA-REQUIREMENTS.pdf")
DB_PATH  = os.path.join(BASE_DIR, "travel_vectorstore")
COLLECTION_NAME = "travel_requirements"


def ingest_pdf():

    # Step 1: Check PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"PDF not found at: {PDF_PATH}")
        return

    print("Loading PDF...")

    # Step 2: Load PDF — each page becomes one Document object
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")

    # Step 3: Split into chunks
    # chunk_size=700   → each chunk is max 700 characters
    # chunk_overlap=70 → 70 characters repeat between chunks
    # Why overlap? So sentences that fall at a boundary
    # are not lost — they appear in both adjacent chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=70
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Step 4: Load the embedding model
    # all-MiniLM-L6-v2 converts text → 384-dimensional vector
    # It runs locally on your CPU — no API call needed
    print("Loading embedding model (first run downloads ~90MB)...")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Step 5: Connect to ChromaDB and create collection
    print("Storing embeddings in ChromaDB...")
    client = chromadb.PersistentClient(path=DB_PATH)

    # Delete collection if it already exists (clean rebuild)
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Existing collection deleted, rebuilding...")
    except:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    # Step 6: Embed each chunk and store in ChromaDB
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "SPAIN-VISA-REQUIREMENTS.pdf", "chunk": i}
                 for i in range(len(chunks))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print(f"Ingestion complete! {len(chunks)} chunks stored in ChromaDB.")
    print(f"Vector store location: {DB_PATH}")


if __name__ == "__main__":
    ingest_pdf()