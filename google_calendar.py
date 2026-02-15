from datetime import datetime, timedelta
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def create_calendar_event(doctor_name, patient_name, appointment_date, appointment_time):

    service = get_service()

    start_datetime = datetime.strptime(
        f"{appointment_date} {appointment_time}",
        "%Y-%m-%d %H:%M"
    )

    end_datetime = start_datetime + timedelta(minutes=30)

    event = {
        'summary': f'Appointment with {doctor_name}',
        'description': f'Patient: {patient_name}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    return event.get('htmlLink')
