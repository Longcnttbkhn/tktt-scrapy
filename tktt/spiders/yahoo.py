# -*- coding: utf-8 -*-
import scrapy
import json

class YahooSpider(scrapy.Spider):
    name = "yahoo"

    def start_requests(self):
    	with open('noturl.json') as datafile:
            self.noturl = set(json.load(datafile))

        with open('currenturl.json') as datafile:
            self.currenturl = set(json.load(datafile))
    	url = 'https://www.yahoo.com' + self.noturl.pop()
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
    	title = response.css('title::text').extract_first()
        description = response.css('meta[name="description"]::attr(content)').extract_first()
        url = response.request.url
        article = response.css('article')
        content = article.css('*::text').extract()
        content = ' '.join(content)

        yield {
            'title': title,
            'description': description,
            'url': url,
            'content': content
        }
        
        allLink = response.css('a[href^="/news/"]')
        allLink = allLink.css(':not([href*="tsrc=jtc_news_index"])::attr(href)').extract()
        allLink = list(set(allLink))
        
        for link in allLink:
            if link in self.currenturl:
            	pass
            else:
            	self.currenturl.add(link)
            	self.noturl.add(link)
        url = 'https://www.yahoo.com' + self.noturl.pop()
        yield scrapy.Request(url, self.parse)

    def closed(self, reason):
		with open('noturl.json', 'w') as outfile:
			json.dump(list(self.noturl), outfile)

		with open('currenturl.json', 'w') as outfile:
			json.dump(list(self.currenturl), outfile)