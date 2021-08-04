# -*- coding: utf-8 -*-
import csv
import logging
import os
import traceback

import pymysql
from twisted.enterprise import adbapi

logger = logging.getLogger("YzwPipeline")


class YzwPipeline(object):
    def __init__(self, pool, settings):
        self.dbpool = pool
        self.settings = settings
        # excel_path = os.getcwd() if settings.get(
        #     "EXCEL_FILE_PATH") == '.' else settings.get("EXCEL_FILE_PATH")
        # excel_file = settings.get("EXCEL_FILE_NAME") + '.xlsx'
        # self.excelFile = os.path.join(excel_path, excel_file)

        csv_path = os.getcwd() if settings.get(
            "CSV_FILE_PATH") == '.' else settings.get("CSV_FILE_PATH")
        csv_file = settings.get("CSV_FILE_NAME") + '.csv'
        self.csvFile = os.path.join(csv_path, csv_file)

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings.get("HOST"),
            port=settings.get("PORT"),
            db=settings.get("DATABASE"),
            user=settings.get("USER"),
            passwd=settings.get("PASSWORD"),
            charset=settings.get("CHARSET"),
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connect_pool = None
        if settings.get("MYSQL"):
            YzwPipeline.__test_mysql_settings(**params)
            db_connect_pool = adbapi.ConnectionPool('pymysql', **params)
        obj = cls(db_connect_pool, settings)
        return obj

    def _create_table(self, txn):
        try:
            sql = "DROP TABLE IF EXISTS `{0}`".format(
                self.settings.get("TABLE"))
            re = txn.execute(sql)
            sql = self.settings.get("CREATE_TEBLE_SQL").format(
                self.settings.get("TABLE"))
            re = txn.execute(sql)
            logger.warning("创建表:'%s'成功." % self.settings.get('TABLE'))
        except Exception as e:
            logger.critical(traceback.format_exc())

    def open_spider(self, spider):
        if self.dbpool:
            obj = self.dbpool.runInteraction(self._create_table)
        else:
            # self.newExcelFile()
            self.newCSVFile()

    def close_spider(self, spider):
        try:
            if self.dbpool:
                self.dbpool.close()
                logger.warning(
                    "数据已存储于数据库" + self.settings.get("DATABASE") + "， 表：" + self.settings.get("TABLE"))
            else:
                # self.wbk.save(self.csvFile)
                logger.warning("excel文件已存储于 " + self.csvFile)
        except Exception as e:
            logger.error(traceback.format_exc())

    def process_item(self, item, spider):
        try:
            if self.dbpool:
                self.process_mysql(item)
            else:
                self.process_csv(item)
        except Exception as e:
            logger.critical(traceback.format_exc())

    def process_mysql(self, item):
        result = self.dbpool.runInteraction(self.insert, item)
        # 给result绑定一个回调函数，用于监听错误信息
        result.addErrback(self.error)

    def insert(self, cursor, item):
        insert_sql = "insert into {0} (`id`, `招生单位`, `院校特性`, `院系所`, `专业`,`研究方向`,`学习方式`, `拟招生人数`" \
                     ", `备注`, `业务课一`, `业务课二`, `外语`, `政治`, `所在地`, `专业代码`,`指导老师`, `门类`, `一级学科` ) " \
                     "VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}', '{15}', '{16}','{17}','{18}')" \
            .format(self.settings.get('TABLE'), item['id'], item['招生单位'], item['院校特性'], item['院系所'], item['专业'],
                    item['研究方向'], item['学习方式'], item['拟招生人数'], item['备注'],
                    item['业务课一'], item['业务课二'], item['外语'], item['政治'], item['所在地'], item['专业代码'], item['指导老师'],
                    item['门类'], item['一级学科'])
        cursor.execute(insert_sql)

    def error(self, reason):
        # 跳过主键重复error
        if reason.value.args[0] != 1062:
            logger.error("insert to database err: -------------\n" + reason.getErrorMessage() + "\n" + str(
                reason.getTraceback()))

    # def process_excel(self, item):
    #     flag = False if (self.row & 1 == 0) else True
    #     for i in range(0, YzwItem.fields.__len__()):
    #         ret = self.sheet.write(self.row, i, item[self.list[i]])
    #     self.row += 1
    def process_csv(self, item):
        with open(self.csvFile, 'a', newline='', encoding='gbk') as csv_file:
            fieldnames = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数',
                          '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
            # for i in range(0, YzwItem.fields.__len__()):
            writer.writerow(item)

    # def newExcelFile(self):
    #     # self.wbk = xlwt.Workbook()
    #     self.wbk = openpyxl.Workbook()

    #     # self.sheet = self.wbk.add_sheet('Sheet1')
    #     self.sheet = self.wbk.create_sheet('Sheet1')

    #     self.row = 1

    #     self.list = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数',
    #                  '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
    #     for i in range(0, YzwItem.fields.__len__()):
    #         self.sheet.write(0, i, self.list[i])

    def newCSVFile(self):
        self.list = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数',
                     '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
        with open(self.csvFile, 'a', newline='', encoding='gbk') as csv_file:
            fieldnames = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数',
                          '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    @staticmethod
    def __test_mysql_settings(**params):
        try:
            db = pymysql.connect(**params)
            db.close()
        except Exception as e:
            logger.critical(str(e))
            os._exit(1)
