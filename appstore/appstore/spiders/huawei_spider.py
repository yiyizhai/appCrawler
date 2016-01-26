import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
	name = "huawei"
	allowed_domains = ["huawei.com"]

	start_urls = [
			"http://appstore.huawei.com/more/all"
	]

	@classmethod
	def parse(self, response):
		page = Selector(response)

		hrefs = page.xpath('//h4[@class="title"]/a/@href')

		for href in hrefs:
			url = href.extract()
			yield scrapy.Request(url, callback=self.parse_item)

	@classmethod
	def parse_item(self, response):
		page = Selector(response)
		item = AppstoreItem()

		item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
		item['url'] = response.url
		item['appid'] = re.match(r'http://.*/(.*)', item ['url']).group(1)
		item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
		item['thumbnail'] = page.xpath('//li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first()
		#item['thumbnail'] = re.match(r'http://.*/(.*)', turl).group(1)

		yield item

