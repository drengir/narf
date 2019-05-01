FROM python:3.7
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flaskr ./
 
EXPOSE 5000
CMD ["python","./server.py"]
