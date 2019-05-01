import time
import json

from flask import Flask
from flask import render_template
from flask import Response
from googlecalendar import Calendar

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(event_stream(), mimetype="text/event-stream")

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(5.0)
    cal = get_calendar()
    event_str = ''
    for event in cal.get_events():
        with app.app_context():
            event_str += render_template('event.html', event=event)
    print(event_str)

    data = {'time': time.ctime(time.time()), 'calendarEvents': event_str}
    return json.dumps(data)


def get_calendar():
    cal = Calendar()
    return cal
    
if __name__ == "__main__":
    app.run()
