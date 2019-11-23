from flask import request, jsonify
from . import api
from CommenlyzerEngine import text_summarize
from bson import ObjectId
from ..model import Manager
#from ..decorators import background_tasks


@api.route('/summary/<id>')
def summary(id):
    article = Manager.get_article(ObjectId(id))
    ans = text_summarize(article['text'])
    return jsonify({'summary':ans})
