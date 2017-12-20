# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DmozItem(Item):
    # define the fields for your item here like:
    book_title = Field()  # 标题
    book_authors = Field()  # 作者
    book_mainpic = Field()  # 图片封面
    book_score = Field()  # 点评分数
    book_type = Field()
    book_aList = Field()  # 书评


# 豆瓣电影
class FilmItem(Item):
    # define the fields for your item here like:
    film_title = Field()  # 标题
    film_year = Field()  # 上映日期
    film_authors = Field()  # 导演
    film_type = Field()  # 类型
    film_img = Field()  # 类型
    film_content = Field()  # 类型
    film_mainpic = Field()  # 图片封面

    film_score = Field()  # 豆瓣评分
    film_score5 = Field()  # 五星比率
    film_score4 = Field()  # 四星比率
    film_score3 = Field()  # 三星比率
    film_score2 = Field()  # 二星比率
    film_score1 = Field()  # 一星比率

    film_aList = Field()  # 影评


class WangYiYunItem(Item):
    # define the fields for your item here like:
    film_title = Field()  # 标题


class JianDanItem(Item):
    jiandan_time = Field()
    jiandan_title = Field()
    jiandan_author = Field()
    jiandan_content = Field()
    jiandan_type = Field()
    jiandan_score = Field()
    jiandan_img = Field()
    order_id = Field()
    jiandan_commentType = Field()


class JianDanCommentItem(Item):
    jiandan_types = Field()
    jiandan_age = Field()
    jiandan_content = Field()
    jiandan_useing = Field()
    jiandan_author = Field()
    jiandan_title = Field()
    jiandan_comment = Field()
    jiandan_zan = Field()
    jiandan_ping = Field()
    jiandan_type = Field()
    jiandan_cai = Field()
