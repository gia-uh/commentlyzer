from flask import request, jsonify
from . import api
from bson import ObjectId
from ..model import Manager


@api.route('/summary/<id>')
def summary(id):
    return jsonify({'summary': 'Este resumen es de prueba.'})
