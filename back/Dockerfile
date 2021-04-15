FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
COPY media ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /home/back
WORKDIR /home/back