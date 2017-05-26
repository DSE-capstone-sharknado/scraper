# -*- coding: utf-8 -*-
import scrapy
import logging
from lxml import html
from exceptions import ValueError
import csv, gzip, os

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["amazon.com"]
    url = 'https://amazon.com/dp/'

    def start_requests(self):
        url = self.url
        input_file = getattr(self, 'file', None)

        print '**** {0} ****'.format(os.getcwd())

        if input_file is not None:
            html = getattr(self, 'html', None)
            skip = list()
            if html is not None:
                skip = [x[:-5] for x in os.listdir(html) if x.endswith('.html')]
                skip.extend(list(set([x.split()[7][26:-1] for x in open(input_file.replace('.gz','') + '.log') if x.find('DEBUG: Crawled (404)') > -1])))
            with gzip.open(input_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    asin = str(row['asin'])
                    p_url = url + asin
                    if asin not in skip:
                        yield scrapy.Request(p_url, self.parse, meta={'cookiejar': p_url})
                        skip.append(asin)
                    # break
                    # break
        else:
            raise ValueError("missing input argument file, ex. file='/path/file'")



    def parse(self, response):
        # path to save html responses
        html = getattr(self, 'html', None)

        # print "******* HTML PATH" + html
        yield self.parse_product(response, html if html is not None else '')


    def parse_product(self, response, htmlpath):
        def getDicFromTable(html):
            # extract only html nodes from raw html
            rows = [x for x in html if str(type(x)) == "<class 'lxml.html.HtmlElement'>"]

            # return dictionary from list of tuples of headers and data elements
            return dict(
                zip([x.text.strip() for x in rows if x.tag == 'th'], [x.text.strip() for x in rows if x.tag == 'td']))

        url = self.url
        doc = html.fromstring(response.text)

        #get asin
        asin = response.meta['redirect_urls'][0].replace(url, '')


        # XPATH_NAME = '//h1[@id="title"]//text()'
        # XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
        # XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
        # # XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
        # # XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
        # XPATH_BRAND = '//a[@id="brand"]//text()'
        # XPATH_FEATURE_BULLETS = '//div[@id="feature-bullets"]//li/span[@class="a-list-item"]/text()'
        # XPATH_PRODUCT_INFORMATION = '//table[@id="productDetails_detailBullets_sections1"]//tr/node()'
        # XPATH_PRODUCT_DESCRIPTION = '//div[@id="productDescription"]//text()'
        #
        # RAW_NAME = doc.xpath(XPATH_NAME)
        # RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
        # # RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
        # RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
        #
        # RAW_BRAND = doc.xpath(XPATH_BRAND)
        # RAW_FEATURE_BULLETS = doc.xpath(XPATH_FEATURE_BULLETS)
        # RAW_PRODUCT_INFORMATION = doc.xpath(XPATH_PRODUCT_INFORMATION)
        # RAW_PRODUCT_DESCRIPTION = doc.xpath(XPATH_PRODUCT_DESCRIPTION)
        #
        # NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        # SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
        # ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
        #
        # BRAND = ''.join(RAW_BRAND).strip()
        # FEATURE_BULLETS = [x.strip() for x in RAW_FEATURE_BULLETS if x.strip() != '']
        # PRODUCT_INFORMATION = getDicFromTable(RAW_PRODUCT_INFORMATION)
        # PRODUCT_DESCRIPTION = '\n'.join([x.strip() for x in RAW_PRODUCT_DESCRIPTION if x.strip() != ''])
        #
        # if not ORIGINAL_PRICE:
        #     ORIGINAL_PRICE = SALE_PRICE

        if len(doc.xpath("//img[contains(@src,'captcha')]")) > 0:
            self.log('====== CAPTCHA DETECTED ======', level=logging.WARNING)
            return
        else:
            # save page
            filename = os.path.join(htmlpath, asin + '.html')
            with open(filename, 'wb') as f:
                f.write(response.text.encode('utf-8')
                self.log('Saved file %s' % filename)

        # return {
        #     'asin': asin,
        #     'NAME': NAME,
        #     'SALE_PRICE': SALE_PRICE,
        #     #                     'CATEGORY':CATEGORY,
        #     'ORIGINAL_PRICE': ORIGINAL_PRICE,
        #     #                     'AVAILABILITY':AVAILABILITY,
        #     'URL': url,
        #     'BRAND': BRAND,
        #     'PRODUCT_DESCRIPTION': PRODUCT_DESCRIPTION,
        #     'FEATURE_BULLETS': FEATURE_BULLETS,
        #     'PRODUCT_INFORMATION': PRODUCT_INFORMATION
        # }