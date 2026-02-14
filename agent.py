import requests
import json
from tools import check_availability, book_appointment, doctor_summary

OPENROUTER_API_KEY = "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"

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check doctor availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "appointment_date": {"type": "string"},
                    "appointment_time": {"type": "string"}
                },
                "required": ["doctor_name", "appointment_date", "appointment_time"]
            }
        }
    }
]

def run_agent(message):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "arcee-ai/trinity-large-preview:free",  
            "messages": [
                {"role": "user", "content": message}
            ],
            "tools": tools_list
        })
    )

    result = response.json()
    return result["choices"][0]["message"]
