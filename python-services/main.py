from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class SearchRequest(BaseModel):
    query:str
    state:str
    crop:str

@app.get("/ping")
def ping():
    return {"message": "Python service is working"}

@app.post("/search")
def search(req: SearchRequest):
    return {
        "received": {
            "query": req.query,
            "state": req.state,
            "crop": req.crop
        }
    }