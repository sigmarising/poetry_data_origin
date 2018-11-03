# -*- coding: utf-8 -*-
import scrapy
from poetry_crawl.items import PoetryCrawlItem


class PoetrySpiderSpider(scrapy.Spider):
    name = 'poetry_spider'

    allowed_domains = ['www.guoxuedashi.com']
    base_url = 'http://www.guoxuedashi.com'
    start_urls = ['http://www.guoxuedashi.com/shici/']

    def parse(self, response):
        dynasty_list = response.xpath("//div[@class='info_content zj clearfix']//dl")
        for i_dynasty in dynasty_list:

            item_da = PoetryCrawlItem()  # da means for DynastyAuthor
            item_da["dynasty"] = i_dynasty.xpath("./dt/text()").extract_first()  # get the dynasty
            item_da["dynasty"] = item_da["dynasty"].lstrip('【').rstrip('】')

            # get every author with the specify dynasty
            author_list = i_dynasty.xpath(".//dd/a")
            for i_author in author_list:
                item_da["author"] = i_author.xpath("./text()").extract_first()  # get the author
                next_url = self.base_url + i_author.xpath("./@href").extract_first()  # get the author url

                # yield to next parse: parse_author
                yield scrapy.Request(
                    url=next_url,
                    meta={
                        'dynasty': item_da['dynasty'],
                        'author': item_da['author']
                    },
                    dont_filter=True,
                    callback=self.parse_author
                )

    def parse_author(self, response):
        item_da = PoetryCrawlItem()
        item_da["dynasty"] = response.meta['dynasty']
        item_da["author"] = response.meta['author']

        intro = response.xpath("//div[@class='info_txt2 clearfix']/p/text()")
        item_da["intro"] = ''.join(intro.extract()).strip()  # get the intro

        # get the items url
        item_list = response.xpath("//div[@class='info_cate clearfix']/dl//dd/a")
        for i_item in item_list:
            item_da["title"] = i_item.xpath("./text()").extract_first()
            next_url = self.base_url + i_item.xpath("./@href").extract_first()

            # yield to next parse: parse_poetry
            yield scrapy.Request(
                url=next_url,
                meta={
                    'dynasty': item_da['dynasty'],
                    'author': item_da['author'],
                    'intro': item_da['intro'],
                    'title': item_da['title']
                },
                dont_filter=True,
                callback=self.parse_poetry
            )

    def parse_poetry(self, response):
        item_da = PoetryCrawlItem()
        item_da["dynasty"] = response.meta['dynasty']
        item_da["author"] = response.meta['author']
        item_da["intro"] = response.meta['intro']
        item_da["title"] = response.meta['title']

        content = response.xpath("//div[@class='info_txt2 clearfix']/p/text()")
        item_da["content"] = "".join(content.extract()).strip()

        yield item_da