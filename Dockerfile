FROM python:3.9-slim-buster
MAINTAINER "carmelo.califano@gmail.com"

WORKDIR /srv

COPY .env app.py requirements.txt /srv/
COPY database /srv/database/
COPY resources /srv/resources/
RUN pip3 install -r requirements.txt

ENV FLASK_APP "/srv/app.py"
EXPOSE 5000/tcp
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
