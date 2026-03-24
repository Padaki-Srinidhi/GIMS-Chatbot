from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import PersistentClient
import os
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from configparser import ConfigParser
# 🔹 Load config
config = ConfigParser()
config.read("config/config.ini")
openai_api_key = config["DEFAULT"]["openai_api_key"]

# 🔹 Init FastAPI
app = FastAPI()

# # 🔹 OpenAI client
# client_openai = OpenAI(api_key=openai_api_key)

HF_TOKEN = config["DEFAULT"]["HF_Token"]
client_llama = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)


# 🔹 Embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔹 Create local ChromaDB
client = PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="website_data")

# 🔹 Request schema
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "AI Chatbot API running 🚀"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    user_query = request.query

    # 🔹 Step 1: Convert query to embedding
    query_embedding = model.encode(user_query).tolist()

    # 🔹 Step 2: Search relevant docs
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    documents = results.get("documents", [[]])[0]

    # 🔹 Step 3: Build context
    context = "\n\n".join(documents)

    # 🔹 Step 4: Send to OpenAI
    prompt = f"""
        You are a helpful college assistant chatbot.

        Answer ONLY from the given context.
        If answer is not present, say "I don't know".

        Context:
        {context}

        Question:
        {user_query}
        """
    completion = client_llama.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:novita",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )


    answer = completion.choices[0].message
    print(f"Answer: {answer}")
    # response = client_openai.chat.completions.create(
    #     model="gpt-4.1-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.3
    # )

    # answer = response.choices[0].message.content

    return {
        "query": user_query,
        "answer": answer
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)