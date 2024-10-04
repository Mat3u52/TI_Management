#  download oficial image of Docker Python
FROM python:3.11.9

#  Set enviropnment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#  Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install uwsgi

# Copy the entire Django project into the container
COPY . /code/