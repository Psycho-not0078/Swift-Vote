FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/sbin"

RUN mkdir /code
RUN apt update && apt upgrade
RUN apt install python3 
COPY ./Swift_Vote/requirements.txt /code/
RUN pip3 install -r /code/requirements.txt
# RUN apk update && apk add wget && \
# wget -O /usr/bin/solc-v0.8.11 https://github.com/ethereum/solidity/releases/download/v0.8.11/solc-static-linux
# RUN apt install python3-mysqldb python3.8-dev libmysqlclient-dev mysql-client libssl-dev libpython3.8-dev mysql-python
# RUN chmod +x /usr/bin/solc-v0.8.11
RUN mkdir /root/.solcx
# RUN cp /usr/bin/solc-v0.8.11 /root/.solcx/solc-v0.8.11
RUN python3 -c 'import solcx;solcx.install_solc_pragma(">0.8.0")'  
WORKDIR /code
COPY ./Swift_Vote/ /code/
# COPY ./init.sh /code/init.sh
# RUN chmod +x init.sh