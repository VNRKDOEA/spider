import scrapy
from tutorial.items import DmozItem
import urllib.request
import os

class markSpider(scrapy.Spider):
    name = "marking"
    # 设定域名
    allowed_domains = ["book.douban.com"]
    # 填写爬取地址
    start_urls = ["https://book.douban.com/subject/27145128/"]

    # 编写爬取方法
    def parse(self, response):
        sourceURL = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1910813120.jpg'
        save_path = r'./img/'  # 保存路径
        fileName = sourceURL.split('/').pop()  # 这个方法太弱了点
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        urllib.request.urlretrieve(sourceURL, save_path + os.sep + fileName)
