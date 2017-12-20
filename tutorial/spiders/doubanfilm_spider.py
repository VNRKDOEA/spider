import scrapy
from tutorial.items import FilmItem
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import pymysql
import urllib
import urllib.request
import os


class FilmBanFilmSpider(scrapy.Spider):
    name = "doubanfilm"
    # 设定域名
    allowed_domains = ["movie.douban.com"]
    # 填写爬取地址
    start_urls = []
    sequence = ['0', '25', '50', '75', '100', '125', '150', '175', '200', '225']

    # 先抓取网址
    def start_requests(self):
        print('爬取网址')
        for line in self.sequence:
            self.start_urls.append("https://movie.douban.com/top250?start=" + line + "&filter=")

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        all = response.xpath('//div[@id="wrapper"]')
        for info in all:
            # print(type((info.xpath(
            #     '//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li').extract())))
            lisp = response.xpath(
                '//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li').extract()
            for key, value in enumerate(response.xpath(
                    '//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li').extract()):
                link = info.xpath(
                    '//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li[' + str(
                        key + 1) + ']/div[@class="item"]/div[@class="pic"]/a/@href').extract()[0]

                yield Request(link, callback=self.parse_item)

    # 编写爬取方法
    def parse_item(self, response):
        # 实例一个容器保存爬取的信息
        item = FilmItem()
        # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        # 先获取每个课程的div
        all = response.xpath('//div[@id="wrapper"]')
        film_type = ''  # 存储电影类型
        film_aList = []  # 存储电影评论
        for info in all:
            item['film_title'] = info.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]  # 标题
            item['film_year'] = info.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()[
                0]  # 上映日期
            item['film_authors'] = \
                info.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()[
                    0]  # 导演
            for type in info.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract():
                # film_type.append(type)
                film_type = film_type + type + ','
            item['film_type'] = film_type
            item['film_mainpic'] = info.xpath('//div[@id="mainpic"]/a[@class="nbgnbg"]/img/@src').extract()[0]
            # 保存图片
            pic = str(info.xpath('//div[@id="mainpic"]/a[@class="nbgnbg"]/img/@src').extract()[0])
            self.saveimg(pic)

            item['film_score'] = \
                info.xpath('//div[@class="rating_self clearfix"]/strong[@property="v:average"]/text()').extract()[0]
            item['film_score5'] = \
                info.xpath('//div[@class="ratings-on-weight"]/div[1]/span[@class="rating_per"]/text()').extract()[0]
            item['film_score4'] = \
                info.xpath('//div[@class="ratings-on-weight"]/div[2]/span[@class="rating_per"]/text()').extract()[0]
            item['film_score3'] = \
                info.xpath('//div[@class="ratings-on-weight"]/div[3]/span[@class="rating_per"]/text()').extract()[0]
            item['film_score2'] = \
                info.xpath('//div[@class="ratings-on-weight"]/div[4]/span[@class="rating_per"]/text()').extract()[0]
            item['film_score1'] = \
                info.xpath('//div[@class="ratings-on-weight"]/div[5]/span[@class="rating_per"]/text()').extract()[0]

            # item['film_aList'] = info.xpath('//div[@id="hot-comments"]/div')


            for key, val in enumerate(info.xpath('//div[@id="hot-comments"]/div[@class="comment-item"]').extract()):
                # print(info.xpath('//div[@id="hot-comments"]/div[@class="comment-item"]/div[@class="comment"]/h3/span[@class="comment-info"]').extract()[0])
                n_al = {}

                n_al['age'] = info.xpath(
                    '//div[@id="hot-comments"]/div[@class="comment-item"][' + str(
                        key + 1) + ']/div[@class="comment"]/h3/span[@class="comment-info"]/span[3]/@title').extract()[
                    0]
                n_al['author'] = info.xpath(
                    '//div[@id="hot-comments"]/div[@class="comment-item"][' + str(
                        key + 1) + ']/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()').extract()[
                    0]
                n_al['content'] = (info.xpath(
                    '//div[@id="hot-comments"]/div[@class="comment-item"][' + str(
                        key + 1) + ']/div[@class="comment"]/p/text()').extract()[
                                       0]).strip()
                n_al['use'] = info.xpath(
                    '//div[@id="hot-comments"]/div[@class="comment-item"][' + str(
                        key + 1) + ']/div[@class="comment"]/h3/span[1]/span[1]/text()').extract()[
                    0]
                n_al['title_key'] = info.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]  # 标题
                n_al['comment_img'] = (
                    info.xpath('//div[@id="mainpic"]/a[@class="nbgnbg"]/img/@src').extract()[0]).split('/').pop()

                film_aList.append(n_al)

                # 存储到数据库


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
                    "insert into w_comment(age,author,content,useing,types,title_key,comment_img) values(%s,%s,%s,%s,%s,%s,%s)",
                    [n_al['age'], n_al['author'], n_al['content'], n_al['use'], 'douban', n_al['title_key'],
                     n_al['comment_img']
                     ])
                connect.commit()
                con.close()
                connect.close()

            item['film_aList'] = film_aList

            # filename = "data.txt"
            # self.database(filename, item)
            yield item

    def saveimg(self, url):
        sourceURL = url
        save_path = r'./img/'  # 保存路径
        fileName = sourceURL.split('/').pop()  # 这个方法太弱了点
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        urllib.request.urlretrieve(sourceURL, save_path + os.sep + fileName)
