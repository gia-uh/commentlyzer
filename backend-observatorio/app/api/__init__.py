from flask import Blueprint,request
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)

from . import crawler, comments, article, sumarization

@api.before_request
def before_request():
    if request.method == 'OPTIONS':
        return '', 200

