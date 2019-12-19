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
        'Negativo': 10,
        'Objetivo': 10
    })


@api.route('/comments/entities/<ObjectId:id>')
def entities(id):

    return jsonify({
        "entities": [
            {
                "count": {
                    "Negativo": 3,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 4,
                    'Objetivo': 1
                },
                "name": "Rectora"
            },
            {
                "count": {
                    "Negativo": 3,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 4,
                     'Objetivo': 1
                },
                "name": "Rector"
            },
            {
                "count": {
                    "Negativo": 2,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 3,
                     'Objetivo': 1
                },
                "name": "UCI"
            },
            {
                "count": {
                    "Negativo": 2,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 3,
                    'Objetivo': 1
                },
                "name": "Miriam"
            },
            {
                "count": {
                    "Negativo": 2,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 3,
                    'Objetivo': 1
                },
                "name": "UH"
            },
            {
                "count": {
                    "Negativo": 1,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 2,
                    'Objetivo': 1
                },
                "name": "Dra"
            },
            {
                "count": {
                    "Negativo": 1,
                    "Neutro": 1,
                    "Positivo": 0,
                    "total": 2,
                    'Objetivo': 1
                },
                "name": "El proceso"
            },
            {
                "count": {
                    "Negativo": 0,
                    "Neutro": 1,
                    "Positivo": 1,
                    "total": 2,
                    'Objetivo': 1
                },
                "name": "UCLV"
            },
            {
                "count": {
                    "Negativo": 1,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 2,
                    'Objetivo': 1
                },
                "name": "Nicado"
            },
            {
                "count": {
                    "Negativo": 0,
                    "Neutro": 0,
                    "Positivo": 1,
                    "total": 1,
                    'Objetivo': 1
                },
                "name": "UNAH"
            }
        ]
    }
    )

@api.route('/comments/wrodcloud/<ObjectId:id>')
def comments_wc(id):

    data = {
        "words": [
            {
                "name": "Fidel",
                "value": 96
            },
            {
                "name": ">",
                "value": 78
            },
            {
                "name": "siempre",
                "value": 65
            },
            {
                "name": "cada",
                "value": 57
            },
            {
                "name": "ser",
                "value": 43
            },
            {
                "name": "pueblo",
                "value": 43
            },
            {
                "name": "FIDEL",
                "value": 41
            },
            {
                "name": "mundo",
                "value": 36
            },
            {
                "name": "más",
                "value": 35
            },
            {
                "name": "voluntad",
                "value": 34
            },
            {
                "name": "Y",
                "value": 33
            },
            {
                "name": "monumento",
                "value": 32
            },
            {
                "name": "hombre",
                "value": 31
            },
            {
                "name": "FIDEL,",
                "value": 30
            },
            {
                "name": "nombre",
                "value": 30
            },
            {
                "name": "si",
                "value": 30
            },
            {
                "name": "SIEMPRE",
                "value": 29
            },
            {
                "name": "obra",
                "value": 26
            },
            {
                "name": "vida",
                "value": 26
            },
            {
                "name": "él",
                "value": 25
            }
        ]
    }
    return data
