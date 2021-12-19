import json
import logging
import sys
from auto_scrape.config import load_config
import auto_scrape.scraper as scraper
import auto_scrape.sentiment as sentiment


if len(sys.argv) < 2:
    print("Config file required as argument!")

config_path = sys.argv[1]


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

config = load_config(config_path)

logging.debug('Running with config file: %s', config_path)
logging.debug('loaded config: %s', config)

reviews = scraper.scrape(config)

classified_reviews = sentiment.get_review_sentement(reviews)

for x in range(1, 4):
    review = classified_reviews[x]
    print(f"{x}. \nscore: {review[1]} \ntitle: {review[0]['title']} \nbody: {review[0]['body']}\n")
