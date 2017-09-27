#-*- coding: utf-8 -*-
import scrapy
from rankproducts.items import RankproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class RankProducts(scrapy.Spider):
	name = 'rankTimon'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('timon.txt', 'r')
		while True:
			timon_url = f.readline()
			if not timon_url: break
			yield scrapy.Request(timon_url, self.parse_timon)
		f.close()

	def parse_timon(self, response):
		self.browser.get(response.url)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="container"]/div[1]/div/div/div[4]/a/text()').extract()
		if category: category = category[0].strip()
		f = open('/Users/minheo/PRG/searchproducts/searchproducts/spiders/search_timon.txt', 'a')
		for sel in selector.xpath('//*[@id="_dealListContainer"]/li'):
			item = RankproductsItem()
			title = sel.xpath('a/div/div[2]/p[2]/text()').extract()
			url = sel.xpath('a/@href').extract()
			img = sel.xpath('a/div/div[1]/div[1]/img/@src').extract()
			count = sel.xpath('a/div/div[2]/span/i/text()').extract()
			site = 'ticketmonster'
			if (category) and (title) and (url) and (img) and (count) and (40 <= len(url[0]) <= 50):
				title = title[0].strip()
				url = url[0]
				img = img[0]
				count = count[0]
				print category
				print title
				print url
				f.write(url + '\n')
				print img
				print count
				item['category'] = category
				item['title'] = title
				item['url'] = url
				item['img'] = img
				item['count'] = int(count.replace(",", ""))
				item['site'] = site
				yield item
		f.close()
		
