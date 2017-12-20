# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
from scrapy.conf import settings
import pymysql


class TutorialPipeline(object):
    def ___init__(self):
        self.file = open('data.json', 'w', encoding='utf-8')

    # def process_item(self, item, spider):
    #     # 读取数据
    #     line = json.dumps(dict(item), ensure_ascii=False) + '\n'
    #     # 写入文件
    #     f = open('./data/data.json', 'w', encoding='utf-8')
    #     f.write(line)
    #
    #     # 返回item
    #     return item
    #
    #     # 该方法在spider被开启时被调用。

    def process_item(self, item, spider):
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

        # self.insetdouban(con, item)

        con.execute(
            "insert into w_news(author,title,time,content,score,type,img,order_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",
            [item['jiandan_author'], item['jiandan_title'], item['jiandan_time'], item['jiandan_content'],
             item['jiandan_score'], item['jiandan_type'], item['jiandan_img'], item['order_id']])

        print("豆瓣爬虫 insert success")  # 测试语句
        connect.commit()
        con.close()
        connect.close()

        return item

    def insetdouban(con, item):
        con.execute(
            "insert into w_douban(film_title,film_year,film_authors,film_type,film_mainpic,film_score,film_score5,film_score4,film_score3,film_score2,film_score1)"
            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [item['film_title'], item['film_year'], item['film_authors'], item['film_type'],
             item['film_mainpic'], item['film_score'], item['film_score5'], item['film_score4'],
             item['film_score3'], item['film_score2'], item['film_score1']])

        for film_aList in item['film_aList']:
            print(film_aList)
            con.execute("insert into w_comment(age,author,content,useing,types) values(%s,%s,%s,%s,%s)",
                        [film_aList['age'], film_aList['author'], film_aList['content'], film_aList['use'], 'douban'
                         ])
        return item
