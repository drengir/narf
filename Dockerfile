FROM arm32v7/debian:stretch-slim 
COPY qemu-arm-static /usr/bin
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flaskr ./
 
EXPOSE 5000
CMD ["python","./server.py"]
