FROM arm32v7/debian:stretch-slim 
COPY qemu-arm-static /usr/bin
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app

RUN \
  echo "deb-src http://deb.debian.org/debian stretch main" >> /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y --no-install-recommends install apt-utils bash openssl curl openssh-client python python-pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flaskr ./
 
EXPOSE 5000
CMD ["python","./server.py"]
