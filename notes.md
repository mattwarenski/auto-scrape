https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page2/?filter=#link



1. Use beautiful soup to scrape a page
* use the css selector to configure a review and stars 
* how is pagination going to work? 
  * next page selector?
1. Get 5 pages worth of reviews and stars 
2. Filter reviews that are under minimum star threshold 
3. Filter out reviews that are under the minimum word threshold
4. Calculate scores of remaining reviews 
5. Print out the n highest 


TODO: 
* [ ] setup vim python
* [ ] setup vim tests and runner
* [ ] setup vim completion 
* [ ] setup vim linting
* [ ] create requirements.txt
* [ ] create README.md


Classes: 

* main.py
  * reads config.py
  * calls scraper 
  * calls analyzer 
  * prints output 
* review.py 
* scraper.py
  * scrape(config)
* sentimentanalysis.py
  * analyze_by_positive_sentiment(config, reviews) -> sorted list(tup(score, review)) 
