FROM python:3.9

WORKDIR /home/campaign/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY ./requirements.txt /home/campaign/backend/requirements.txt

RUN pip install -r requirements.txt
