FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

RUN apt-get install -y apt-utils
RUN apt-get install -y redis-server
RUN apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

#RUN service redis-server start
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "web.py" ]