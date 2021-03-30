# Flask-MongoDB-APIv2
Flask-based API offering CRUD operations, backend DB is MongoDB

### Setup
Create a [virtual environment for Python](https://docs.python.org/3/library/venv.html) in the current directory:
```
$ python3 -m venv .
```

Activate the virtual environment:
```
$ source bin/activate
```

**Optional**, install any dependencies:
```
(Flask-MongoDB-APIv2) python3 -m pip install --upgrade pip setuptools wheel

(Flask-MongoDB-APIv2) python3 -m pip install flask flask-mongoengine flask-bcrypt flask-restful flask-jwt-extended
```

____

### Docker-Compose

#### Build
file `Dockerfile`:
```
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
```

file `docker-compose.yaml`:
```
version: "3"

services:
  rest-api:
    container_name: apiv2
    build: .
    image: flask-mongodb-api:2.0
    environment:
      - ENV_FILE_LOCATION=.env
    ports:
      - "5000:5000"
    depends_on:
      - mongo-db
    networks:
      - frontend
      - backend
  mongo-db:
    container_name: db
    image: mongo:latest
    ports:
      - "27017:27017"
    networks:
      - backend
    volumes:
      - db_data:/data/db

networks:
  frontend:
  backend:

volumes:
  db_data:
#    external: true  # To be used if the volume is created manually
    name: mongodb_data
```

#### Run
```
(Flask-MongoDB-APIv2) docker-compose up -d
Creating network "flask-mongodb-apiv2_backend" with the default driver
Creating network "flask-mongodb-apiv2_frontend" with the default driver
Creating volume "mongodb_data" with default driver
Building rest-api
Sending build context to Docker daemon  6.227MB
...
Successfully tagged flask-mongodb-api:2.0
WARNING: Image for service rest-api was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating db ... done
Creating apiv2 ... done
```

#### Monitor
```
(Flask-MongoDB-APIv2) docker-compose ps
Name             Command             State            Ports
---------------------------------------------------------------------
api    flask run --host=0.0.0.0      Up      0.0.0.0:5000->5000/tcp
db     docker-entrypoint.sh mongod   Up      0.0.0.0:27017->27017/tcp

(Flask-MongoDB-APIv2) docker volume ls
DRIVER    VOLUME NAME
...
local     mongodb_data
...

(Flask-MongoDB-APIv2) docker inspect mongodb_data
[
    {
        "CreatedAt": "2021-03-28T16:01:15+02:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "flask-mongodb-apiv2",
            "com.docker.compose.version": "1.28.5",
            "com.docker.compose.volume": "mongodb_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/mongodb_data/_data",
        "Name": "mongodb_data",
        "Options": null,
        "Scope": "local"
    }
]
```

**NOTE**: volume `mongodb_data` gets created automatically upon launching `docker-compose`.

#### SECURITY
The DB password is passed onto the API container during the build phase through `environment` config option in `docker-compose.yaml`.<br/>
It's important to notice that, while the password is available within the container itself, the build leaves no traces of it as it can be shown by inspecting the image or displaying its history.

____

### Tests

curl http://127.0.0.1:5000/api/movies
[]%

curl -H "Content-Type: application/json" --data '{"email": "carmelo@example.com", "password": "test123"}' -X POST http://127.0.0.1:5000/api/auth/signup
{"id": "6062df650fd2f46e6d12e41c"}

curl -H "Content-Type: application/json" --data '{"email": "carmelo@example.com", "password": "test123"}' -X POST http://127.0.0.1:5000/api/auth/login
{"token": "eyJ0...UDwk"}

export TOKEN="eyJ0...UDwk"

curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" --data '{"username": "user1", "full_url": "https://www.google.com/", "short_name": "Google", "notes": ["search engine", "sergey brin", "larry page"]}' -X POST http://127.0.0.1:5000/api/vaults
{"id": "6062f667c2f387092a559f8d"}

curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" --data '{"username": "user2", "full_url": "https://www.bing.com/", "short_name": "Bing", "notes": ["search engine", "bill gates", "taylor swift"]}' -X POST http://127.0.0.1:5000/api/vaults
{"id": "6062f667c2f387092a559f8e"}

curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" --data '{"username": "user3", "full_url": "https://www.yahoo.com/", "short_name": "Yahoo", "notes": ["search engine", "outdated"]}' -X POST http://127.0.0.1:5000/api/vaults
{"id": "6062f667c2f387092a559f8f"}

curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -X DELETE http://127.0.0.1:5000/api/vaults/6062f69ec2f387092a559f8f
""

____

### Resources
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Dockerize a Flask App](https://dev.to/riverfount/dockerize-a-flask-app-17ag)
- [Setup & basic CRUD API...](https://dev.to/paurakhsharma/flask-rest-api-part-0-setup-basic-crud-api-4650)
- [Manage data in Docker](https://docs.docker.com/storage/)
- [Persistent Databases Using Docker’s Volumes and MongoDB](https://betterprogramming.pub/persistent-databases-using-dockers-volumes-and-mongodb-9ac284c25b39)

