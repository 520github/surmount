#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pystache as tp


class BaseSqlHandler(object):

    def __init__(self):
        print("BaseSqlHandler init")

    @staticmethod
    def get_t_sunso_stock_day_trade_statistic_core_data_insert_sql(data):
        return BaseSqlHandler.get_insert_sql_by_tp_file(
            "tp_day_trade_statistic_core.sql", data)

    @staticmethod
    def get_t_sunso_stock_day_trade_statistic_volume_data_insert_sql(data):
        return BaseSqlHandler.get_insert_sql_by_tp_file(
            "tp_day_trade_statistic_volume.sql", data)

    @staticmethod
    def tp_select_column_from_newly_quotes_data_hist_by_pre_date(data):
        return BaseSqlHandler.get_insert_sql_by_tp_file(
            "tp_select_column_from_newly_quotes_data_hist_by_pre_date.sql", data)

    @staticmethod
    def get_insert_sql_by_tp_file(tp_file, data):
        t = open(BaseSqlHandler.get_sql_path(tp_file), "r")
        sql = tp.render(t.read(), data)
        # print("sql-->" + sql)
        return sql

    @staticmethod
    def get_sql_path(name):
        return "../sql/" + name


# data = {"a":'hello',"b":100,"c":"yes"}
# BaseSqlHandler.get_insert_sql(data)