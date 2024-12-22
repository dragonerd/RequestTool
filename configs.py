from flask import Flask, g
import configparser
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

app = Flask(__name__)


def load_config():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config

config = load_config()

text_data = {
    'key1': config['INDEX']['key1'],
    'key2': config['INDEX']['key2'],
    'key3': config['INDEX']['key3'],
    'key4': config['INDEX']['key4'],
    'version': config['INDEX']['version']
}

#ENABLE DISABLE DUMMY DATABASE
dummy_database = config.getboolean('DATABASE', 'DummyDB')
app.config['DUMMY_DATABASE'] = dummy_database
valor_booleano = config.getboolean('DATABASE', 'DummyDB')
print(f'\033[1;32m[DUMMY DATABASE] = {dummy_database}\033[0m')

app.jinja_env.globals['dummy_database'] = dummy_database

#SECRET KEY 
SECRET_KEY = config['App']['SECRET_KEY']
app.config['SECRET_KEY'] = SECRET_KEY

#Variables Flask 
server_port = int(config['Server']['port'])
server_host = config['Server']['host']
print(f'\033[1;32m[FLASK DATA SERVER] PORT:{server_port} - HOST {server_host}\033[0m')

#Debug Mode
debug_state = config.getboolean('App', 'DebugMode')
app.config['DEBUG'] = debug_state
valor_booleano = config.getboolean('App', 'DebugMode')
print(f'\033[1;32m[DEBUG MODE] = {debug_state}\033[0m')

#Instancias server
sqlalchemy_url = config['Database']['sqlalchemy.url']
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_url

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
db.init_app(app)