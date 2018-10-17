# Flask Demo App

## Installing
Install using [pipenv](https://github.com/pypa/pipenv):

```shell
pipenv install
pipenv shell
```

## Running the App

```shell
export FLASK_APP=index.py
export FLASK_DEBUG=1
flask run
```

The server will run on http://127.0.0.1:5000.
The debug flag forces the server to restart after files changed.
