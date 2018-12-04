#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from DbEngineHandler import DbEngineHandler
from DateHandler import DateHandler
from TemplateHandler import TemplateHandler


class TrackBace(DbHandler, DbEngineHandler, object):
    trade_date = None
    classify_type = None

    t_sunso_stock_day_trade_statistic_core_data = "t_sunso_stock_day_trade_statistic_core_data"
    t_sunso_stock_classify_track_basic = "t_sunso_stock_classify_track_basic"
    t_sunso_stock_classify_track_config = "t_sunso_stock_classify_track_config"

    def __init__(self):
        super(TrackBace, self).__init__()
        DbEngineHandler.__init__(self)
        print("TrackBace init")

    def init_classify_track_portal(self):
        date_list = self.get_classify_track_data_list()
        if date_list is None:
            return
        for date in date_list:
            self.trade_date = DateHandler.get_date_str(date["trade_date"])
            self.init_classify_track_basic()
            self.init_classify_track_config()
            self.init_classify_track_reback_stock_data()
            self.init_list_classify_track_day_data()
            self.init_list_classify_track_stock_day_data()

    def get_classify_track_data_list(self):
        sql = "select distinct trade_date from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where 1 > 0 order by trade_date asc"
        return self.select_list_sql(sql)

    def init_classify_track_basic(self):
        print("do nothing")

    def update_classify_track_basic(self, classify_track_basic_data):
        print("do nothing")

    def init_classify_track_config(self):
        print("do nothing")

    def init_classify_track_reback_stock_data(self):
        sql = "select * from " + self.t_sunso_stock_classify_track_config + " " \
              "where track_date='" + self.trade_date + "'"
        data_list = self.select_list_sql(sql)
        if data_list is None:
            return
        for data in data_list:
            template_key = "industry_insert_stock_classify_track_reback_stock_data.sql"
            sql = self.get_sql_by_template(template_key, data)
            self.insert_sql(sql)

    def init_list_classify_track_day_data(self):
        data_list = self.get_calssify_track_list_by_classify_type()
        if data_list is None:
            return
        for data in data_list:
            if self.track_date_after_trade_date(data):
                continue
            self.init_one_classify_track_day_data(data)
            self.update_classify_track_basic(data)

    def init_one_classify_track_day_data(self, data):
        print("do nothing")

    def init_list_classify_track_stock_day_data(self):
        data_list = self.get_calssify_track_list_by_classify_type()
        if data_list is None:
            return
        for data in data_list:
            if self.track_date_after_trade_date(data):
                continue
            stock_list = self.get_classify_stock_list(data)
            if stock_list is None:
                continue
            for stock in stock_list:
                self.handle_one_stock_data(data, stock)

    def track_date_after_trade_date(self, classify_track_basic_data):
        track_date = DateHandler.get_date_str(classify_track_basic_data["track_date"])
        return DateHandler.compare_greater_equal_two_date_str(track_date, self.trade_date)

    def get_calssify_track_list_by_classify_type(self):
        sql = "select * from " + self.t_sunso_stock_classify_track_basic + " " \
              "where classify_type='" + self.classify_type + "'"
        return self.select_list_sql(sql)

    def get_classify_stock_list(self, classify_track_basic_data):
        return None

    def handle_one_stock_data(self, classify_track_basic_data, stock):
        code = stock["code"]
        trade_date_close_amt = stock["close_amt"]
        track_date = classify_track_basic_data["track_date"]

        data = {"trade_date": self.trade_date,
                "classify_type": classify_track_basic_data["classify_type"],
                "classify_name": classify_track_basic_data["classify_name"],
                "track_date": track_date,
                "code": code, "name": stock["name"],
                "close_amt": trade_date_close_amt,
                "close_amt_ratio": stock["close_pre_close_diff_amt_ratio"],
                }

        data["track_sum_day"] = self.get_stock_count_value_by_between_date(data)
        data["sum_close_amt_ratio"] = round(self.get_stock_sum_close_amt_ratio_value_by_between_date(data), 2)
        data["avg_close_amt_ratio"] = round(self.get_stock_avg_close_amt_ratio_value_by_between_date(data), 2)

        stock_data = {"code": code, "trade_date": track_date}

        track_date_close_amt = self.get_stock_close_amt_by_date(stock_data)
        data["track_date_close_amt"] = track_date_close_amt
        data["track_date_close_amt_ratio"] = self.get_stock_close_pre_close_diff_amt_ratio_by_date(stock_data)
        data["from_track_date_up_down_ratio"] = self.cal_percent_round_2_not_zero(trade_date_close_amt, track_date_close_amt)

        template_key = "industry_insert_stock_classify_track_stock_day_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def get_stock_close_amt_by_date(self, data):
        return self.get_stock_column_value_by_date(data, "close_amt")

    def get_stock_close_pre_close_diff_amt_ratio_by_date(self, data):
        return self.get_stock_column_value_by_date(data, "close_pre_close_diff_amt_ratio")

    def get_stock_column_value_by_date(self, data, column):
        data["column"] = column
        template_key = "stock_column_value_by_one_date.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_stock_count_value_by_between_date(self, data):
        return self.get_stock_column_value_by_between_date(data, "count(*)")

    def get_stock_sum_close_amt_ratio_value_by_between_date(self, data):
        return self.get_stock_column_value_by_between_date(data, "sum(close_pre_close_diff_amt_ratio)")

    def get_stock_avg_close_amt_ratio_value_by_between_date(self, data):
        return self.get_stock_column_value_by_between_date(data, "avg(close_pre_close_diff_amt_ratio)")

    def get_stock_column_value_by_between_date(self, data, column):
        data["column"] = column
        template_key = "stock_column_value_by_between_date.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        return path + "/sql/"

    # 计算百分比，并进行四舍五入保留2为小数
    def cal_percent_round_2_not_zero(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100

        return round(((first_value - second_value) / second_value) * 100, 2)