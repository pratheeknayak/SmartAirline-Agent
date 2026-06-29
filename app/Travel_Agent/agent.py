import chromadb
from sentence_transformers import SentenceTransformer
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "travel_vectorstore")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name="travel_requirements")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def travel_requirement_lookup(query: str) -> dict:
    """Retrieve relevant travel policy information for visa passport or entry requirement questions."""
    try:
        query_embedding = embed_model.encode(query).tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=3, include=["documents", "metadatas"])
        docs = results.get("documents", [[]])[0]
        if not docs:
            return {"status": "NO_RESULTS", "data": []}
        return {"status": "OK", "data": [{"content": doc.strip()} for doc in docs]}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0.3)

root_agent = Agent(
    name="Travel_Agent",
    model=llm,
    instruction="You are a Visa and Travel Expert. For ANY travel question always call travel_requirement_lookup first. Answer ONLY using retrieved content. Never use your own knowledge. If data is insufficient say I dont have enough information from the travel policy.",
    tools=[travel_requirement_lookup]
)