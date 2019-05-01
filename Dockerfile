FROM arm32v7/debian:stretch-slim 
COPY qemu-arm-static /usr/bin
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app
RUN apt-get -y --no-install-recommends install apt-utils bash openssl curl openssh-client python python-pip 
EXPOSE 3000
CMD ["python","./dummy.py","3000"]
