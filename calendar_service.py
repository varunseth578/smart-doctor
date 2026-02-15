from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta
from dateutil import parser

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service


def convert_to_datetime(date_str, time_str):
    """
    Convert appointment date and time to ISO format
    """

    dt = parser.parse(f"{date_str} {time_str}")

    start = dt.isoformat()
    end = (dt + timedelta(minutes=30)).isoformat()

    return start, end


def create_calendar_event(doctor_name, patient_name, appointment_date, appointment_time):

    try:
        service = get_calendar_service()

        start, end = convert_to_datetime(
            appointment_date,
            appointment_time
        )

        event = {
            'summary': f'Dr. {doctor_name} Appointment with {patient_name}',
            'description': 'Doctor Appointment booked via AI system',
            'start': {
                'dateTime': start,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Asia/Kolkata',
            },
        }

        event_result = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        print("Calendar event created:", event_result.get("htmlLink"))

        return event_result

    except Exception as e:
        print("Google Calendar Error:", e)
        raise e
