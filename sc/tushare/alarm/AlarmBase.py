#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from TemplateHandler import TemplateHandler


class AlarmBase(DbHandler, object):

    trade_date = None
    alarm_stock_data_list = []
    limit = 5
    column_key = "column"
    date_compare_key = "date_compare"
    plate_name = None
    plate_start_date = None

    def __init__(self):
        super(AlarmBase, self).__init__()
        print("AlarmBase init ")

    def alarm_stock_list(self):
        stock_data_list = self.get_stock_data_list()
        for stock_data in stock_data_list:
            if self.alarm_stock_one(stock_data):
                self.alarm_stock_data_list.append(stock_data)

        self.join_to_plate()
        return self.alarm_stock_data_list

    def join_to_plate(self):
        data = {"plate_name": self.plate_name, "plate_start_date": self.plate_start_date,
                "join_date": self.trade_date, "trade_date": self.trade_date, "codes": self.get_alarm_stock_codes()}
        template_key = "insert_sunso_stock_plate_stock.sql"
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def alarm_stock_one(self, stock_data):
        return False

    def get_alarm_stock_codes(self):
        codes = ""
        for stock in self.alarm_stock_data_list:
            codes = codes + "'" + stock["code"] + "',"
        codes = codes + "''"
        return codes

    def get_stock_data_list(self):
        sql = "select * from t_sunso_stock_day_trade_statistic_core_data " \
              "where trade_date='" + self.trade_date + "' and open_amt > 0"
        return self.select_data_list(sql)

    def get_one_stock_data_by_date(self, code, trade_date):
        data = {"code": code, "trade_date": trade_date}
        template_key = "get_one_stock_data_by_date.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.select_one_sql(sql)

    def get_stock_code(self, stock_data):
        return stock_data["code"]

    def get_data_dict_by_stock_data(self, stock_data):
        return {"code": self.get_stock_code(stock_data)}

    def get_avg_turnover_rate_value_by_trade_statistic_core_data(self, data):
        if self.column_key not in data.keys():
            data[self.column_key] = "avg(turnover_rate)"
        return self.get_column_value_by_trade_statistic_core_data(data)

    def get_avg_small_sum_trade_amt_ratio_by_trade_statistic_volume_data(self, data):
        if self.column_key not in data.keys():
            data[self.column_key] = "avg(small_sum_trade_amt_ratio)"
        return self.get_column_value_by_trade_statistic_volume_data(data)

    def get_column_value_by_trade_statistic_volume_data(self, data):
        template_key = "get_column_value_by_trade_statistic_volume_data.sql"
        return self.get_column_value_by_template(template_key, data)

    def get_column_value_by_trade_statistic_core_data(self, data):
        template_key = "get_column_value_by_trade_statistic_core_data.sql"
        return self.get_column_value_by_template(template_key, data)

    def get_column_value_by_template(self, template_key, data):
        trade_date_key = "trade_date"
        if trade_date_key not in data.keys():
            data[trade_date_key] = self.trade_date

        if self.date_compare_key not in data.keys():
            data[self.date_compare_key] = "<="

        sort_key = "sort"
        if sort_key not in data.keys():
            data[sort_key] = "desc"

        limit_key = "limit"
        if limit_key not in data.keys():
            data[limit_key] = self.limit

        sql = self.get_sql_by_template(template_key, data)
        # print(sql)
        return self.count_sql_default_zero(sql)

    def select_data_list(self, sql):
        return self.select_list_sql(sql)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        return sql

    def get_tempalte_path(self):
        return "./sql/"
