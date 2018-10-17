
import os
import json
import datetime
from flask import Flask
from flask_cors import CORS, cross_origin
#from flask_restful import Api

app = Flask(__name__)
#api = Api(app)

CORS(app)

from app import routes
