import unittest
from bs4 import BeautifulSoup
import auto_scrape.scraper as scraper
from unittest import mock
from auto_scrape.config import Config

class TestScraper(unittest.TestCase):

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, text):
                self.text = text

        html1 = """
        <html>
            <body>
                <div class="title">title1</div>
                <div class="body">body1</div>
                <div class="title">title2</div>
                <div class="body">body2</div>
                <a href="page2link", class="next-link">next link text</a>
            </body>
        </html>
        """

        html2 = """
        <html>
            <body>
                <div class="title">title3</div>
                <div class="body">body3</div>
                <div class="title">title4</div>
                <div class="body">body4</div>
                <a href="page3link", class="next-link">next link text</a>
            </body>
        </html>
        """

        return MockResponse(html2 if args[0] == 'page2link' else html1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_scrape(self, mock_get):
        config_json = {
            'pause_time': 0.0001,
            'start_url': 'myUrl',
            'num_pages': 2,
            'next_link_selector': {
                'tag': 'a',
                'attrs': { 
                    'class': 'next-link'
                }, 
                'value': 'href'
            }, 
            'title_selector': {
                'tag': 'div',
                'attrs': { 
                    'class': 'title'
                }
            },
            'body_selector': {
                'tag': 'div',
                'attrs': { 
                    'class': 'body'
                }
            }
        }

        config = Config(config_json)

        reviews = scraper.scrape(config)

        self.assertEqual([{
                "title": "title1",
                "body": "body1"
            }, {
                "title": "title2",
                "body": "body2"
            }, 
            {
                "title": "title3",
                "body": "body3"
            },

            {
                "title": "title4",
                "body": "body4"
            }
        ], reviews)


    def test_find_in_soup_noAttrs(self):
        html = """
        <html>
            <body>
                <span>test</span> 
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, { "tag": "span" })
        self.assertEqual(values, ["test"])

    def test_find_in_soup_search_by_text_regex(self):
        html = """
        <html>
            <body>
                <div>not my div</div>
                <div>stuff in a 123 string</div>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "div",
            "attrs": { 
                "text": "/in a [0-9]+/"
            }
        })
        self.assertEqual(values, ["stuff in a 123 string"])

    def test_find_in_soup_get_child_value(self):
        html = """
        <html>
            <body>
                <div class="test">
                    <span>test</span>
                </div>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "div",
            "value": {
                "child" : {
                    "tag": "span", 
                }
            }
        })
        self.assertEqual(values, ["test"])

    def test_find_in_soup_href(self):
        html = """
        <html>
            <body>
                <a href="testurl">test</a> 
            </body>
        </html>
        """

        soup = BeautifulSoup(html)

        values = scraper.find_in_soup(soup, {
            "tag": "a",
            "value":  "href"
        })
        self.assertEqual(values, ["testurl"])

    def test_find_in_soup_by_class(self):
        html = """
        <html>
            <body>
                <span class="testClass">test value</span>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "span", 
            "attrs":  { 
                "class": "testClass"
            }
        })
        self.assertEqual(values, ["test value"])

    def test_find_in_soup_value_regex(self):
        html = """
        <html>
            <body>
                <span>3 out of 5</span>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "span",
            "value" : {
                "attr": "text",
                "regex": "^\\s*[0-9]"
            }
        })
        self.assertEqual(values, ["3"])

    def test_find_in_soup_value_regex_and_attr(self):
        html = """
        <html>
            <body>
                <a href="sampleHref">href title</a>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "a",
            "value" : {
                "attr": "href",
                "regex": "[A-Z][a-z]{2}"
            }
        })
 
    def test_find_in_soup_value_regex_and_attr_and_text_regex(self):
        html = """
        <html>
            <body>
                <a href="sampleHref">next </a>
                <a href="sampleHref2">ext </a>
                <a href="sampleHref3"></a>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "a",
            "attrs": {
                "text": "/^next/"
            },
            "value" : {
                "attr": "href",
                "regex": "[A-Z][a-z]{2}"
            }
        })

        self.assertEqual(values, ["Hre"])

    def test_find_in_soup_value_regex_and_attr_notFound(self):
        html = """
        <html>
            <body>
                <a href="sampleHref">href title</a>
            </body>
        </html>
        """

        soup = BeautifulSoup(html)
        values = scraper.find_in_soup(soup, {
            "tag": "a",
            "value" : {
                "attr": "href",
                "regex": "[A-Z][!]"
            }
        })
        self.assertEqual(values, [''])

if __name__ == '__main__':
    unittest.main()

