FROM python:3.11-slim

# Set the working directory
WORKDIR /home/campaign/backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file to the working directory
COPY ./requirements.txt /home/campaign/backend/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt
