import csv
import re

with open('app/static/tlds.txt', 'r+') as f:
    top_level_domains = f.read().splitlines()

with open('app/static/uri-schemes-1.csv', newline='', encoding='utf-8') as csvfile:
    uris = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        uris.append(row['URI Scheme'])

def search_for_links(content):
    """ Returns a list of urls from a import string"""
    re_link =  re.compile(r'\b\S+\.[a-zA-Z]{2,}\S*', re.M)
    links = []
    for link in re.findall(re_link, content):
        if link not in links:
            links.append(link)
            return links

def image_detect(url):
    """Determines if the url is an image. """
    image_extension = ['.jpg', '.png', '.jpeg', '.gif']
    extension = re.search(r'\.[a-zA-Z]{2,}$', url, re.M)
    print(extension) 

    if extension == None:
        return False
    
    if extension.group(0) in image_extension:
        return True
def check_tld(domain):
    """returns True if domain is listed as a top-level domain"""
    return domain.upper() in top_level_domains

