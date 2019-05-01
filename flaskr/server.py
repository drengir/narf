import time

from flask import Flask
from flask import render_template
from flask import Response

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World!'

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
    time.sleep(1.0)
    current_time = time.ctime(time.time())
    return current_time


if __name__ == "__main__":
    app.run()
