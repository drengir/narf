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
    time.sleep(10.0)
    cal = get_calendar()
    print(cal)
    data = {'time': time.ctime(time.time())}
    return json.dumps(data)


def get_calendar():
    cal = Calendar()
    cal.get("a3suuihq983gnr1k7td668lmpk@group.calendar.google.com")
    return cal
    

if __name__ == "__main__":
    app.run()
