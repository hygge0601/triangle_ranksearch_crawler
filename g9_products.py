#-*- coding: utf-8 -*-
import scrapy
from rankproducts.items import RankproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class RankProducts(scrapy.Spider):
	name = 'rankG9'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('g9.txt', 'r')
		while True:
			g9_url = f.readline()
			if not g9_url: break
			yield scrapy.Request(g9_url, self.parse_g9)
		f.close()

	def parse_g9(self, response):
		self.browser.get(response.url)
		time.sleep(4)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="container"]/div[1]/div[3]/a/text()').extract()
		if not category: selector.xpath('//*[@id="container"]/div[1]/div[2]/a/text()').extract()
		if category: category = category[0].strip()
		print category
		f = open('/Users/minheo/PRG/searchproducts/searchproducts/spiders/search_g9.txt', 'a')
		for sel in selector.xpath('//*[@id="categoryDealsItemList"]/div/li'):
			item = RankproductsItem()
			title = sel.xpath('a/span[2]/text()').extract()
			url = sel.xpath('a/@href').extract()
			img = sel.xpath('a/span[1]/img/@data-original').extract()
			count = sel.xpath('div/span/strong/text()').extract()
			if (category) and (title) and (url) and (img) and (count):
				title = title[1].strip()
				url = 'www.g9.co.kr' + url[0]
				f.write(url + '\n')
				img = img[0]
				count = count[0]
				site = 'g9'
				print title
				print url
				print img
				print count
				item['category'] = category
				item['title'] = title
				item['url'] = url
				item['img'] = img
				item['count'] = int(count)
				item['site'] = site
				yield item
		f.close()
