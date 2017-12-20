import scrapy
from tutorial.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    # 设定域名
    allowed_domains = ["book.douban.com"]
    # 填写爬取地址
    start_urls = ["https://book.douban.com/subject/27145128/"]

    # 编写爬取方法
    def parse(self, response):
        # 实例一个容器保存爬取的信息
        item = DmozItem()
        # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        # 先获取每个课程的div
        all = response.xpath('//div[@id="wrapper"]')
        for info in all:
            item['book_title'] = info.xpath('h1/span/text()').extract()[0]              # 标题
            item['book_authors'] = info.xpath('//div[@id="info"]/span[1]/a[1]/text()').extract()[0]  # 作者
            item['book_mainpic'] = info.xpath('//div[@id="mainpic"]/a[@class="nbg"]/@href').extract()[0]  # 图片封面
            item['book_score'] = info.xpath(
                '//div[@id="interest_sectl"]//div[@class="rating_wrap clearbox"]//div[@class="rating_self clearfix"]//strong/text()').extract()[
                0]  # 评分
            item['book_type'] = '书籍'
            # 获取div中的学生人数
        comment = response.xpath('//div[@class="comment-list hot show"]/ul/li')

        aList = []

        for com in comment:
            comments = com.xpath('div[@class="comment"]/p/text()').extract()
            aList.append(comments)  # 前五评论

        item['book_aList'] = aList
        # yield item
