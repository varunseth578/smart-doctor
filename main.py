from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_memory = {}

@app.post("/chat")
def chat(data: dict):
    session_id = data["session_id"]
    message = data["message"]

    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    conversation_memory[session_id].append(message)

    response = run_agent(message)

   
    if isinstance(response, dict):
        return {"response": response.get("content", "No content")}
    else:
        return {"response": str(response)}
