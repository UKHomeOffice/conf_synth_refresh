FROM python:3.8
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY conf-synth-data.py .
COPY automate-setup.py .
COPY installplugins.sh .
RUN chmod 754 installplugins.sh
COPY conf_plugins/ conf_plugins/
USER 70