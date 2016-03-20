import pymongo
import re
from bson.objectid import ObjectId

conn = pymongo.MongoClient('localhost', 27017)
db = conn.shownoter
shownotes_coll = db.shownotes
links_coll = db.link_cache


def create_entry(value, collection):
    """Adds new link to database"""
    result = collection.insert_one(value)
    return result.inserted_id


def append_to_entry(id, entry):
    """adds/edits fields to entry in database. """
    result = shownotes_coll.update_one(
        {'_id': ObjectId(id)},
        {'$set': entry}, upsert=True)
    return result


def retrieve_from_db(value, collection, field="_id"):
    """fetches results in database"""
    if field == "_id":  # checks for id to return ObjectId
        value = ObjectId(value)

    result = collection.find_one({field: value})
    return result


def cache_url(url, title):
    """add url to cache"""
    domain = get_domain(url)
    links_coll.insert_one({'url': url, 'domain': domain, 'title': title})


def get_domain(url):
    """returns the domain of the url"""
    if url[-1] == '/':
        url = url[:-1]
    pattern = re.compile(r'\w{3,5}:\/\/(www\.)?|www\.')
    new_url = re.sub(pattern, '', url)
    return new_url


def count_entries(collection):
    count = collection.count()
    return count
