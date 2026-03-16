from fastapi import FastAPI
from pydantic import BaseModel

from storage.vector_store import VectorStore


app = FastAPI(title="Covenix")
store = VectorStore()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.on_event("startup")
def warm_start():
    try:
        store._get_index()
    except Exception:
        store.build_index()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search(req: SearchRequest):
    results = store.search(req.query, req.top_k)
    return {"results": results}
