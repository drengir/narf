FROM drengir/nfc-bindings:latest
COPY qemu-arm-static /usr/bin
LABEL maintainer=vikings<containersolutions@mobi.ch>

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY flaskr ./

WORKDIR /usr/src/app
EXPOSE 5000
CMD ["python3","./server.py"]
