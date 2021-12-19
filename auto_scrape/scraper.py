"""
Contains all functions used to download an html page and scrape it's contents
"""
import re
import logging
import time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def download_page(page_url):
    """
    requests the resource from page_url and returns html as a string

    returns str
    """
    source = requests.get(page_url)
    return source.text

def extract_by_regex(tags, extractor_definition):
    """
    extracts values from tags using a regex
    the regex is defined in the extractor_definition. See README.md for exact structure

    returns [str]
    """
    values = []
    for html in tags:
        attr = extractor_definition['attr']
        regex = extractor_definition['regex']
        raw_value = html.get_text() if attr == 'text' else html[attr]
        matches = re.search(regex, raw_value)
        value = matches.group(0) if matches else ""
        values.append(value)
    return values

def find_in_soup(soup: BeautifulSoup, selector):
    """
    searches soup instance for all instances of selector. See README.md for selector definition.

    returns [str]
    """

    find_args = {}
    if 'attrs' in selector:
        attrs = selector['attrs'].copy()
        find_args = {'attrs': attrs}

        if 'text' in attrs:
            text_value = attrs.pop('text')
            if text_value.startswith('/') and text_value.endswith('/'):
                find_args['text'] = re.compile(text_value.strip('/'))
            else:
                find_args['text'] = text_value

    tags = soup.find_all(selector['tag'], **find_args)

    if 'value' not in selector:
        return [t.get_text() for t in tags]

    if isinstance(selector['value'], dict):
        value = selector['value']
        if 'child' in value:
            all_values = []
            {all_values.extend(find_in_soup(t, value['child'])) for t in tags}
            return all_values
        return extract_by_regex(tags, value)
    else:
        value = selector['value']
        ret_val = []
        for v in tags:
            if v.has_attr(value):
                logging.debug("Found attribute '%s' in html: %s'", value, v)
                ret_val.append(v[value])
            else:
                logging.error(f"Attribute not found. Looking for attribute: '{value}' in html: {v}" )

        return ret_val


def scrape(config):
    """
    scrapes a web page according to the past in config
    config.start_url is used to get html
    reviews are parsed and extracted using selectors in config 

    returns
    [
        {"title": str, "body": str}, ...
    ]
    """
    num_pages = config.get_int('num_pages', default=5)


    url = config.get_string('start_url')
    start_url = urlparse(url)
    reviews = []
    next_page_selector = config.get("next_link_selector")
    title_selector = config.get("title_selector")
    body_selector = config.get("body_selector")
    for page in range(1, num_pages + 1):
        if page != 1:
            pause_time = config.get_float('pause_time', default=1.0)
            time.sleep(pause_time)
        logging.info('scraping %s of %s: %s', page, num_pages, url)

        page_source = download_page(url)
        soup = BeautifulSoup(page_source)

        next_url = find_in_soup(soup, next_page_selector)
        titles = find_in_soup(soup, title_selector)
        bodies = find_in_soup(soup, body_selector)

        for itter in range(len(titles)):
            reviews.append({
                "title": titles[itter],
                "body": bodies[itter],
            })
        if not next_url:
            return reviews

        if next_url[0].startswith('/'):
            url = f"{start_url.scheme}://{start_url.netloc}{next_url[0]}"
        else:
            url = next_url[0]
    return reviews

