# -*- coding: utf-8 -*-
import csv
import logging
import os
import traceback

logger = logging.getLogger("YzwPipeline")


class YzwPipeline(object):
    def __init__(self, settings):
        self.list = ['id', '招生单位', '院校特性', '院系所', '专业', '研究方向', '学习方式', '拟招生人数',
                     '业务课一', '业务课二', '外语', '政治', '所在地', '专业代码', '指导老师', '门类', '一级学科', '备注']
        csv_path = os.getcwd() if settings.get(
            "CSV_FILE_PATH") == '.' else settings.get("CSV_FILE_PATH")
        csv_file = settings.get("CSV_FILE_NAME") + '.csv'
        self.csvFile = os.path.join(csv_path, csv_file)

    @classmethod
    def from_settings(cls, settings):
        obj = cls(settings)
        return obj

    def open_spider(self, spider):
        self.new_csv_file()

    def close_spider(self, spider):
        try:
            logger.warning(" csv 文件已存储于 " + self.csvFile)
        except Exception as e:
            logger.error(traceback.format_exc())

    def process_item(self, item, spider):
        try:
            self.process_csv(item)
        except Exception as e:
            logger.critical(traceback.format_exc())

    def error(self, reason):
        # 跳过主键重复error
        if reason.value.args[0] != 1062:
            logger.error("insert to database err: -------------\n" + reason.getErrorMessage() + "\n" + str(
                reason.getTraceback()))

    def process_csv(self, item):
        with open(self.csvFile, 'a', newline='', encoding='gbk') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.list, delimiter=',')
            writer.writerow(item)

    def new_csv_file(self):
        with open(self.csvFile, 'w+', newline='', encoding='gbk') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.list, delimiter=',')
            writer.writeheader()
