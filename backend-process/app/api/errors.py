from flask import jsonify
from ..exceptions import ValidationError
from . import api


@api.errorhandler(ValidationError)
def bad_request(e=None):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response


@api.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(e=None):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@api.errorhandler(405)
def method_not_supported(e=None):
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


@api.app_errorhandler(500)  # this has to be an app-wide handler
def internal_server_error(e=None):
    msg = e.args[0] if e.args else 'Unknow error'
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': msg})
    response.status_code = 500
    return response
