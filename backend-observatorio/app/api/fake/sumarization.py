from flask import request, jsonify
from .. import api
from bson import ObjectId
from ...model import Manager


@api.route('/summary/<id>')
def summary(id):
    return jsonify({
        "summary": "Todav\u00eda en 1968 el colegio universitario de Yale, una de las universidades elitistas conocidas como la Ivy league, no admit\u00eda mujeres, en Cuba el impulso educativo a las mujeres humildes, campesinas y obreras hac\u00eda que su ingreso a las universidades se multiplicase por todo el pa\u00eds, de forma abierta e irrestricta, incluyendo la Universidad de la Habana.\nDe las tres universidades hist\u00f3ricas de Cuba, la Universidad de la Habana, la Universidad Central de las Villas y la Universidad de Oriente, es en esta ultima que conozca, la que hace poco ten\u00eda una rectora negra, la Dra. Martha del Carmen Mesa, hoy viceministra primera del MES."
    }
    )
