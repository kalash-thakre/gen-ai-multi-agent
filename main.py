from dotenv import load_dotenv
load_dotenv()  # Must be FIRST before any other imports

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os

from multi_agent_system.agent import process_message

app = FastAPI(title="Multi-Agent System")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    response = process_message(req.message)
    return {"response": response}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
