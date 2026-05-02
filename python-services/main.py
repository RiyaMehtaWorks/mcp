from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

documents = [
    {"id": 1, "doc_origin": "state", "state": "Haryana", "crop": "Wheat", "score": 0.9},
    {"id": 2, "doc_origin": "state", "state": "Haryana", "crop": "Wheat", "score": 0.85},
    {"id": 3, "doc_origin": "central", "state": "Haryana", "crop": "Wheat", "score": 0.82},
    {"id": 4, "doc_origin": "other", "state": "Haryana", "crop": "Wheat", "score": 0.88},
    {"id": 5, "doc_origin": "other", "state": "Haryana", "crop": "Wheat", "score": 0.7},
    {"id": 6, "doc_origin": "central", "state": "Punjab", "crop": "Rice", "score": 0.95},
    {"id": 7, "doc_origin": "state", "state": "Haryana", "crop": "Wheat", "score": 0.95}
]

class SearchRequest(BaseModel):
    query:str
    state:str
    crop:str

@app.get("/ping")
def ping():
    return {"message": "Python service is working"}

@app.post("/search")
def search(req: SearchRequest):
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
        high_score_docs = []
        for doc in matching_docs:
            if doc["score"] >= 0.8:
                print("ADDING:", doc)
                high_score_docs.append(doc)

        # Step 3: add to results
        results.extend(high_score_docs)

        # Step 4: stop early
        if len(results) >= 5:
            break

    return {
        "results": results[:5]
    }