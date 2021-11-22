FROM python:3.10.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt update && apt upgrade
COPY requirements.txt /code/
RUN apt-get install libmysqlclient-dev
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pymysql mysqlclient
RUN pip install -U -r requirements.txt
COPY . /code/