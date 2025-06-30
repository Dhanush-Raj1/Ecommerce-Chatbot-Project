FROM apache/airflow:slim-2.10.5-python3.9

# root user for installing dependencies 
USER root          

# Install system dependencies for Pillow, other image libraries and Chromium, ChromeDriver
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    tk-dev \
    tcl-dev \
    python3-dev \
    gcc \
    chromium \
    chromium-driver \
    && apt-get clean

# airflow user for installing required libraries
USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

