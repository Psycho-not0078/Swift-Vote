FROM python:alpine
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/sbin"

RUN mkdir /code
WORKDIR /code
RUN apk update && apk upgrade
COPY ./Swift_Vote/requirements.txt /code/
RUN apk add --update python3 --no-cache py3-pip gcc musl-dev mariadb-connector-c-dev

# RUN apt install python3-mysqldb python3.8-dev libmysqlclient-dev mysql-client libssl-dev libpython3.8-dev mysql-python
RUN pip3 install -r requirements.txt
COPY ./Swift_Vote/ /code/
# COPY ./init.sh /code/init.sh
# RUN chmod +x init.sh