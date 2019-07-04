from flask import request, jsonify
from flask import current_app as app
from Crawler import CubaDebate, Crawler
from . import api
from ..decorators import background_tasks, background_optional
from .article import get_data
from ..model import Manager
import datetime
from hashlib import sha1
import logging
import re
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

    app.logger.info('inserting Notice and Comments')
    # id = Manager.insert_art(data.data)
    id = Manager.new_entry(data.data, comments)

    return jsonify({'id': str(id)})


