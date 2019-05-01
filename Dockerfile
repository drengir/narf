FROM python:3.7
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app
COPY json_exporter.py ./
RUN apk add --update bash openssl curl openssh-client python python-pip && rm -rf /var/cache/apk/*
EXPOSE 8080
CMD ["python","./dummy.py","8080"]
