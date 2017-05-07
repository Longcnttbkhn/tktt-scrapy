# -*- coding: utf-8 -*-
import scrapy
import json

class HuffingtonpostSpider(scrapy.Spider):
    name = "HuffingtonPost"

    def start_requests(self):
    	with open('HuffingtonPost/noturl.json') as datafile:
            self.noturl = set(json.load(datafile))

        with open('HuffingtonPost/currenturl.json') as datafile:
            self.currenturl = set(json.load(datafile))

    	url = self.noturl.pop()
        yield scrapy.Request(url, self.parse, dont_filter=True, errback=self.error_handle)

    def parse(self, response):
        url = response.request.url
        print url
        if url.startswith('http://www.huffingtonpost.com/entry/'):
            if '/entry/' in url:
                print "crawl" + url
                title = response.css('title::text').extract_first()
                description = response.css('meta[name="description"]::attr(content)').extract_first()
                article = response.css('div.entry__text')
                content = article.css('*::text').extract()
                content = ' '.join(content)
                yield {
                    'title': title,
                    'description': description,
                    'url': url,
                    'content': content
                }

            allLink = response.css('a[href^="http://www.huffingtonpost.com/entry/"]::attr(href)').extract()
            # allLink = allLink.css(':not([href$=".xml"])::attr(href)').extract()
            allLink = list(set(allLink))
            
            for link in allLink:
                if link in self.currenturl:
                	pass
                else:
                	self.currenturl.add(link)
                	self.noturl.add(link)

        url = self.noturl.pop()
        yield scrapy.Request(url, self.parse, dont_filter=True, errback=self.error_handle)


    def error_handle(self, failure):
        url = self.noturl.pop()
        yield scrapy.Request(url, self.parse, dont_filter=True, errback=self.error_handle)

    def closed(self, reason):
		with open('HuffingtonPost/noturl.json', 'w') as outfile:
			json.dump(list(self.noturl), outfile)

		with open('HuffingtonPost/currenturl.json', 'w') as outfile:
			json.dump(list(self.currenturl), outfile)
