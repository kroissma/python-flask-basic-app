import json
import datetime
from flask import Flask
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import configparser
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

config = configparser.ConfigParser()
config.read('config.ini')


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)

app.config['MONGO_URI'] = config['MONGODB']['URI'] + config['MONGODB']['DATABASE']
app.config['JWT_SECRET_KEY'] = config['JWT']['SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
mongo = PyMongo(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.json_encoder = JSONEncoder

CORS(app)

from app.controllers import *
