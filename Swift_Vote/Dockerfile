FROM python:3.10.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt update && apt upgrade
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/