from flask import request, jsonify
from . import api
from ..decorators import background
from ..model import Manager, Articles
from bson import ObjectId
from datetime import datetime
from Crawler import CubaDebate
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('articles')
logger.setLevel(logging.DEBUG)


@api.route('/article/<id>')
def get_data(id):

    article = Articles(id).to_article()

    return jsonify(article)

@api.route('/article/paginate')
def get_topten_paginate():

    # return jsonify({'funciona':1})
    page=int(request.args.get('page',''))
    logger.debug('page: '+str(page))
    articles = Articles.topten_page(page)
    na = Articles.count_articles()
    ap = Articles.arts_per_page
    nn = na//ap
    rest = na % ap
    nn += int(bool(rest != 0))
    nextt = page+1
    if nextt> nn:
        nextt = None

    logger.debug(articles)

    return jsonify({
        'articles': articles,
        'pages': nn,
        'next': nextt
    })


@api.route('/article/topten')
def get_topten():
    articles = Articles.topten()

    return jsonify({
        'articles': articles,
    })

@api.route('/article/get_update/<id>')
def method_name():
    artt = Articles(id)
    art = artt.to_article()
    data = CubaDebate(art['url'])
    cc = data.comment
    if len(cc) > art['comments']:
        cc = cc[art['comments']:]
        Manager.add_comments(artt.id, cc)
    Manager.update_last_update(artt.id)
    article = Articles(id).to_article()
    return jsonify(article)


@api.route('/article/update/<id>')
@background
def update_article(id):
    artt = Articles(id)
    art = artt.to_article()
    data = CubaDebate(art['url'])
    cc = data.comment
    if len(cc) > art['comments']:
        cc = cc[art['comments']:]
        Manager.add_comments(artt.id, cc)
    Manager.update_last_update(artt.id)
    return jsonify({'id': str(id)})


