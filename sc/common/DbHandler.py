#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LightMysql import LightMysql
from ConfigReader import ConfigReader

class DbHandler(object):

    db_execute = None

    def __init__(self):
        self.configReader = ConfigReader().get_conf("main")
        self.ip = self.configReader.mysql_ip
        self.port = self.configReader.mysql_port
        print("ip:" + self.ip + ", port:" + self.port)
        dbconfig = {
            'host': self.ip,
            'port': self.port,
            'user': 'root',
            'passwd': 'root',
            'db': 'tushare',
            'charset': 'utf8'}

        DbHandler.db_execute = LightMysql(dbconfig)
        print("DbHandler init ")

    def count_sql(self, sql):
        data = DbHandler.db_execute.select(sql)
        if len(data) < 1:
            return None
        count = data[0]["c"]
        if isinstance(count, unicode):
            count = self.encode(count)
        # self.log_info("count result-->" + str(count))
        return count

    def count_sql_default_zero(self, sql):
        value = self.count_sql(sql)
        if value is None:
            value = 0
        return value

    def delete_sql(self, sql):
        DbHandler.db_execute.dml(sql)

    def insert_sql(self, sql):
        DbHandler.db_execute.dml(sql)

    def update_sql(self, sql):
        DbHandler.db_execute.dml(sql)

    @staticmethod
    def select_list_sql(sql):
        # print(sql)
        data_list = DbHandler.db_execute.select(sql)
        if len(data_list) < 1:
            return None
        DbHandler.convert_dict_list_unicode_to_str(data_list)
        return data_list

    @staticmethod
    def select_one_sql(sql):
        data_list = DbHandler.select_list_sql(sql)
        if data_list is None:
            return data_list
        return data_list[0]

    # 把字典列表中的unicode值转换成字符串
    @staticmethod
    def convert_dict_list_unicode_to_str(data_list):
        if data_list is None:
            return data_list
        for data in data_list:
            DbHandler.convert_dict_unicode_to_str(data)
        return data_list

    # 把字典中的unicode值转换成字符串
    @staticmethod
    def convert_dict_unicode_to_str(data):
        if data is None:
            return data

        for key in data:
            value = data[key]
            if isinstance(value, unicode):
                data[key] = DbHandler.encode(value)

        return data

    # 把unicode值转化成字符串
    @staticmethod
    def encode(value):
        return value.encode('utf-8')


if __name__ == "__main__":
    sql = "select count(*) as c from t_sunso_stock_basic"
    db = DbHandler()
    result = db.count_sql(sql)
    print("result-->" + str(result))