#  download oficial image of Docker Python
FROM python:3.11

#  Set enviropnment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#  Set the working directory in the container
WORKDIR /TI_Management

# Install system dependencies
RUN pip install --upgrade pip
COPY requirements.txt /TI_Management/
RUN pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /TI_Management/