# Doctor Appointment Assistant
![Alt text](https://github.com/varunseth578/smart-doctor/blob/1252b5bd22515aba808d7527c00b8d5feb934934/Screenshot%202026-02-15%20212947.png)
![Alt text](https://github.com/varunseth578/smart-doctor/blob/1252b5bd22515aba808d7527c00b8d5feb934934/Screenshot%202026-02-15%20213011.png)
![Alt text](https://github.com/varunseth578/smart-doctor/blob/1252b5bd22515aba808d7527c00b8d5feb934934/Screenshot%202026-02-15%20213032.png)


An AI-powered Doctor Appointment Assistant that allows users to check doctor availability, book appointments, create Google Calendar events, and send confirmation emails automatically.

Built using:
FastAPI (Backend)
React.js (Frontend)
PostgreSQL / SQLite (Database)
OpenRouter AI (LLM Agent)
Google Calendar API
Gmail API


Backend Setup

1. Create virtual environment

```bash
python -m venv myenv
```

Activate:

```bash
myenv\Scripts\activate
```


2. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install requests python-dotenv
```


3. Setup Google APIs

Enable:
Google Calendar API
Gmail API

Download:
```bash
credentials.json
```

Place inside:
```bash
backend/
```


6. Start backend

```bash
uvicorn main:app --reload
```


Frontend Setup

Go to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start React app:

```bash
npm start
```


Sample Prompts

Example 1:
```
Book appointment with Dr. Sharma
```

Example 2:
```
My name is Varun Seth
```

Example 3:
```
25-02-2026
```

Example 4:
```
3:00 PM
```

Example final response:
```
Appointment Confirmed ✅
Confirmation email sent successfully.
```


API Usage

POST /chat

Endpoint:
```bash
POST http://127.0.0.1:8000/chat
```


Technologies Used

FastAPI
React.js
PostgreSQL / SQLite
SQLAlchemy
Google Calendar API
Gmail API
OpenRouter API
Python

