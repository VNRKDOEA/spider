import scrapy
from tutorial.items import WangYiYunItem
from scrapy.http import Request, FormRequest
import json


class FilmBanFilmSpider(scrapy.Spider):
    name = "wangyiyun"

    # 设定域名
    allowed_domains = ["music.163.com"]
    # 填写爬取地址
    start_urls = ["http://music.163.com/weapi/v1/resource/comments/R_SO_4_28819878?csrf_token="]

    # class scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback])

    def start_requests(self):
        yield scrapy.FormRequest(
            headers={'Content-Type': 'application/json; charset=UTF-8'},
            url="http://music.163.com/weapi/v1/resource/comments/R_SO_4_28819878?csrf_token=",
            formdata={
                'form_params': '7IuXjHO1Qj1HU91TBCDZb+f64Mr8l/NlQ/2GnAyLdfjEsyjHvxdkDPy92Nj+NqdRXhBGS34QS7IvEZHZ79T327x26ibyRePlPB//Zy+bU6Q69a8uMWUqoNF7IcNqTdgrzFpkZg4DdPfHmVwO9mR/CRHe1cxRq/vNNKfhVstPUrv+pGUOh1ZlRsVuxbeS7bGV',
                'encSecKey': '7550241dd3a3db72902a8df04c130b06ed23ec1d1e74075c624901fe86ce6157658f2b2efb2f014fc1bdd38e493b79b2b3e843d74998a6cb887a4869bc79f57a4a5d79c4fa35377d97fc62798ab9b26bfcffe507e5325066766d3881eaabf837c6b9def5d7462eea48d8231d839336c6ca3fd38cb64417cccfb39e0aab856ac1'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        item = dir(response.text)
        print(item)
        print(response.text)
        # print(response.status)

    def parse(self, response):
            print(response)
            print('爬取分析')
