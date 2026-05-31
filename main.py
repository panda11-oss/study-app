from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://host.docker.internal:11434"

@app.post("/api/llm")
async def llm_proxy(request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=120) as client:
        res = await client.post(f"{OLLAMA_URL}/api/chat", json=body)
        return res.json()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
