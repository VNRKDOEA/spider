import scrapy
import re
from tutorial.items import JianDanItem
from scrapy.http import Request
import pymysql
import urllib
import urllib.request
import os
import requests
import shutil
import time


#  爬取煎蛋网前100条信息
class FilmJiandanpider(scrapy.Spider):
    name = "jiandan"
    # 设定域名
    allowed_domains = ["www.jiandan.net"]
    # start_urls = []
    # 填写爬取地址rr
    start_urls = ["http://jandan.net/new"]

    def start_requests(self):
        print('爬取网址')
        # for line in self.sequence:
        #     self.start_urls.append("https://movie.douban.com/top250?start=" + line + "&filter=")

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        ul = response.xpath('//div[@id="body"]/div[@id="content"]/div[@class="post f"]')
        for info in ul:
            # print(enumerate(info.xpath("//ul/li").extract()))
            for key, value in enumerate(info.xpath("//div[@id='content']/div[@class='post f']/ul/li").extract()):
                # print(key)
                # print(value)
                # print(info.xpath("//div[@id='content']/div[@class='post f']/ul/li["+str(key + 1)+"]/a/text()").extract()[0])
                link = \
                    info.xpath(
                        "//div[@id='content']/div[@class='post f']/ul/li[" + str(key + 1) + "]/a/@href").extract()[0]
                # print(link)

                yield scrapy.Request(link, callback=self.parse_item, dont_filter=True)
                # self.parse_items(response, link)
                # res = urllib.request.urlopen(url)
                # html = res.read().decode('utf-8')
                # print(html)

                # 编写爬取方法

    def parse_item(self, response):
        all = response.xpath('//div[@id="body"]/div[@id="content"]/div[@class="post f"][1]')
        item = JianDanItem()
        item['jiandan_author'] = \
            response.xpath("//div[@id='content']/div[@class='post f'][1]/div[@class='time_s']/a/text()").extract()[0]
        item['jiandan_title'] = response.xpath("//div[@id='content']/div[@class='post f'][1]/h1/a/text()").extract()[0]
        item['jiandan_time'] = \
            response.xpath("//div[@id='content']/div[@class='post f'][1]/div[@class='time_s']/text()").extract()[0]
        jiandan_content = ""
        jiandan_img = ""
        img_url = ""

        for key, value in enumerate(response.xpath("//div[@id='content']/div[@class='post f'][1]/p").extract()):
            print(key)
            if (key == 0 and len(
                    response.xpath("//div[@id='content']/div[@class='post f'][1]/p[1]/img").extract()) > 0):
                print('这个是图片')
                jiandan_img = response.xpath(
                    "//div[@id='content']/div[@class='post f'][1]/p[1]/img/@data-original").extract()[0]
                # print(jiandan_img)
                self.saveimg(jiandan_img)
                img_url = jiandan_img.split('/').pop()
            else:
                jiandan_content = jiandan_content + response.xpath(
                    "//div[@id='content']/div[@class='post f'][1]/p[" + str(key + 1) + "]").xpath(
                    'string(.)').extract()[0]

        item['jiandan_content'] = jiandan_content
        item['jiandan_img'] = img_url

        jiandan_score = response.xpath(
            '//div[@id="content"]/div[@class="post f"][1]/div[3]/div[@class="total_votes"]/text()').extract()[0]
        item['jiandan_score'] = jiandan_score
        item['jiandan_type'] = response.xpath('//div[@id="content"]/h3/a/text()').extract()[0]
        ticks = time.time()
        item['order_id'] = ticks

        yield item




        for key, value in enumerate(response.xpath('//ol[@class="commentlist"]/li').extract()):
            n_al = {}
            n_al['author'] = response.xpath("//ol[@class='commentlist']/li[" + str(
                key + 1) + "]/div/div/div[@class='author']/strong/text()").extract()[0]
            n_al['types'] = 'jiandan'
            n_al['type'] = '煎蛋'
            n_al['age'] = response.xpath("//ol[@class='commentlist']/li[" + str(
                key + 1) + "]/div/div/div[@class='author']/small/a/text()").extract()[0]
            n_al['content'] = \
                response.xpath("//ol[@class='commentlist']/li[" + str(key + 1) + "]/div/div/div[2]/p/text()").extract()[
                    0]
            n_al['zan'] = response.xpath(
                "//ol[@class='commentlist']/li[" + str(key + 1) + "]/div/div/div[3]/span[1]/span[1]/text()").extract()[
                0]
            n_al['cai'] = response.xpath(
                "//ol[@class='commentlist']/li[" + str(key + 1) + "]/div/div/div[3]/span[2]/span[1]/text()").extract()[
                0]
            n_al['title'] = response.xpath("//ol[@class='commentlist']/li[" + str(
                key + 1) + "]/div/div/div[@class='text']/span/a/text()").extract()[0]
            n_al['order_id'] = ticks
            connect = pymysql.connect(
                user="root",
                password="dexing07",  # 连接数据库，
                port=3306,
                host="120.78.174.192",
                db="mysql",
                charset="utf8"
            )
            con = connect.cursor()  # 获取游标
            con.execute("use maoping")  # 使用数据库
            print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
            print("数据库连接成功！")

            con.execute(
                "insert into w_comment(author,title_key,types,comment_type,age,content,comment_zan,comment_cai,order_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [n_al['author'], n_al['title'], n_al['types'], n_al['type'], n_al['age'], n_al['content'], n_al['zan'],
                 n_al['cai'],n_al['order_id']
                 ])
            connect.commit()
            con.close()
            connect.close()


            # print(jiandan_content)

    def saveimg(self, url):
        if url.find('http:') ==-1:
            url = 'http:' + url
        r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        fileNames = url.split('/').pop()
        if r.status_code == 200:
            with open("./img/jiandan/" + fileNames, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
