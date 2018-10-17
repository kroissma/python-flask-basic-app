# Flask Demo App

## Installing
Install using [pipenv](https://github.com/pypa/pipenv):

```shell
pipenv install
pipenv shell
```

## Preparing MongoDB from Docker image

```shell
docker run -p 27017:27017 --name mongodb -d mongo

# check if the db is running
docker ps

# to stop the database:
docker stop <name|CONTAINER ID>

# start the container again
docker start <name>
# or start the docker container with the interactive shell
docker exec -it mongodb mongo
```

[MongoDB Shell Cheat Sheet](https://www.opentechguides.com/how-to/article/mongodb/118/mongodb-cheatsheat.html)

## Running the App

```shell
export FLASK_APP=index.py
export FLASK_DEBUG=1
flask run
```

The server will run on http://127.0.0.1:5000.
The debug flag forces the server to restart after files changed.
