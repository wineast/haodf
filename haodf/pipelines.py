# -*- coding: utf-8 -*-

"""
pipelines.pyc存储方法
"""
import copy
import pymysql
import pymysql.cursors
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

from haodf.items import HaodfItem

SETTINGS = get_project_settings()
class HaodfPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # pipeline默认调用
    def process_item(self, item, spider):
        asynItem = copy.deepcopy(item)
        # query = self.dbpool.runInteraction(self.hospital_insert, item)  # 调用插入的方法
        # query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        # query1 = self.dbpool.runInteraction(self.department_insert, asynItem)  # 调用插入的方法
        # query1.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        query2 = self.dbpool.runInteraction(self.doctor_insert, asynItem)  # 调用插入的方法
        query2.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # def hospital_insert(self, tx, item):
    #     sql = "insert into hospital(province,city,hospital,hospital_level,hospital_type,department_num,doctor_num,telephone,hospital_href) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #     params = (item["province"], item["city"], item["hospital"], item["hospital_level"], item["hospital_type"], item["department_num"],
    #     item["doctorTotal_num"], item["telephone"], item["hospital_href"])
    #     tx.execute(sql, params)

    # def department_insert(self, tx, item):
    #     sql = "insert into department_shanghai(hospital,department,doctor_num,department_href) values(%s,%s,%s,%s)"
    #     params = (item["hospital"], item["department"], item["doctorDep_num"], item["department_href"])
    #     tx.execute(sql, params)
    #
    def doctor_insert(self, tx, item):
        sql = "insert into doctor_raw(name,pinyin,province,city,hospital,department,title,skill,score,disease,bio_url,source_url,modify_time,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"
        params = (item["name"], item["pinyin"], item["province"],item["city"],item["hospital"], item["department"], item["title"], item["skill"],item["score"], item["disease"],item["bio_url"],item["source_url"])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print('--------------database operation exception!!-----------------')
        print(failue)

class JsonPipeline(object):
    def __init__(self):
        self.file = open('./doctorlist.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item,HaodfItem):
            self.exporter.export_item(item)
            return item
