from flask import request, jsonify
from flask import current_app as app
from CubaCrawler import Crawler
from CommenlyzerEngine import extract_opinion
from bson import ObjectId
from collections import Counter
from . import api
from ..decorators import background_tasks, background_optional
from .article import get_data
from ..model import Manager
import datetime
from hashlib import sha1
import logging
import re
from .comments import stopwordsd
from ..decorators import background

sps = re.compile('  +')


@api.route('/getpage', methods=['POST'])
@background_optional
def get_page():
    data = request.json
    print(data)
    url = data['url']

    id = Manager.search_url(url)

    if id is not None:
        # return jsonify({'id': str(id)})
        return get_data(str(id))

    data = Crawler(app.config['PROXY_CONFIG'])
    data.request(url)

    tt = datetime.datetime.utcnow()

    dat = data.data

    dat['url'] = url
    # inyecta un campo update_time con la fecha donde
    # se escrapeo el articulo
    dat['last_update'] = tt
    dat['media'] = data.source
    comments = data.comment
    # print(comments)
    # comments_clean = []
    # for i in comments:
    #     tt = i['text']
    #     tt = tt.strip()
    #     tt = sps.sub(' ',tt)
    #     tt1 = tt.lower()
    #     i['text'] = tt
    #     comments_clean.append(i)

    opinion = extract_opinion([comment['text'] for comment in comments])
    words = Counter()
    for c,o in zip(comments,opinion):
        c['opinion']=o
        for j in c['text'].split(' '):
            if not(j in stopwordsd):
                words[j]+=1
    counter = Counter(opinion)
    ress = {
       'Positivo': counter['Positivo'],
       'Neutro': counter['Neutro'],
       'Negativo': counter['Negativo'],
       'Objetivo': counter['Objetivo']
    }
    dat['opinion'] = 'Neutro'

    app.logger.info('inserting Notice and Comments')
    # id = Manager.insert_art(data.data)
    id = Manager.new_entry(data.data, comments)
    words = [{"name": i,"value":j} for i,j in sorted(words.items(),key=lambda x:x[1], reverse=True)]
    Manager.inser_ops(ObjectId(id),ress, tt)
    Manager.inser_wc(ObjectId(id),words, tt)

    return jsonify({'id': str(id)})


