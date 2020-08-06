# pull official base image
FROM python:3.8.3-alpine

# File Author / Maintainer
MAINTAINER Krzysztof Lopatynski <krzysztof.lopatynski@gmail.com>

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV HTTP_PROXY http://address:port
# ENV HTTPS_PROXY http://address:port

################## BEGIN INSTALLATION ######################
# Add system packages
RUN apk --no-cache add \
    linux-headers bash gcc libressl-dev musl-dev libffi-dev\
    libjpeg-turbo-dev libpng libpq \
    python3-dev mariadb-dev \
    mariadb-client uwsgi uwsgi-python3 openssh 

    
RUN pip install --upgrade pip

# copy project
COPY . /app

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
