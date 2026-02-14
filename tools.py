from database import SessionLocal
from models import Appointment
from datetime import date

def check_availability(doctor_name, appointment_date, appointment_time):
    db = SessionLocal()
    existing = db.query(Appointment).filter(
        Appointment.doctor_name == doctor_name,
        Appointment.date == appointment_date,
        Appointment.time == appointment_time
    ).first()

    if existing:
        return {"available": False}
    return {"available": True}


def book_appointment(doctor_name, patient_name, appointment_date, appointment_time, symptoms):
    db = SessionLocal()
    appointment = Appointment(
        doctor_name=doctor_name,
        patient_name=patient_name,
        date=appointment_date,
        time=appointment_time,
        symptoms=symptoms
    )
    db.add(appointment)
    db.commit()
    return {"status": "booked"}


def doctor_summary(doctor_name):
    db = SessionLocal()
    today = date.today()
    appointments = db.query(Appointment).filter(
        Appointment.doctor_name == doctor_name,
        Appointment.date == today
    ).all()

    return {
        "total_today": len(appointments)
    }
