FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY conf.py conf.py
# RUN chmod 744 conf.py
# RUN useradd -ms /bin/bash 1000
USER 70