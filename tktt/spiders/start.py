# -*- coding: utf-8 -*-
import scrapy


class StartSpider(scrapy.Spider):
    name = "start"
    # start_urls = ['http://yahoo.com/news/']
    # start_urls = ['http://yahoo.com/tech/']
    start_urls = ['http://www.huffingtonpost.com/']
    def parse(self, response):
        # allLink = response.css('a[href^="https://www.yahoo.com/news/"], a[href^="/news/"]')
        # allLink = allLink.css(':not([href*="tsrc=jtc_news_index"])::attr(href)').extract()

        # allLink = response.css('a[href^="https://www.yahoo.com/tech/"], a[href^="/tech/"]')
        # allLink = allLink.css('::attr(href)').extract()
        
        allLink = response.css('a[href^="http://www.huffingtonpost.com/entry/"]::attr(href)').extract()
        # allLink = allLink.css(':not([href$=".xml"])::attr(href)')
        allLink = set(allLink)
        yield {
        	'urls': allLink
        }