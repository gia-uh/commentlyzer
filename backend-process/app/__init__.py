from flask import Flask
from config import config
from flask_cors import CORS
import logging
from flask_pymongo import PyMongo



# crawler = CubaDebate()
mongo = PyMongo()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mongo.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
