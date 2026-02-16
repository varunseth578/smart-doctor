from database import SessionLocal
from models import Appointment
from datetime import datetime
from google_calendar import create_calendar_event
from gmail_sender import send_email


def check_availability(doctor_name, appointment_date, appointment_time):

    db = SessionLocal()

    appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    appointment_time = datetime.strptime(appointment_time, "%H:%M").time()

    existing = db.query(Appointment).filter(
        Appointment.doctor_name == doctor_name,
        Appointment.date == appointment_date,
        Appointment.time == appointment_time
    ).first()

    db.close()

    if existing:
        return {"available": False}

    return {"available": True}


def book_appointment(doctor_name, patient_name, appointment_date, appointment_time):

    db = SessionLocal()

    appointment_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    appointment_time_obj = datetime.strptime(appointment_time, "%H:%M").time()

    new_appointment = Appointment(
        doctor_name=doctor_name,
        patient_name=patient_name,
        date=appointment_date_obj,
        time=appointment_time_obj
    )

    db.add(new_appointment)
    db.commit()
    db.close()

    
    calendar_link = create_calendar_event(
        doctor_name,
        patient_name,
        appointment_date,
        appointment_time
    )

    
    subject = "Appointment Confirmation"

    message = f"""
Hello {patient_name},

Your appointment has been successfully booked.

Doctor: {doctor_name}
Date: {appointment_date}
Time: {appointment_time}

Calendar Link:
{calendar_link}

Thank you.
"""

    send_email(
        "ivarunseth@gmail.com", 
        subject,
        message
    )

    return {
        "status": "booked",
        "calendar_link": calendar_link,
        "email_sent": True
    }
