import os
import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send"
]


def send_email(to_email, subject, message_text):

    creds = None

    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(message_text)

    message["to"] = to_email
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {
        "raw": raw_message
    }

    
    service.users().messages().send(
        userId="me",
        body=body
    ).execute()

    print("✅ Email sent successfully")
