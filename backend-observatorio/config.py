import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    AUTO_DELETE_BG_TASKS = True
    ITSFUCKINGDEBUG = True

    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/elchismoso"

    #MONGODB_DB = os.environ.get('MONGODB_DB') or 'Articles'
    #MONGODB_HOST = os.environ.get('MONGODB_HOST') or 'localhost'
    #MONGODB_PORT = os.environ.get('MONGODB_PORT') or 27017

    proxy = os.environ.get('PROXY_CONFIG')
    PROXY_CONFIG = json.loads(proxy) if proxy else {
        "http": 'http://h.canizares%40estudiantes.matcom.uh.cu:mecagoendios@proxy-cu.uh.cu:3128', "https": "http://h.canizares%40estudiantes.matcom.uh.cu:mecagoendios@proxy-cu.uh.cu:3128"}
    # MONGODB_USERNAME = 'webapp'
    # MONGODB_PASSWORD = 'pwd123'
    PROXY_CONFIG = json.loads(proxy) if proxy else {}


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    """
    The production config
    """


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
