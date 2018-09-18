# -*- coding: utf-8 -*-
import scrapy
import urllib
from Tieba.items import TiebaItem


class TImageSpider(scrapy.Spider):
    name = 't_image'
    allowed_domains = ['tieba.baidu.com']
    kw = input('请输入贴吧名称: ')
    kw = urllib.parse.quote(kw)
    pn = 0
    urls = 'https://tieba.baidu.com/f?kw=%s&pn=%s' % (kw, pn)
    print('=========', urls)
    start_urls = [urls]

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

    def parse(self, response):
        all_pn = response.xpath('//div[@id="frs_list_pager"]/a[@class="last pagination-item "]/\
        @href').extract()[0].split('pn=')[1]
        tz_urls = response.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a/@href').extract()
        for tz_url in tz_urls:
            tz_url = 'https://tieba.baidu.com' + tz_url
            yield scrapy.Request(url=tz_url, callback=self.tz_parse)

            if self.pn <= int(all_pn):
                self.pn += 50
            urls = 'https://tieba.baidu.com/f?kw=%s&pn=%s' % (self.kw, self.pn)
            yield scrapy.Request(url=urls, callback=self.parse)
