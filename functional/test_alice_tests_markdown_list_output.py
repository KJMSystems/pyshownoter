from app import shownoter
from app import mongo
import pytest


def mock_url_homepage_result(url):
    return UrlHomepageResult(url)

class UrlHomepageResult(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.content = '<html><head><title>{} Homepage</title></head></html>'.format(url)

@pytest.fixture(autouse=True)
def mock_http(monkeypatch):
    """
    This will mock all http requests and return a TestResult instance
    that will emulate the results object that will generate a title of:
    "{url} Homepage"
    """
    monkeypatch.setattr(shownoter, 'get', mock_url_homepage_result)

@pytest.fixture(autouse=True)
def kill_cache(monkeypatch):
    """Make the caching function always return no matches when testing"""
    monkeypatch.setattr(mongo, "retrieve_from_cache", lambda x: None)
    monkeypatch.setattr(mongo, "cache_url", lambda x, y: None)

def test_alice_generates_basic_shownotes():
    """
    Alice has a chat history that she wants to extract the links and images
    from.  She wants these links and images to be formatted nicely so
    that she can save them as shownotes for her podcast.
    """

    chat_history = """
    Jay: Lorem ipsum dolor oneplayerbattleship.net ipiscing elit.
    Cam: goatsvscats.io urpis elementum testingcodeforthewin.org
    Alice: Nullam http://example.com/photo.gif ngue.
    Jay: Prae http://example.com/9032dfd.png lesuada finibus.
    Dahl: Vestibulum suscipit erat quis placerat feugiat.
    Funchess: Vestibulum bettertypingwithcats.com porttitor.
    Val: Integer gotypingcatsgo.com luctus viverra ut eu orci.
    Cam: Nunc ut purus non ex https://testinggoatsforever.links/tdd/super.html
    Alice: Etiam http://www.highflyingtypingcats.com tis.
    Vivamus typingcatsinhistory.com/1800s/eduardo.html :)""".strip()

    md = ["* [http://oneplayerbattleship.net Homepage](http://oneplayerbattleship.net)",
            "* [http://goatsvscats.io Homepage](http://goatsvscats.io)",
            "* [http://testingcodeforthewin.org Homepage](http://testingcodeforthewin.org)",
            "* ![](http://example.com/photo.gif)",
            "* ![](http://example.com/9032dfd.png)",
            "* [http://bettertypingwithcats.com Homepage](http://bettertypingwithcats.com)",
            "* [http://gotypingcatsgo.com Homepage](http://gotypingcatsgo.com)",
            "* [https://testinggoatsforever.links/tdd/super.html Homepage](https://testinggoatsforever.links/tdd/super.html)",
            "* [http://www.highflyingtypingcats.com Homepage](http://www.highflyingtypingcats.com)",
            "* [http://typingcatsinhistory.com/1800s/eduardo.html Homepage](http://typingcatsinhistory.com/1800s/eduardo.html)"]

    expected_output = "\n".join(md)
    actual_output = shownoter.format_links_as_markdown(chat_history)
    assert expected_output == actual_output
