"""
This file contains fixtures and other functions used across multiple tests
"""
from app import mongo

import pytest


@pytest.fixture
def content():
    return '<html><head><title>Test</title></head></html>'

class GetResult(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.content = '<html><head><title>Test</title></head></html>'

class GetResultNoTitle(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.content = '<html><head></head></html>'

class GetNotFound(object):
    def __init__(self, url):
        self.status_code = 404

def mock_get(url):
    return GetResult(url)

@pytest.fixture(autouse=True)
def kill_cache(monkeypatch):
    """Make the caching function always return no matches when testing"""
    monkeypatch.setattr(mongo, "retrieve_from_cache", lambda x: None)

def mock_not_found(url):
    return GetNotFound(url)

def mock_requests_connection_error(url):
    raise requests.exceptions.ConnectionError

def mock_get_without_title(url):
    return GetResultNoTitle(url)

