from flask import Blueprint,request
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)

# from .fake import comments, sumarization
from . import crawler,  article

from .fake import comments, sumarization
# from . import comments, sumarization


@api.before_request
def before_request():
    if request.method == 'OPTIONS':
        return '', 200

