import scrapy
import re
from tutorial.items import JianDanItem
from scrapy.http import Request
import pymysql
import urllib
import urllib.request
import os
import shutil
import requests


#  爬取煎蛋网前100条信息
class FilmTestspider(scrapy.Spider):
    name = "test"
    # 设定域名
    allowed_domains = ["www.jiandan.net"]
    # start_urls = []
    # 填写爬取地址rr
    start_urls = ["http://jandan.net/new"]

    def parse(self, response):
        url = 'http://img.jandan.net/news/2017/12/cdc7bb1afd00c483939f93bae0ead86a.jpg'
        # sourceURL = url
        # save_path = r'./img'  # 保存路径
        # fileNames = sourceURL.split('/').pop()  # 这个方法太弱了点
        #
        # req = urllib.request.Request(url)
        # req.add_header("User-Agent",
        #                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
        #
        # data = urllib.request.urlopen(req)
        # print(data.info())
        # print(data.readlines())
        # print(data)
        # if not os.path.exists(save_path):
        #     os.makedirs(save_path)
        # print(sourceURL)
        # print(save_path + os.sep + fileNames)
        # urllib.request.urlretrieve(sourceURL, filename=(save_path + fileNames))
        # urllib.request.urlretrieve(sourceURL, save_path + os.sep + fileName)



        r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        fileNames = url.split('/').pop()
        if r.status_code == 200:
            with open("./img/jiandan/"+fileNames, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
