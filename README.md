# scraper
Web Scraper used to scrape Amazon Product Pages

Author: Julius Remigio

# Required Libraries
- lxml
- scrapy

## Middlewares used:
- https://github.com/alecxe/scrapy-fake-useragent
- https://github.com/aivarsk/scrapy-proxies

## Proxies
The proxies in proxy.txt was created using free public proxies that were available at the time of scraping. It should be updated regularly with working proxies to increase rate of success.

## Starting a scaping session:
Sessions are started using scrapy CLI utility.
Custom parameters are passed using the `-a` parameter. 
Custom Parameters:
- file - csv file with column header 'asin' (list of amazon products to scrape)
- html - folder to store html of scraped products
Example:
```bash
scrapy crawl product -a html=./../../html -a file=./../reviews_Women.csv.gz -o ./../reviews_Women.jl --logfile ./../reviews_Women.csv.log
```

## Settings.py
Used to changing scraping behavior such as retries and middleware configuration

## Spiders
spider directory contains all spider classes. Currently there is only a products spider for scraping amazon product pages.

