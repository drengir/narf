#!/bin/bash
set -e

docker build -t narf .
docker run -it -p 5000:5000 narf
