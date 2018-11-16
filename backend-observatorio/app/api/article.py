from flask import request, jsonify
from . import api
from ..decorators import background_tasks
from ..model import Manager, Articles
from bson import ObjectId
from datetime import datetime
from Crawler import CubaDebate


@api.route('/article/<id>')
def get_data(id):

    article = Articles(id).to_article()

    return jsonify(article)


@api.route('/article/topten')
def get_topten():
    articles = Articles.topten()

    return jsonify({
        'articles': articles
    })


@api.route('/article/update/<id>')
def update_article(id):
    artt = Articles(id)
    art = artt.to_article()
    data = CubaDebate(art['url'])
    cc = data.comment
    if len(cc) > art['comments']:
        cc = cc[art['comments']:]
        Manager.add_comments(artt.id,cc)
    Manager.update_last_update(artt.id)
    return jsonify({'id': str(id)})


