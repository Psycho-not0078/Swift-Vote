FROM python:3.10.0-alpine3.14
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/sbin"

RUN mkdir /code
WORKDIR /code
RUN apk update && apk upgrade
COPY requirements.txt /code/
RUN apk add --update python3 --no-cache py3-pip gcc musl-dev mariadb-connector-c-dev

# RUN apt install python3-mysqldb python3.8-dev libmysqlclient-dev mysql-client libssl-dev libpython3.8-dev mysql-python
RUN pip install -r requirements.txt
COPY . /code/