import time
import json
import os
import threading
from queue import Queue

from flask import Flask
from flask import render_template
from flask import Response
from googlecalendar import Calendar

app = Flask(__name__)
send_queue = Queue()

def poll_loop():
    print("Poll loop startet")
    while True:
        with app.app_context():
            get_message()

@app.route('/')
def root():
    return render_template('index.jinja')

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(send_queue.get())
    return Response(event_stream(), mimetype="text/event-stream")

def get_message():
    # blocks for new id
    batch_id = nfc.get_id()

    # return empty page
    if batch_id is None:
        print("batch_id is empty, resetting to start page")
        send_event(render_template('welcome.jinja'))
        return

    calendar_id = map_nfc_to_calendar_id(batch_id)
    if calendar_id is None:
        print('No mapping for id {} found'.format(batch_id))
        send_event(render_template('slacktime.jinja'))
        return

    send_event(render_template('loading.jinja'))
    events = cal.get_events(calendar_id)
    if not events:
        send_event(render_template('slacktime.jinja'))
        return
    send_event(render_template('calendar.jinja', events = events))

def send_event(jinja_render):
    data = {'time': time.ctime(time.time()), 'calendarEvents': jinja_render}
    send_queue.put(json.dumps(data))

def get_calendar():
    return  Calendar()

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
    return nfc_mapping.get(batch_id)

nfc = get_nfc()
cal = get_calendar()
nfc_mapping = {
    'mock_id': 'a3suuihq983gnr1k7td668lmpk@group.calendar.google.com',
    '2306301066': 'a3suuihq983gnr1k7td668lmpk@group.calendar.google.com',
    '528197766': 'sagkegsn0eb8lesd8ej0gssnko@group.calendar.google.com'
}

if __name__ == "__main__":
    x = threading.Thread(target=poll_loop, daemon=True)
    x.start()
    app.run(host = "0.0.0.0")
