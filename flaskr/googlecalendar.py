from __future__ import print_function
import datetime, time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar():
    """ User is hardcorded, only calender can be changed """

    def __init__(self):
        self.creds   = None

    def load_token(self):
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

    def get_events(self, cal_id = "primary"):
        if not self.creds: self.load_token()
        service = build('calendar', 'v3', credentials=self.creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=cal_id, timeMin=now,
                                              maxResults=2, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events: 
            print(cal_id[:26], "-> No events found")
            return {}

        date_format = '%Y-%m-%d'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end   = event['end'].get('dateTime', event['end'].get('date'))
            date   = start.split("T")[0]
            start2 = start.split("T")[1].split("+")[0]
            end2   = end.split("T")[1].split("+")[0]
            if not "location" in event: event["location"] = "no room"
            print(cal_id[:26], "->", start, "-", end, event['summary'], event["location"])
            event["startTime"] = start2
            event["endTime"]   = end2
            event["eventDate"] = date
            if event == events[0]: event["mainEvent"] = True
            else:                  event["mainEvent"] = False
        return events


if __name__ == '__main__':
    cal = Calendar()
    cal.get_events("a3suuihq983gnr1k7td668lmpk@group.calendar.google.com")
    cal.get_events("sagkegsn0eb8lesd8ej0gssnko@group.calendar.google.com")
