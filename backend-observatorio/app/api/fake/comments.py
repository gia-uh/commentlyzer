from flask import request, jsonify
from .. import api
from datetime import datetime
from ...model import Manager
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
                "count": {
                    "negative": 3,
                    "neutral": 0,
                    "positive": 1,
                    "total": 4
                },
                "name": "Rectora"
            },
            {
                "count": {
                    "negative": 3,
                    "neutral": 0,
                    "positive": 1,
                    "total": 4
                },
                "name": "Rector"
            },
            {
                "count": {
                    "negative": 2,
                    "neutral": 0,
                    "positive": 1,
                    "total": 3
                },
                "name": "UCI"
            },
            {
                "count": {
                    "negative": 2,
                    "neutral": 0,
                    "positive": 1,
                    "total": 3
                },
                "name": "Miriam"
            },
            {
                "count": {
                    "negative": 2,
                    "neutral": 0,
                    "positive": 1,
                    "total": 3
                },
                "name": "UH"
            },
            {
                "count": {
                    "negative": 1,
                    "neutral": 0,
                    "positive": 1,
                    "total": 2
                },
                "name": "Dra"
            },
            {
                "count": {
                    "negative": 1,
                    "neutral": 1,
                    "positive": 0,
                    "total": 2
                },
                "name": "El proceso"
            },
            {
                "count": {
                    "negative": 0,
                    "neutral": 1,
                    "positive": 1,
                    "total": 2
                },
                "name": "UCLV"
            },
            {
                "count": {
                    "negative": 1,
                    "neutral": 0,
                    "positive": 1,
                    "total": 2
                },
                "name": "Nicado"
            },
            {
                "count": {
                    "negative": 0,
                    "neutral": 0,
                    "positive": 1,
                    "total": 1
                },
                "name": "UNAH"
            }
        ]
    }
    )
