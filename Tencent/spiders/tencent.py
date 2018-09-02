# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem 
from lxml import etree 

class TencentSpider(scrapy.Spider):
	name = 'tencent'
	allowed_domains = ['tencent.com']
	baseUrl = 'https://hr.tencent.com/position.php?&start='
	offset = 0
	start_urls = [baseUrl + str(offset)]

	def parse(self, response):
		node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
		for node in node_list:
			items = TencentItem()
			# 提取信息
			items['positionName'] = node.xpath("./td/a/text()").extract()[0]# .encode('utf-8')
			items['positionLink'] = node.xpath("./td/a/@href").extract()[0]
			if node.xpath("./td[2]/text()"):
				items['positionType'] = node.xpath("./td[2]/text()").extract()[0]
			else:	
				items['positionType'] = None

			items['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
			items['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
			items['publishTime']  = node.xpath("./td[5]/text()").extract()[0]
			# print(items)
			yield items
		if self.offset < 3300 + 10:
			self.offset += 10
			urls = self.baseUrl + str(self.offset)
			request = scrapy.Request(urls, callback=self.parse)
			yield request
	




# //div[@class='left wcont_b box']//table[@class='tablelist']//tr/td[@class='l square']