#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../common'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../tushare'))
from ConfigReader import ConfigReader
from LightMysql import LightMysql
from TushareBase import TushareBase


class TableColumnTest(object):

    db_execute = None

    def __init__(self):
        # super(TableColumnTest, self).__init__()
        # self.configReader = ConfigReader().get_conf("main")

        dbconfig = {
            'host': '127.0.0.1',
            'port': 3307,
            'user': 'root',
            'passwd': 'root',
            'db': 'tushare',
            'charset': 'utf8'}
        TableColumnTest.db_execute = LightMysql(dbconfig)

        print("TableColumnTest init")

    def select_sql(self, sql):
        return TableColumnTest.db_execute.select(sql)

    def show_table_colums(self, table_name):
        sql = "select * from " + table_name + " limit 1"
        data = self.select_sql(sql)[0]
        result = ""
        for column in data:
            result = result + column + ","

        print("result-->" + result)
        return result


column = TableColumnTest()
column.show_table_colums("t_sunso_stock_day_trade_statistic_data")
# column.show_table_colums("t_tushare_stock_basic")
