import scrapy

from scrapy.loader import ItemLoader

from ..items import OrientbankItem
from itemloaders.processors import TakeFirst


class OrientbankSpider(scrapy.Spider):
	name = 'orientbank'
	start_urls = ['https://www.orient-bank.com/news-updates/']

	def parse(self, response):
		post_links = response.xpath('//section')
		for post in post_links:
			title = post.xpath('.//span[@class="sub-section-header"]/text()').get()
			description = post.xpath('.//div[@class="col-md-12 col-xs-12 details"]//text()[normalize-space()]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()
			date = post.xpath('.//span[@class="pull-right date"]/text()').get()

			item = ItemLoader(item=OrientbankItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
