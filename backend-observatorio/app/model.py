from . import mongo
from typing import List, Tuple
from bson.objectid import ObjectId
from bson.code import Code
from bson.son import SON
from datetime import datetime
import pymongo


class Manager:
    mongo = mongo
    db = mongo.db
    articles = mongo.db["Articles"]
    comments = mongo.db["Comments"]
    entities = mongo.db["Entities"]
    opinions = mongo.db["Opinions"]

    @staticmethod
    def update_last_update(Id: ObjectId):
        Manager.articles.update_one(
            {'_id': Id}, {"$set": {"last_update": datetime.utcnow()}}, upsert=False)

    def get_last_update(Id: ObjectId):
        r = Manager.articles.find_one({'_id': Id})
        if not (r is None):
            return r['last_update']
        return None

    @staticmethod
    def new_entry(article: dict, comments_l: List[dict])->ObjectId:
        Id = Manager.insert_art(article)
        for i in comments_l:
            i['super'] = Id
            if '_id' in i:
                i.pop('_id')
            print(i)
            Manager.comments.insert_one(i)
        return Id

    @staticmethod
    def inser_ents(Id: ObjectId, ents_l: List[dict], upadtet):
        obj = {'entities': ents_l, 'super': Id, 'last_update': upadtet}
        Manager.entities.insert_one(obj)

    @staticmethod
    def get_ents(Id: ObjectId):
        return Manager.entities.find_one({'super': Id})

    @staticmethod
    def update_ents(Id: ObjectId, ents_l: List[dict], updatet):
        Manager.entities.update_one(
            {'super': Id}, {"$set": {"last_update": updatet, "entities": ents_l}}, upsert=False)

    @staticmethod
    def inser_ops(Id: ObjectId, op: dict, upadtet):
        obj = {'opinion': op, 'super': Id, 'last_update': upadtet}
        Manager.opinions.insert_one(obj)

    @staticmethod
    def get_ops(Id: ObjectId):
        return Manager.opinions.find_one({'super': Id})

    @staticmethod
    def update_ops(Id: ObjectId, op: dict, updatet):
        Manager.opinions.update_one(
            {'super': Id}, {"$set": {"last_update": updatet, "opinion": op}}, upsert=False)

    @staticmethod
    def get_article(Id: ObjectId)->dict:
        return Manager.articles.find_one_or_404({'_id': Id})

    @staticmethod
    def insert_art(article: dict)->ObjectId:
        Id = Manager.articles.insert_one(article).inserted_id
        return Id

    @staticmethod
    def search_url(url: str):
        a = Manager.articles.find_one({'url': url})
        if a:
            return a['_id']
        else:
            return None

    @staticmethod
    def add_comments(Id: ObjectId, comments_l: List[dict]):
        for i in comments_l:
            if Manager.comments.find(i):
                pass
            else:
                i['super'] = Id
                Manager.comments.insert_one(i)
        #article = Manager.articles.find_one_or_404({'_id': Id})
        #actualiza la fecha de upadte del articulo
        #article['update_time'] = datetime.now()

    @staticmethod
    def interval_comments(Id: ObjectId, right: datetime)->List[dict]:
        return Manager.comments.find({'super': Id, 'date': {'$lt': right}})
        # return Manager.comments.find({'_id': Id, 'date': {'$lt': right}})


class Articles():
    __slots__ = ('id', 'article')
    arts_per_page = 12

    def __init__(self, id):
        if isinstance(id, str):
            id = ObjectId(id)
        self.article = mongo.db.Articles.find_one_or_404({'_id': id})
        self.id = id

    @staticmethod
    def count_articles():
        return mongo.db.Articles.count()

    @staticmethod
    def topten_by_comments():

        pipeline = [
            {
                u"$group": {
                    u"_id": {
                        u"super": u"$super"
                    },
                    u"count": {
                        u"$sum": 1
                    }
                }
            },
            {
                u"$project": {
                    u"_id": 0,
                    u"count": u"$count",
                    u"super": u"$_id.super"
                }
            },
            {
                u"$sort": SON([(u"count", -1)])
            },
            {
                u"$limit": 10
            }
        ]

        articles = mongo.db.Comments.aggregate(
            pipeline,
        )

        ans = []
        for id in articles:
            article = mongo.db.Articles.find_one({'_id': id['super']})
            ans.append({'title': article['title'], 'id': str(
                id['super']), 'comments': id['count']})

        return ans

    @staticmethod
    def topten():

        articles = mongo.db.Articles.find({}).sort(
            [('last_update', pymongo.DESCENDING)]).limit(10)

        ans = []

        for article in articles:
            comments = mongo.db.Comments.find(
                {"super": article['_id']}).count()
            ans.append({
                'title': article['title'],
                'id': str(article['_id']),
                'comments': comments,
                'last_update': article['last_update'],
                'media': article['media'],
                'img': article['img'],
                "pub_date": article['pub_date'],
                'url': article['url'],

            })

        return ans

    @staticmethod
    def top_page(page):

        articles = mongo.db.Articles.find({}).sort(
            [('last_update', pymongo.DESCENDING)]).skip((page-1)*Articles.arts_per_page).limit(Articles.arts_per_page)

        ans = []

        for article in articles:
            comments = mongo.db.Comments.find(
                {"super": article['_id']}).count()
            ans.append({
                'title': article['title'],
                'id': str(article['_id']),
                'comments': comments,
                'last_update': article['last_update'],
                'media': article['media'],
                'img': article['img'],
                "pub_date": article['pub_date'],
                'url': article['url'],

            })

        return ans

    @staticmethod
    def top_page_filter(page, filt):

        articles = mongo.db.Articles.find({'title': {'$regex': filt, '$options': "i"}})
        nn = articles.count()
        articles = articles.sort(
            [('last_update', pymongo.DESCENDING)]).skip((page-1)*Articles.arts_per_page).limit(Articles.arts_per_page)

        ans = []

        for article in articles:
            comments = mongo.db.Comments.find(
                {"super": article['_id']}).count()
            ans.append({
                'title': article['title'],
                'id': str(article['_id']),
                'comments': comments,
                'last_update': article['last_update'],
                'media': article['media'],
                'img': article['img'],
                "pub_date": article['pub_date'],
                'url': article['url'],

            })
        return ans, nn

    @property
    def count_comments(self):
        return mongo.db.Comments.find({'super': self.id}).count()

    def to_article(self):
        return {
            'title': self.article['title'],
            'author': self.article['author'],
            'url': self.article['url'],
            'img': self.article['img'],
            'last_update': self.article['last_update'],
            'comments': self.count_comments,
            'id': str(self.id),
            "pub_date": self.article['pub_date'],
            'media': self.article['media']
        }
