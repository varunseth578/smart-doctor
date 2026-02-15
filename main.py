from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_memory = {}
session_data = {}

@app.post("/chat")
def chat(data: dict):
    session_id = data["session_id"]
    message = data["message"]

    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
        session_data[session_id] = {
            "doctor_name": None,
            "appointment_date": None,
            "available_slots": []
        }

    conversation_memory[session_id].append({
        "role": "user",
        "content": message
    })

    response = run_agent(
        conversation_memory[session_id],
        session_data[session_id]
    )

    conversation_memory[session_id].append({
        "role": "assistant",
        "content": response
    })

    return {"response": response}
