import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# 🔹 Create local ChromaDB
client = PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="website_data")

model = SentenceTransformer('all-MiniLM-L6-v2')

def ingest(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            print("Processing:", filename)

            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                content = f.read()

            url = "https://" + filename.replace(".txt", "").replace("_", "/")

            embedding = model.encode(content).tolist()

            collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[{"source": url}],
                ids=[url]
            )

folder_path = "pages"
ingest(folder_path)

print("✅ Done! Check 'chroma_db' folder")