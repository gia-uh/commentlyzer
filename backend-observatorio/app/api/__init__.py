from flask import Blueprint,request
from flask_cors import CORS
import os
import importlib

api = Blueprint('api', __name__)
CORS(api)

from . import crawler,  article, task
#comments = None
#sumarization = None
task = None
#from .fake import comments, sumarization

real = os.getenv('REAL_PROCESS')

if real=='1':
    #global comments, sumarization
    #comments = importlib.import_module('comments','.')
    #sumarization = importlib.import_module('sumarization','.')
    exec('from . import comments, sumarization',globals())
else:
    #global comments, sumarization
    #comments = importlib.import_module('comments','.fake')
    #sumarization = importlib.import_module('sumarization','.fake')
    exec('from .fake import comments, sumarization',globals())

@api.before_request
def before_request():
    if request.method == 'OPTIONS':
        return '', 200

