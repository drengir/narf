FROM arm32v7/debian:stretch-slim 
COPY qemu-arm-static /usr/bin
LABEL maintainer=vikings<containersolutions@mobi.ch>
WORKDIR /usr/src/app

RUN \
  echo "deb-src http://deb.debian.org/debian stretch main" >> /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y --no-install-recommends install apt-utils bash python3 python3-pip wget zip gcc autoconf automake libtool pkg-config make cmake usbutils && \
  wget https://github.com/xantares/nfc-bindings/archive/master.zip && \
  wget https://github.com/nfc-tools/libnfc/archive/libnfc-1.7.1.tar.gz && \
  unzip master.zip && \
  tar xvfz libnfc-1.7.1.tar.gz && \
  sh -c "echo /usr/local/lib > /etc/ld.so.conf.d/usr-local-lib.conf" && \
  ldconfig

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir &&\
    pip3 install pylint && \
    pylint --disable=C *.py
COPY flaskr ./

WORKDIR /usr/src/app/libnfc-libnfc-1.7.1
RUN \
  autoreconf -vis && \
  ./configure --with-drivers=pn532_i2c --prefix=/usr --sysconfdir=/etc && \
  make clean && \
  make && \
  make install && \
  mkdir /etc/nfc && \
  echo "device.name = 'PN532'\ndevice.connstring = pn532_i2c:/dev/i2c-1" >> /etc/nfc/libnfc.conf
 
WORKDIR /usr/src/app/nfc-bindings-master
RUN \
  cmake -DCMAKE_INSTALL_PREFIX=~/.local . && \
  make install

WORKDIR /usr/src/app
EXPOSE 5000
CMD ["python3","./server.py"]
