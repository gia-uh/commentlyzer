from flask import request, jsonify
from . import api
from datetime import datetime
from ..model import Manager
from bson import ObjectId
from pandas import DataFrame
import pandas as pd
from collections import Counter
from flask import current_app as app
import json
import requests
import re

@api.route('/comments/time/<string:id>')
def timeline(id):
    comments = list(Manager.interval_comments(ObjectId(id), datetime.now()))

    # Hack for agroup by time
    df = DataFrame(data={'date': [comment['date'] for comment in comments], 'id': [comment['_id'] for comment in comments]})
    if df.empty:
        return jsonify({})
    fs=df.groupby(pd.Grouper(key='date', freq='3600S'))

    ans = [(str(v[0]), len(v[1])) for v in fs]
    tans = {}
    for i, (date, count) in enumerate(ans):
        if i == 0 or i == len(ans)-1:
            tans[date] = count
            continue

        if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
            continue

        tans[date] = count

    return jsonify(tans)



@api.route('/comments/opinion/<ObjectId:id>')
def comments_opinion(id):

    return jsonify({
        'Positivo': 10,
        'Neutro': 10,
        'Negativo': 10
    })


@api.route('/comments/entities/<ObjectId:id>')
def entities(id):

    return jsonify({
        "entities": [
            {
                "name": "Etecsa (esto)",
                "count": {
                    "total": 30,
                    "positive": 20,
                    'negative': 30,
                    'neutral': 50
                }
            },
            {
                "name": "Guagua (está)",
                "count": {
                    "total": 30,
                    "positive": 0.2,
                    'negative': 0.3,
                    'neutral': 0.5
                }
            },
            {
                "name": "Guagua (cableado)",
                "count": {
                    "total": 30,
                    "positive": 0.2,
                    'negative': 0.3,
                    'neutral': 0.5
                }
            }
        ]
    })
