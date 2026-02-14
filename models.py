from sqlalchemy import Column, Integer, String, Date, Time
from database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String)
    patient_name = Column(String)
    date = Column(Date)
    time = Column(Time)
    symptoms = Column(String)
