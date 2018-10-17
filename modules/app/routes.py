from app import app
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

@app.route('/')
@app.route('/index')
def index():
    return config['MONGODB']['URI']
