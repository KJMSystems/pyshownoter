import csv
import re

with open('app/static/tlds.txt', 'r+') as f:
    top_level_domains = f.read().splitlines()

with open('app/static/uri-schemes-1.csv', newline='', encoding='utf-8') as csvfile:
    uris = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        uris.append(row['URI Scheme'])

def link_detect(content):
    """ Returns a list of urls from a import string"""
    re_link = re.compile(r'(\b(\S+[:\.@]\/\/)*([\w\d]+[@\.][a-zA-Z]+\d*([@\/\w\.\?=]+)*))', re.M)
    links = []

    for link in re.findall(re_link, content):
        if link[0] not in links:
            links.append(link[0])
    return links

def image_detect(url):
    """Determines if the url is an image. """
    image_extension = ['.jpg', '.png', '.jpeg', '.gif']
    extension = re.search(r'\.[a-zA-Z]{2,}$', url, re.M)

    if extension == None:
        return False
    
    if extension.groups(0) in image_extension:
        return True
    
def check_tld(domain):
    """returns True if domain is listed as a top-level domain"""
    return domain.upper() in tld


