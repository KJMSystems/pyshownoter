"""The views_helper.py hosts any functions that assist the views.py module"""
from app import shownoter
from app.validations import url_parser
from app.validations import custom_title
from app.mongo import cache_db


def shownoter_wrapper(content, custom_title_enabled):
    """wrapper around shownoter functionality. This creates a dictionary
    values of the Link/Image class"""
    links = []
    for line in content.split('\n'):
        if custom_title_enabled and custom_title.detect_link(line):
            line_link = custom_title.detect_link(line)

            if line_link:
                url = line_link['url']
                line_link['url'] = shownoter.valid_link(url).url

                if line_link not in links:
                    line_link['markdown'] = shownoter.format_link_as_markdown(
                        title=line_link['title'],
                        url=line_link['url'],
                        is_image=False)
                    links.append(line_link)

        elif url_parser.get_potential_link(line):
            potential_links = url_parser.get_potential_link(content)

            for url in potential_links:
                cached_link = cache_db.retrieve_from_cache_db(url)
                if cached_link:
                    links.append(cached_link)

                elif shownoter.check_link_validity(url):
                    link = shownoter.prep_link(url)

                    if link:
                        cache_db.insert_to_cache_db(link)
                        links.append(link)

                else:
                    continue

        else:
            continue

    return links
