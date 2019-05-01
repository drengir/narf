import time
import json
import os

from flask import Flask
from flask import render_template
from flask import Response
from googlecalendar import Calendar

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.jinja')

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(event_stream(), mimetype="text/event-stream")

def get_message():
    # blocks for new id
    batch_id = nfc.get_id()

    # return empty page
    if batch_id is None:
        print("batch_id is non, resetting to start page")
        with app.app_context():
            jinja_render = render_template('welcome.jinja')
            data = {'time': time.ctime(time.time()), 'calendarEvents': jinja_render}
            return json.dumps(data)

    calendar_id = map_nfc_to_calendar_id(batch_id)

    events = cal.get_events(calendar_id)
    if not events:
        data = {'time': time.ctime(time.time()), 'calendarEvents': "Calendar not found :-("}
        return json.dumps(data)

    with app.app_context():
        jinja_render = render_template('calendar.jinja', events = events)

    data = {'time': time.ctime(time.time()), 'calendarEvents': jinja_render}
    return json.dumps(data)


def get_calendar():
    cal = Calendar()
    return cal

def get_nfc():
    use_mock = 'USE_NFC_MOCK' in os.environ and os.environ['USE_NFC_MOCK'].lower() == "true"
    if use_mock:
        from nfc_client_mock import Nfc
        print("using NFC mock!")
        return Nfc()
    try:
        from nfc_client import Nfc
    except:
        print("Couldn't load NFC, falling back to mock!")
        from nfc_client_mock import Nfc
    return Nfc()

def map_nfc_to_calendar_id(batch_id):
    if batch_id == 'mock_id':
        return "a3suuihq983gnr1k7td668lmpk@group.calendar.google.com"
    return None

nfc = get_nfc()
cal = get_calendar()

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
