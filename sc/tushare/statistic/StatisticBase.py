#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from DbEngineHandler import DbEngineHandler
from DateHandler import DateHandler
from TemplateHandler import TemplateHandler


class StatisticBase(DbHandler, DbEngineHandler, object):
    trade_date = None
    limit = 5
    limit_key = "limit"
    column_key = "column"
    date_compare_key = "date_compare"

    close_pre_close_diff_amt_ratio = "close_pre_close_diff_amt_ratio"
    open_pre_close_diff_amt_ratio = "open_pre_close_diff_amt_ratio"
    low_pre_close_diff_amt_ratio = "low_pre_close_diff_amt_ratio"
    high_pre_close_diff_amt_ratio = "high_pre_close_diff_amt_ratio"
    low_high_diff_amt_ratio = "low_high_diff_amt_ratio"

    t_sunso_stock_day_trade_statistic_core_data = "t_sunso_stock_day_trade_statistic_core_data"
    t_sunso_stock_day_trade_statistic_range_avg_data = "t_sunso_stock_day_trade_statistic_range_avg_data"

    def __init__(self):
        super(StatisticBase, self).__init__()
        DbEngineHandler.__init__(self)
        print("StatisticBase init")

    def load_statistic_data(self):
        date_list = self.get_stock_date_list()
        if date_list is None:
            return
        for date in date_list:
            self.trade_date = DateHandler.get_date_str(date["trade_date"])
            stock_data_list = self.get_stock_data_list()
            if stock_data_list is None:
                continue
            for data in stock_data_list:
                data["trade_date"] = DateHandler.get_date_str(data["trade_date"])
                self.handle_one_stock_data(data)

    def handle_one_stock_data(self, data):
        print("do nothing")

    def get_stock_date_list(self):
        sql = "select distinct trade_date from " \
              "" + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where 1 > 0 " \
              # "and trade_date='2018-11-16'"
        return self.select_data_list(sql)

    def get_stock_data_list(self):
        sql = "select * from t_sunso_stock_day_trade_statistic_core_data " \
              "where trade_date='" + self.trade_date + "' and open_amt > 0 " \
              " and code not in (select code from " \
              "" + self.t_sunso_stock_day_trade_statistic_range_avg_data + " " \
              "where trade_date='" + self.trade_date + "') "
              # " and code='600133'"
        return self.select_data_list(sql)

    def select_data_list(self, sql):
        return self.select_list_sql(sql)

    def get_pre_plus_count_close_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_plus_count(data, self.close_pre_close_diff_amt_ratio, limit)

    def get_pre_plus_count_open_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_plus_count(data, self.open_pre_close_diff_amt_ratio, limit)

    def get_pre_plus_count_low_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_plus_count(data, self.low_pre_close_diff_amt_ratio, limit)

    def get_pre_plus_count_high_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_plus_count(data, self.high_pre_close_diff_amt_ratio, limit)

    def get_pre_plus_count_low_high_diff_amt_ratio(self, data, limit):
        return self.get_pre_plus_count(data, self.low_high_diff_amt_ratio, limit)

    def get_pre_plus_count(self, data, column, limit):
        data["dynamicCondition"] = " and " + column + " > 0 "
        data[self.column_key] = "count(*)"
        data[self.limit_key] = limit
        return self.get_column_value_by_trade_statistic_core_data(data)

    def get_pre_avg_low_high_diff_amt_ratio(self, data, limit):
        return self.get_pre_avg_value(data, self.low_high_diff_amt_ratio, limit)

    def get_pre_avg_high_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_avg_value(data, self.high_pre_close_diff_amt_ratio, limit)

    def get_pre_avg_low_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_avg_value(data, self.low_pre_close_diff_amt_ratio, limit)

    def get_pre_avg_open_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_avg_value(data, self.open_pre_close_diff_amt_ratio, limit)

    def get_pre_avg_close_pre_close_diff_amt_ratio(self, data, limit):
        return self.get_pre_avg_value(data, self.close_pre_close_diff_amt_ratio, limit)

    def get_pre_avg_value(self, data, column, limit):
        data[self.column_key] = "avg(" + column + ")"
        data[self.limit_key] = limit
        return self.get_column_value_by_trade_statistic_core_data(data)

    def get_column_value_by_trade_statistic_core_data(self, data):
        template_key = "get_column_value_by_pre_day_from_trade_statistic_core_data.sql"
        return self.get_column_value_by_template(template_key, data)

    def get_column_value_by_template(self, template_key, data):
        trade_date_key = "trade_date"
        if trade_date_key not in data.keys():
            data[trade_date_key] = self.trade_date

        if self.date_compare_key not in data.keys():
            data[self.date_compare_key] = "<"

        sort_key = "sort"
        if sort_key not in data.keys():
            data[sort_key] = "desc"

        if self.limit_key not in data.keys():
            data[self.limit_key] = self.limit

        sql = self.get_sql_by_template(template_key, data)
        #print(sql)
        return round(self.count_sql_default_zero(sql),2)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        return path + "/sql/"