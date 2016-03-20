import re
from app.mongo import mongo


def remove_url_scheme(url):
    """removes the url scheme and/or 'www' from the url and
        returns the domain and extension"""

    pattern = re.compile(r'\w{3,5}:\/\/(www\.)?|www\.')
    new_url = re.sub(pattern, '', url)
    return new_url


def retrieve_from_cache_db(url):
    """checks links_coll for entries returns url_entry in True or False"""
    base_url = remove_url_scheme(url)
    db_entry = mongo.retrieve_from_db(value=base_url,
                                      collection=mongo.links_coll,
                                      field="base_url")

    if db_entry is not None:
        return db_entry

    else:
        return mongo.retrieve_from_db(value=base_url+'/',
                                      collection=links_coll,
                                      field="base_url")


def insert_to_cache_db(db_entry):
    """wrapper that adds entry to link_cache database"""
    base_url = remove_url_scheme(db_entry['url'])
    db_entry['base_url'] = base_url
    return mongo.create_entry(value=db_entry, collection=mongo.links_coll)
