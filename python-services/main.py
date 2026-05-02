import torch
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from utils import compute_score

app = FastAPI()

print(torch.cuda.device_count())
print(torch.cuda.get_device_name(1))
# loading the model, added device due to crash when the cuda:0 was being used by default
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda:1")

documents = [
    {"id": 1, "doc_origin": "state", "state": "Haryana", "crop": "Sugarcane"},
    {"id": 2, "doc_origin": "state", "state": "Himachal", "crop": "Wheat"},
    {"id": 3, "doc_origin": "central", "state": "Punjab", "crop": "Wheat"},
    {"id": 4, "doc_origin": "other", "state": "Haryana", "crop": "Rice"},
    {"id": 5, "doc_origin": "other", "state": "Haryana", "crop": "Wheat"},
    {"id": 6, "doc_origin": "central", "state": "Punjab", "crop": "Rice"},
    {"id": 7, "doc_origin": "state", "state": "Haryana", "crop": "Wheat"}
]

class SearchRequest(BaseModel):
    query:str
    state:str
    crop:str

@app.get("/ping")
def ping():
    return {"message": "Python service is working"}

@app.get("/embed")
def embed():
    vec = model.encode("wheat fertilizer")
    return {"length": len(vec)}

@app.post("/search")
def search(req: SearchRequest):
    query_embedding = model.encode(req.query)
    results = []

    priority_order = ["state", "central", "other"]

    for origin in priority_order:

        # Step 1: filter by origin + state + crop
        matching_docs = []
        for doc in documents:
            if (
                doc["doc_origin"] == origin
                and doc["state"] == req.state
                and doc["crop"] == req.crop
            ):
                matching_docs.append(doc)

        # Step 2: filter by score
        # high_score_docs = []
        # for doc in matching_docs:
            # if doc["score"] >= 0.8:
            #     print("ADDING:", doc)
            #     high_score_docs.append(doc)

        high_score_docs = []

        for doc in matching_docs:
            score = compute_score(model, query_embedding, doc)

            print("SCORE:", score, "DOC:", doc)

            if score >= 0.5:
                high_score_docs.append(doc)
        
        # Step 3: add to results
        results.extend(high_score_docs)

        # Step 4: stop early
        if len(results) >= 5:
            break

    return {
        "results": results[:5]
    }