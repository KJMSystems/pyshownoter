import re


def remove_url_scheme(url):
    """removes the url scheme and/or 'www' from the url and
        returns the domain and extension"""

    pattern = re.compile(r'\w{3,5}:\/\/(www\.)?|www\.')
    new_url = re.sub(pattern,'', url)
    return new_url


