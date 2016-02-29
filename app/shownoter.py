""" The shownoter module contains the core Shownoter functionality """

import re
import requests

from app import mongo
from app import url_parser

from datetime import datetime
from bs4 import BeautifulSoup
from markdown import markdown


def format_links_as_hash(source):
    urls = url_parser.link_detect(source)
    links = []

    for url in urls:
        valid_link = True

        if url_parser.image_detect(url):
            link = Image(url)

        else:
            link = Link()

            try:
                link.collect_data(url)
            except ValueError:
                valid_link = False
                continue

        if valid_link:
            if not link.title:
                link.title = link.url

            entry = {
                'url':link.url,
                'title':link.title,
                'markdown':link.markdown}
            links.append(entry)

    return links

def format_links_as_markdown(source):
    """ Wraps the shownoter functionality in a single function call """
    urls = link_detect(source)
    links = []

    for url in urls:
        if image_detect(url):
            link = Image(url)
        else:
            link = Link()
            link.collect_data(url)

        links.append(link.markdown)

    output = links_to_string(links)
    return output.strip()

def link_detect(site):
    """ Returns a list of urls from a string"""
    re_link =  re.compile(r'\b\S+\.[a-zA-Z]{2,}\S*', re.M)
    links = []

    for link in re.findall(re_link, site):

        if link not in links:
            links.append(link)

    return links

def get(link):
    """ A wrapper around requests.get to allow for easy mocking """
    return requests.get(link, timeout=1.5, allow_redirects=False)

def parse_title(content, default_title=""):
    """Parses the title of a site from it's content"""
    if content == None:
        return default_title

    soup =  BeautifulSoup(content, 'html.parser')
    if soup == None or soup.title == None:
        return default_title

    title = soup.title.text
    return title.strip()

def link_markdown(title, url):
    """Formats a generic link to a markdown list item link"""
    return '* [{}]({})'.format(title, url)

def image_markdown(title, url):
    """Formats a link as an image"""
    return '* ![{}]({})'.format(title, url)

def request_content(site):
    """ Returns content or raises ValueError """
    success = True

    try:
        request = get(site)
    except:
        # TODO insert some logging here requests.ConnectionError (or other) being trapped.
        raise ValueError("Url not found")

    if request.status_code == 200:
        return request
    else:
        # TODO insert some logging here
        pass

    raise ValueError("Url not found")

def possible_urls(url):
    """ Generator that returns possible variations of a given url """
    if re.search(r'^\w{3,5}://', url):
        yield url
    else:
        prefixes = ['http://', 'https://', 'http://www.', 'https://www.']

        for prefix in prefixes:
            yield prefix+url

def get_domain(url):
    """returns the domain of the url"""
    pattern = re.compile(r'\w{3,5}:\/\/(www\.)?|www\.')
    new_url = re.sub(pattern,'', url)
    return new_url

def valid_link(site):
    """Returns the content of a website from a url

    If the first request fails it will attempt variations

    If all variations fail a ValueError is raised"""

    for url in possible_urls(site):
        try:
            return request_content(url)
        except ValueError:
            continue

    raise ValueError("No valid link permutation found")

class Link():
    def collect_data(self, site):
        """ Collects the various information about the link """

        cached_url = mongo.retrieve_from_cache(site)

        if cached_url:
            self.url = cached_url['url']
            self.title = cached_url['title']

        else:
            #TODO REMOVE SELF SITE AND MAKE JUST SITE!!!
            self.site = valid_link(site)
            self.url =  self.site.url
            self.title = parse_title(self.site.content)
            mongo.cache_url(self.url, self.title)

        self.markdown = link_markdown(self.title, self.url)

class Image(Link):
    """Images are like links except they ignore connectivity tests."""

    title = ''

    def __init__(self, site):
        self.url = site
        self.markdown = image_markdown(self.title, self.url)


def links_to_string(links):
    """This function takes a list of objects and returns it as a string"""

    links_string = ''
    for link in links:
        links_string += link + '\n'
    return links_string
