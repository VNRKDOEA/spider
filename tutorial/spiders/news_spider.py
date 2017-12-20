import scrapy
import re

class FilmWeixinSpider(scrapy.Spider):
    name = "news"
    # 设定域名
    allowed_domains = ["weixin.sogou.com"]
    # 填写爬取地址rr
    start_urls = ["http://weixin.sogou.com/weixin?type=2&s_from=input&query=fuck&ie=utf8&_sug_=n&_sug_type_="]

    # def start_requests(self):



    def parse(self, response):
        all = response.xpath('//div[@class="news-box"]')
        print(all)
        for info in all:
            for li in info.xpath('//ul[@class="news-list"]/li').extract():
                title = info.xpath('//div[@class="txt-box"]/h3/a')
                print(title.xpath('string(.)').extract()[0])
                imgs = info.xpath('//')




