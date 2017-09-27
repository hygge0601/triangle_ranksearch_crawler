#-*- coding: utf-8 -*-
import scrapy
from rankproducts.items import RankproductsItem 
import time
from selenium import webdriver
from scrapy.selector import Selector

class RankProducts(scrapy.Spider):
	name = 'rankAuction'

	def __init__(self):
		self.browser = webdriver.PhantomJS('/Users/minheo/phantomjs/bin/phantomjs')
		time.sleep(3)	

	def start_requests(self):
		f = open('auction.txt', 'r')
		while True:
			auction_url = f.readline()
			if not auction_url: break
			for i in range(10):
				yield scrapy.Request(auction_url + '&page=%d' %i, self.parse_auction)
		f.close()

	def parse_auction(self, response):
		self.browser.get(response.url)
		html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
		selector = Selector(text = html)
		category = selector.xpath('//*[@id="locbar"]/div/div/a[3]/strong/text()').extract()
		if category: category = category[0]
		f = open('/Users/minheo/PRG/searchproducts/searchproducts/spiders/search_auction.txt', 'a')
		for sel in selector.xpath('//*[@class="list_view "]'):
			item = RankproductsItem()
			title = sel.xpath('div[1]/div[2]/div[2]/div[1]/a/text()').extract()
			url = sel.xpath('div[1]/div[2]/div[2]/div[1]/a/@href').extract()
			img = sel.xpath('div[1]/div[1]/div/a/img/@data-original').extract()
			count = sel.xpath('div[2]/div[2]/div[2]/strong/text()').extract()
			site = 'auction'
			if (category) and (title) and (url) and (img) and (count) and (177 <= len(url[0]) <= 197):
				print category
				title = title[0].strip()
				#print title
				url = url[0]
				f.write(url+'\n')
				#print url
				img = img[0]
				#print img
				count = count[0]
				#print count
				#print site
				item['category'] = category
				item['title'] = title
				item['url'] = url
				item['img'] = img
				item['count'] = int(count.replace(",", ""))
				item['site'] = site
				yield item
		f.close()
