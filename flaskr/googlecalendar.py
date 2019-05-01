from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar():


    def __init__(self):
        self.creds   = None

    def loadToken(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            self.login()

    def login(self):
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            self.creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.creds, token)

    def get(self, cal_id = "primary"):
        if not self.creds: self.loadToken()
        service = build('calendar', 'v3', credentials=self.creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=cal_id, timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events: 
            print(cal_id[:26], "-> No events found")
            return {}

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end   = event['end'].get('dateTime', event['end'].get('date'))
            if not "location" in event: event["location"] = "no room"
            print(cal_id[:26], "->", start, "-", end, event['summary'], event["location"])
        return events


if __name__ == '__main__':
    cal = Calendar()
    cal.get("a3suuihq983gnr1k7td668lmpk@group.calendar.google.com")
    cal.get("sagkegsn0eb8lesd8ej0gssnko@group.calendar.google.com")