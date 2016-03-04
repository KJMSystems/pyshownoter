from app import shownoter
from app import cache_db
from app import url_parser
import pytest
import requests


from test_helpers import *

# Test link detection

def test_detect_links_finds_one_link_text():
    sample_text = '''This is a test
    to see if our regex
    will find link.com
    and return it'''
    assert shownoter.detect_links(sample_text) == ['link.com']

def test_detect_links_finds_multiple_links():
    sample_text = '''This is a test
    to see if our regex
    will find link.com
    and link.net
    and foo.bar
    and returns them all'''
    assert shownoter.detect_links(sample_text) == ['link.com', 'link.net', 'foo.bar']

def test_detect_linkss_will_only_return_one_of_duplicates():
    sample_text = '''This is a test
    to see if our detect_links
    will find link.com
    link.com
    link.com
    but only show one link.com'''
    assert shownoter.detect_links(sample_text) == ['link.com']
# Test link object

def test_title_is_parsed(content):
    title = shownoter.fetch_site_title(content)
    assert "Test" == title

def test_title_is_blank_if_no_title_in_content():
    title = shownoter.fetch_site_title("<html><head><title></title></head></html>")
    assert "" == title

def test_title_is_blank_if_title_tag_missing():
    title = shownoter.fetch_site_title("<html><head></head></html>")
    assert "" == title

def test_title_is_blank_if_content_missing():
    title = shownoter.fetch_site_title("")
    assert "" == title

def test_title_is_blank_if_content_none():
    title = shownoter.fetch_site_title(None)
    assert "" == title

def test_title_is_defaulted_if_specified():
    title = shownoter.fetch_site_title(None, "Ewerer")
    assert "Ewerer" == title

# Test valid_link

def test_valid_link_inserts_prefix_if_none(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get)

    link = shownoter.valid_link('link.com')
    assert 'http://link.com' == link.url

def test_valid_link_does_nothing_if_prefix_exists(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get)

    link = shownoter.valid_link('http://link.com')
    assert 'http://link.com' == link.url

def test_valid_link_throws_value_error_if_none_found(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_not_found)

    try:
        shownoter.valid_link('http://link.com')
    except ValueError as e:
        assert "No valid link permutation found" == e.args[0]
    else:
        assert False, "Expected Value Error"

def test_valid_link_throws_value_error_if_none_found_if_not_prefixed(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_not_found)

    try:
        shownoter.valid_link('link.com')
    except ValueError as e:
        assert "No valid link permutation found" == e.args[0]
    else:
        assert False, "Expected Value Error"

# Test requesting content
def test_request_content_returns_content_on_200(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get)

    link = shownoter.request_content('link.com')
    assert 200 == link.status_code

def test_request_content_raises_value_error_on_404(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_not_found)

    try:
        link = shownoter.request_content('link.com')
    except ValueError as e:
        assert "Url not found" == e.args[0]
    else:
        assert False, "Expected Value Error"

def test_request_content_raises_value_error_on_404(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_requests_connection_error)

    try:
        link = shownoter.request_content('link.com')
    except ValueError as e:
        assert "Url not found" == e.args[0]
    else:
        assert False, "Expected Value Error"

# Test possible urls
def test_possible_urls_returns_one_option_when_prefixed_with_http():
    options = list(shownoter.possible_urls("http://example.com"))

    assert 1 == len(options)
    assert options[0] == "http://example.com"

def test_possible_urls_returns_one_option_when_prefixed_with_https():
    options = list(shownoter.possible_urls("https://example.com"))

    assert 1 == len(options)
    assert options[0] == "https://example.com"

def test_possible_urls_returns_multiple_options_when_not_prefixed():
    options = list(shownoter.possible_urls("example.com"))

    assert 1 < len(options)

def test_possible_urls_adds_http_prefix():
    options = list(shownoter.possible_urls("example.com"))

    assert "http://example.com" in options

def test_possible_urls_adds_http_www__prefix():
    options = list(shownoter.possible_urls("example.com"))

    assert "http://www.example.com" in options

def test_possible_urls_adds_https_prefix():
    options = list(shownoter.possible_urls("example.com"))

    assert "https://example.com" in options

def test_possible_urls_adds_https_www_prefix():
    options = list(shownoter.possible_urls("example.com"))

    assert "https://www.example.com" in options

# Test image detection

def test_image_detect_detects_png():
    link = 'link.png'
    assert url_parser.image_detect(link)

def test_image_detect_detects_jpg():
    link = 'link.jpg'
    assert url_parser.image_detect(link)

def test_image_detect_detects_gif():
    link = 'link.gif'
    assert url_parser.image_detect(link)

def test_image_detect_does_not_detect_outside_other_links():
    link = 'link.foo'
    assert not url_parser.image_detect(link)

def test_image_detect_does_not_throw_attribute_error_when_no_extension():
    link = 'https://gist.github.com/anonymous/7e5fa94f6e946551b70a'
    assert not url_parser.image_detect(link)

# Test Markdown generation

def test_link_markdown():
    link = 'link.com'
    title = 'Test'
    assert '[Test](link.com)' in shownoter.format_link_as_markdown(title, link, False)

def test_shownoter_returns_a_list_of_three_element_hashes(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get)

    text = "link.com"
    results = shownoter.shownoter(text)
    assert 1 == len(results)
    assert "* [Test](http://link.com)" == results[0]["markdown"]
    assert "Test" == results[0]["title"]
    assert "link.com" == results[0]["url"]

def test_shownoter_excludes_invalid_links(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_not_found)

    text = "link.com"
    results = shownoter.shownoter(text)
    assert 0 == len(results)

def test_format_links_with_default_title_if_title_not_found(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get_without_title)

    text = "link.com"
    results = shownoter.shownoter(text)
    assert 1 == len(results)
    assert "link.com" == results[0]["title"]

def test_maintains_case(monkeypatch):
    monkeypatch.setattr(shownoter, 'request_get', mock_get)

    text = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    results = shownoter.shownoter(text)
    assert 1 == len(results)
    assert "* [Test](https://www.youtube.com/watch?v=dQw4w9WgXcQ)" == results[0]["markdown"]
    assert "Test" == results[0]["title"]
    assert "https://www.youtube.com/watch?v=dQw4w9WgXcQ" == results[0]["url"]

def test_remove_url_scheme():
    urls = ['http://foo.com', 'http://www.foo.com', 'https://foo.com', 'ftp://foo.com', 'www.foo.com']
    for url in urls:
        assert cache_db.remove_url_scheme(url) == 'foo.com'

