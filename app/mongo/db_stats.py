"""module returns statistic information from the import mongo database"""
import pymongo
from app.mongo import mongo


def last(item_limit):
    recent_items = mongo.shownotes_coll.find(
        {"title": {"$exists": True}}).sort(
        "created", pymongo.DESCENDING).limit(item_limit)
    return recent_items
