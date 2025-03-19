FROM python:3.11-slim

WORKDIR /home/campaign/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get install -y libpq-dev

COPY ./requirements.txt /home/campaign/backend/requirements.txt

RUN pip install -r requirements.txt
