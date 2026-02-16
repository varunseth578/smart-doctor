from fastapi import FastAPI
from pydantic import BaseModel


from agent import check_availability, book_appointment


app = FastAPI(title="Doctor Appointment MCP Server")




class AvailabilityRequest(BaseModel):
    doctor_name: str
    appointment_date: str


class BookingRequest(BaseModel):
    doctor_name: str
    patient_name: str
    appointment_date: str
    appointment_time: str



@app.get("/mcp/tools")
def list_tools():

    return {
        "tools": [
            {
                "name": "check_availability",
                "description": "Check doctor available slots",
                "endpoint": "/mcp/tools/check_availability",
                "method": "POST"
            },
            {
                "name": "book_appointment",
                "description": "Book doctor appointment",
                "endpoint": "/mcp/tools/book_appointment",
                "method": "POST"
            }
        ]
    }




@app.post("/mcp/tools/check_availability")
def availability(request: AvailabilityRequest):

    result = check_availability(
        doctor_name=request.doctor_name,
        appointment_date=request.appointment_date
    )

    return result


@app.post("/mcp/tools/book_appointment")
def booking(request: BookingRequest):

    result = book_appointment(
        doctor_name=request.doctor_name,
        patient_name=request.patient_name,
        appointment_date=request.appointment_date,
        appointment_time=request.appointment_time
    )

    return result
