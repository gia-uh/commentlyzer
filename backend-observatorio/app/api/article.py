from flask import request, jsonify
from . import api
from ..decorators import background
from ..model import Manager, Articles
from bson import ObjectId
from datetime import datetime
from Crawler import Crawler
import logging
from flask import current_app as app

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
    page = int(request.args.get('page', '1'))
    filt = request.args.get('filter', '')
    # logger.debug('page: '+str(page))
    # logger.debug('filter: '+str(filt)+'\ttype: '+str(type(filt)))
    if not filt:
        articles = Articles.top_page(page)
        na = Articles.count_articles()
        ap = Articles.arts_per_page
        nn = na//ap
        rest = na % ap
        nn += int(bool(rest != 0))
    else:
        articles, na = Articles.top_page_filter(page, filt)
        ap = Articles.arts_per_page
        nn = na//ap
        rest = na % ap
        nn += int(bool(rest != 0))

    # logger.debug(articles)

    return jsonify({
        'articles': articles,
        'pages': nn,
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
    data = Crawler(app.config['PROXY_CONFIG'])
    data.request(art['url'])
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
    data = Crawler(app.config['PROXY_CONFIG'])
    data.request(art['url'])
    cc = data.comment
    logger.debug("{0}".format(len(cc)))
    if len(cc) > art['comments']:
        cc = cc[art['comments']:]
        Manager.add_comments_now(artt.id, cc)
    Manager.update_last_update(artt.id)
    return jsonify({'id': str(id)})


