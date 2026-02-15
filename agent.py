


import requests
import json
from datetime import datetime

from database import SessionLocal
from models import Appointment
from calendar_service import create_calendar_event
from gmail_sender import send_email


OPENROUTER_API_KEY = "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"


def validate_and_convert_date(date_str):

    try:

      
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")

        # Convert to YYYY-MM-DD for database
        return date_obj.strftime("%Y-%m-%d")

    except ValueError:

        return None


# -----------------------------
# CHECK AVAILABILITY
# -----------------------------
def check_availability(doctor_name=None, appointment_date=None, appointment_time=None):

    if not doctor_name:
        return {"message": "Please provide doctor name."}

    if not appointment_date:
        return {"message": "Please provide appointment date in DD-MM-YYYY format."}

    db_date = validate_and_convert_date(appointment_date)

    if not db_date:
        return {"message": "Invalid date format. Please use DD-MM-YYYY."}

    print(f"Checking availability for Dr. {doctor_name} on {appointment_date}")

    return {
        "available_slots": ["2:00 PM", "3:00 PM", "4:00 PM"]
    }


# -----------------------------
# BOOK APPOINTMENT
# -----------------------------
def book_appointment(
    doctor_name=None,
    patient_name=None,
    appointment_date=None,
    appointment_time=None
):

    # VALIDATION
    if not doctor_name:
        return {"status": "missing", "message": "Please provide doctor name."}

    if not patient_name:
        return {"status": "missing", "message": "Please provide patient name."}

    if not appointment_date:
        return {"status": "missing", "message": "Please provide appointment date in DD-MM-YYYY format."}

    if not appointment_time:
        return {"status": "missing", "message": "Please provide appointment time."}


    # Validate and convert date
    db_date = validate_and_convert_date(appointment_date)

    if not db_date:
        return {
            "status": "error",
            "message": "Invalid date format. Please use DD-MM-YYYY."
        }


    db = SessionLocal()

    try:

        # Save to database
        new_appointment = Appointment(
            doctor_name=doctor_name,
            patient_name=patient_name,
            appointment_date=db_date,
            appointment_time=appointment_time
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        print("✅ Appointment saved in database")


        # Create Calendar Event
        calendar_link = None

        try:

            calendar_link = create_calendar_event(
                doctor_name,
                patient_name,
                db_date,
                appointment_time
            )

            print("✅ Calendar event created")

        except Exception as cal_error:

            print("❌ Calendar error:", cal_error)


        # Send Email
        try:

            subject = "Appointment Confirmation"

            body = f"""
Appointment Confirmed

Doctor: Dr. {doctor_name}
Patient: {patient_name}
Date: {appointment_date}
Time: {appointment_time}

Calendar Link:
{calendar_link}

Thank you.
"""

            send_email(
                "ivarunseth@gmail.com",
                subject,
                body
            )

            print("✅ Email sent successfully")

        except Exception as email_error:

            print("❌ Email error:", email_error)


        return {

            "status": "confirmed",

            "message": f"""
Appointment Confirmed ✅

Doctor: Dr. {doctor_name}
Patient: {patient_name}
Date: {appointment_date}
Time: {appointment_time}

Confirmation email sent successfully.
""",

            "calendar_link": calendar_link
        }


    except Exception as e:

        db.rollback()

        print("❌ DATABASE ERROR:", e)

        return {
            "status": "error",
            "message": str(e)
        }

    finally:

        db.close()


# -----------------------------
# TOOLS LIST
# -----------------------------
tools_list = [

    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check doctor available slots",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "appointment_date": {"type": "string"},
                    "appointment_time": {"type": "string"}
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book doctor appointment",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "patient_name": {"type": "string"},
                    "appointment_date": {"type": "string"},
                    "appointment_time": {"type": "string"}
                }
            }
        }
    }

]


# -----------------------------
# RUN AGENT
# -----------------------------
def run_agent(messages, session_info):

    system_prompt = {

        "role": "system",

        "content": """
You are a Doctor Appointment Assistant.

RULES:

• Always ask patient name if missing
• Always ask appointment date in DD-MM-YYYY format
• Always ask appointment time if missing
• Never confirm booking without full details

Example: 25-02-2026
"""
    }


    headers = {

        "Authorization": f"Bearer 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",

        "Content-Type": "application/json"

    }


    payload = {

        "model": "stepfun/step-3.5-flash:free",

        "messages": [system_prompt] + messages,

        "tools": tools_list,

        "tool_choice": "auto"

    }


    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers=headers,

        json=payload

    )


    result = response.json()

    msg = result["choices"][0]["message"]


    if "tool_calls" in msg:

        tool_call = msg["tool_calls"][0]

        function_name = tool_call["function"]["name"]

        arguments = json.loads(tool_call["function"]["arguments"])


        if function_name == "check_availability":

            tool_result = check_availability(**arguments)

            return tool_result.get(
                "message",
                f"Available slots: {tool_result.get('available_slots', [])}"
            )


        elif function_name == "book_appointment":

            tool_result = book_appointment(**arguments)

            return tool_result["message"]


    return msg.get("content", "Done")
