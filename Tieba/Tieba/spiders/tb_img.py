# -*- coding: utf-8 -*-
import urllib
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Tieba.items import TiebaItem


class TbImgSpider(CrawlSpider):
    name = 'tb_img'
    allowed_domains = ['tieba.baidu.com']
    kw = input('请输入贴吧名称: ')
    kw = urllib.parse.quote(kw)
    urls = 'https://tieba.baidu.com/f?kw=%s&pn=0' % kw
    print('=========', urls)
    start_urls = [urls]

    rules = (
        Rule(LinkExtractor(allow=r'pn=\d+'), callback='parse_item', follow=True),
    )

    @staticmethod
    def tz_parse(response):
        try:
            print('+' * 50, response.url)
            image_urls = response.xpath('//div[contains(@id, "post_content_")]/img[@class="BDE_Image"]\
                                       /@src').extract()
            print(image_urls)
            for image_url in image_urls:
                item = TiebaItem()
                item['image_url'] = image_url
                print(image_url)
                yield item
        except Exception as e:
            print(e)

    def parse_item(self, response):
        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        tz_urls = response.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/@href').extract()
        for tz_url in tz_urls:
            tz_url = 'https://tieba.baidu.com' + tz_url
            yield scrapy.Request(url=tz_url, callback=self.tz_parse)
