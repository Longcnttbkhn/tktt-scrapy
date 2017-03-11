# -*- coding: utf-8 -*-
import scrapy


class StartSpider(scrapy.Spider):
    name = "start"
    allowed_domains = ["yahoo.com/news"]
    start_urls = ['http://yahoo.com/news/']

    def parse(self, response):
        allLink = response.css('a[href^="/news/"]')
        allLink = allLink.css(':not([href*="tsrc=jtc_news_index"])::attr(href)').extract()
        allLink = set(allLink)
        yield {
        	'urls': allLink
        }