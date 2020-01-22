from flask import request, jsonify
from . import api
from datetime import datetime
from ..model import Manager
from bson import ObjectId
from pandas import DataFrame
import pandas as pd
from CommenlyzerEngine import extract_opinion
from CommenlyzerEngine.entities import pipe_ents_detect
from collections import Counter
from flask import current_app as app
import json
import requests
import re

stopwordsd = set(["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como", "m\\u00e1s", "pero", "sus", "le", "ya", "o", "este", "s\\u00ed", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "tambi\\u00e9n", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "m\\u00ed", "antes", "algunos", "qu\\u00e9", "unos", "yo", "otro", "otras", "otra", "\\u00e9l", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "t\\u00fa", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosostros", "vosostras", "os", "m\\u00edo", "m\\u00eda", "m\\u00edos", "m\\u00edas", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "est\\u00e1s", "est\\u00e1", "estamos", "est\\u00e1is", "est\\u00e1n", "est\\u00e9", "est\\u00e9s", "estemos", "est\\u00e9is", "est\\u00e9n", "estar\\u00e9", "estar\\u00e1s", "estar\\u00e1", "estaremos", "estar\\u00e9is", "estar\\u00e1n", "estar\\u00eda", "estar\\u00edas", "estar\\u00edamos", "estar\\u00edais", "estar\\u00edan", "estaba", "estabas", "est\\u00e1bamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvi\\u00e9ramos", "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuvi\\u00e9semos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "hab\\u00e9is", "han", "haya", "hayas", "hayamos", "hay\\u00e1is", "hayan", "habr\\u00e9", "habr\\u00e1s", "habr\\u00e1", "habremos", "habr\\u00e9is", "habr\\u00e1n", "habr\\u00eda", "habr\\u00edas", "habr\\u00edamos", "habr\\u00edais", "habr\\u00edan", "hab\\u00eda", "hab\\u00edas", "hab\\u00edamos", "hab\\u00edais", "hab\\u00edan", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras", "hubi\\u00e9ramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubi\\u00e9semos", "hubieseis", "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "se\\u00e1is", "sean", "ser\\u00e9", "ser\\u00e1s", "ser\\u00e1", "seremos", "ser\\u00e9is", "ser\\u00e1n", "ser\\u00eda", "ser\\u00edas", "ser\\u00edamos", "ser\\u00edais", "ser\\u00edan", "era", "eras", "\\u00e9ramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fu\\u00e9ramos", "fuerais", "fueran", "fuese", "fueses", "fu\\u00e9semos", "fueseis", "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "ten\\u00e9is", "tienen", "tenga", "tengas", "tengamos", "teng\\u00e1is", "tengan", "tendr\\u00e9", "tendr\\u00e1s", "tendr\\u00e1", "tendremos", "tendr\\u00e9is", "tendr\\u00e1n", "tendr\\u00eda", "tendr\\u00edas", "tendr\\u00edamos", "tendr\\u00edais", "tendr\\u00edan", "ten\\u00eda", "ten\\u00edas", "ten\\u00edamos", "ten\\u00edais", "ten\\u00edan", "tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron", "tuviera", "tuvieras", "tuvi\\u00e9ramos", "tuvierais", "tuvieran", "tuviese", "tuvieses", "tuvi\\u00e9semos", "tuvieseis", "tuviesen", "teniendo", "tenido", "tenida", "tenidos", "tenidas", "tened"])
ENTITIES_NUMBER = 5
WRODS_NUMBER = 20

@api.route('/comments/time/<string:id>')
def timeline(id):
    comments = list(Manager.interval_comments(ObjectId(id), datetime.now()))

    # Hack for agroup by time
    df = DataFrame(data={'date': [comment['date'] for comment in comments], 'id': [
                   comment['_id'] for comment in comments]})
    if df.empty:
        return jsonify([{},{},{},{}])
    fs = df.groupby(pd.Grouper(key='date', freq='3600S'))

    # opinion = extract_opinion([comment['text'] for comment in comments])

    ans = [(str(v[0]), len(v[1])) for v in fs]
    tans = {}

    for i, (date, count) in enumerate(ans):
        if i == 0 or i == len(ans)-1:
            tans[date] = count
            continue

        if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
            continue

        tans[date] = count

    # TODO: terminer lo de los graficos, copiar lo de arriba cuatro veces con un if en los list comprehension de el dataframe
    df = DataFrame(data={'date': [comment['date'] for comment in comments if comment['opinion']=='Positivo'], 'id': [
                   comment['_id'] for comment in comments if comment['opinion']=='Positivo']})
    if df.empty:
        tanspos = {}
    else:
        fs = df.groupby(pd.Grouper(key='date', freq='3600S'))

        # opinion = extract_opinion([comment['text'] for comment in comments])

        ans = [(str(v[0]), len(v[1])) for v in fs]
        tanspos = {}

        for i, (date, count) in enumerate(ans):
            if i == 0 or i == len(ans)-1:
                tanspos[date] = count
                continue

            if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
                continue

            tanspos[date] = count

    df = DataFrame(data={'date': [comment['date'] for comment in comments if comment['opinion']=='Negativo'], 'id': [
                   comment['_id'] for comment in comments if comment['opinion']=='Negativo']})
    if df.empty:
        tansneg = {}
    else:
        fs = df.groupby(pd.Grouper(key='date', freq='3600S'))

        # opinion = extract_opinion([comment['text'] for comment in comments])

        ans = [(str(v[0]), len(v[1])) for v in fs]
        tansneg = {}

        for i, (date, count) in enumerate(ans):
            if i == 0 or i == len(ans)-1:
                tansneg[date] = count
                continue

            if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
                continue

            tansneg[date] = count

    df = DataFrame(data={'date': [comment['date'] for comment in comments if comment['opinion']=='Neutro'], 'id': [
                   comment['_id'] for comment in comments if comment['opinion']=='Neutro']})
    if df.empty:
        tansneu = {}
    else:
        fs = df.groupby(pd.Grouper(key='date', freq='3600S'))

        # opinion = extract_opinion([comment['text'] for comment in comments])

        ans = [(str(v[0]), len(v[1])) for v in fs]
        tansneu = {}

        for i, (date, count) in enumerate(ans):
            if i == 0 or i == len(ans)-1:
                tansneu[date] = count
                continue

            if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
                continue

            tansneu[date] = count

    df = DataFrame(data={'date': [comment['date'] for comment in comments if comment['opinion']=='Objetivo'], 'id': [
                   comment['_id'] for comment in comments if comment['opinion']=='Objetivo']})
    if df.empty:
        tansobj = {}
    else:
        fs = df.groupby(pd.Grouper(key='date', freq='3600S'))

        # opinion = extract_opinion([comment['text'] for comment in comments])

        ans = [(str(v[0]), len(v[1])) for v in fs]
        tansobj = {}

        for i, (date, count) in enumerate(ans):
            if i == 0 or i == len(ans)-1:
                tansobj[date] = count
                continue

            if ans[i-1][1] == 0 and ans[i+1][1] == 0 and ans[i][1] == 0:
                continue

            tansobj[date] = count
    res = [
            {'name': 'Negativo', 'data': tansneg},
            {'name': 'Neutro', 'data': tansneu},
            {'name': 'Objetivo', 'data': tansobj},
            {'name': 'Positivo', 'data': tanspos},
            {'name': 'Total', 'data': tans}
        ]
    return jsonify(res)


@api.route('/comments/opinion/<ObjectId:id>')
def comments_opinion(id):
    upt = Manager.get_last_update(ObjectId(id))
    ops = Manager.get_ops(ObjectId(id))
    updateb = False
    inserteb = False
    if not(ops is None):
        if ops['last_update']==upt:
            return jsonify(ops['opinion'])
        else:
            updateb = True
    else:
        inserteb = True

    opinion = list(map(lambda x: x['opinion'], Manager.interval_comments(ObjectId(id), datetime.utcnow())))
    if len(opinion)==0:
        return  jsonify({
                    'Positivo': 0,
                    'Neutro': 0,
                    'Negativo': 0,
                    'Objetivo': 0
                })
    #opinion = extract_opinion([comment['text'] for comment in comments])

    counter = Counter(opinion)
    ress = {
       'Positivo': counter['Positivo'],
       'Neutro': counter['Neutro'],
       'Negativo': counter['Negativo'],
       'Objetivo': counter['Objetivo']
    }
    if updateb:
        Manager.update_ops(ObjectId(id), ress, upt)
    elif inserteb:
        Manager.inser_ops(ObjectId(id), ress, upt)

    return jsonify(ress)


@api.route('/comments/entities/<ObjectId:id>')
def entities(id):
    upt = Manager.get_last_update(ObjectId(id))
    ents = Manager.get_ents(ObjectId(id))
    updateb = False
    inserteb = False
    if not(ents is None):
        if ents['last_update']==upt:
            return jsonify({'entities': ents['entities'][:ENTITIES_NUMBER]})
        else:
            updateb = True
    else:
        inserteb = True
    commentss = list(Manager.interval_comments(ObjectId(id), datetime.utcnow()))
    comments = list(map(lambda x: x['text'],commentss))
    if len(comments)==0:
        return jsonify({'entities':[]})
    ents = pipe_ents_detect(comments)
    entss = set()
    for i in ents:
        i = i.strip()
        if i and len(i)>=2 and not(i.lower() in stopwordsd) and re.match('[a-zA-Z]',i):
            entss.update(i)
    opinion = list(map(lambda x: x['opinion'], commentss))
    ress = [{'name': i,
             'count':{ "total": 0,
                    'Positivo': 0,
                    'Neutro': 0,
                    'Negativo': 0,
                    'Objetivo': 0}} for i in entss]
    for n,i in enumerate(comments):
        #i=Counter(i.split(' '))
        for j in ress:
            if j['name'] in i:
                j['count']['total']+=1
                j['count'][opinion[n]]+=1
    ress = list(sorted(ress,key = lambda x:x['count']['total'],reverse=True))
    if updateb:
        Manager.update_ents(ObjectId(id), ress, upt)
    elif inserteb:
        Manager.inser_ents(ObjectId(id), ress, upt)
    print(ress[:ENTITIES_NUMBER])
    return jsonify({'entities':ress[:ENTITIES_NUMBER]})

@api.route('/comments/wrodcloud/<ObjectId:id>')
def comments_wc(id):
    upt = Manager.get_last_update(ObjectId(id))
    wc = Manager.get_wc(ObjectId(id))
    updateb = False
    inserteb = False
    #if not(wc is None):
    #    if wc['last_update']==upt:
    #        return jsonify({'words':wc['words'][:WRODS_NUMBER]})
    #    else:
    #        updateb = True
    #else:
    #    inserteb = True

    coms = list(map(lambda x: (x['text'],x['opinion']), Manager.interval_comments(ObjectId(id), datetime.utcnow())))
    if len(coms)==0:
        return  jsonify({'words':[]})
    words = Counter()
    wordspol = {}
    for c, op in coms:
        for j in c.split(' '):
            if not(j.lower() in stopwordsd):
                words[j]+=1
                if j in wordspol:
                    wordspol[j][op]+=1
                    wordspol[j]['total']+=1
                else:
                    wordspol[j]={ "total": 0,
                        'Positivo': 0,
                        'Neutro': 0,
                        'Negativo': 0,
                        'Objetivo': 0}
                    wordspol[j][op]+=1
                    wordspol[j]['total']+=1
    words = [{"name": i,"value":j,'wdata':wordspol[i]} for i,j in sorted(words.items(),key=lambda x:x[1],reverse=True)]
    if updateb:
        Manager.update_wc(ObjectId(id), words, upt)
    elif inserteb:
        Manager.inser_wc(ObjectId(id), words, upt)

    return  jsonify({'words':words[:WRODS_NUMBER]})
