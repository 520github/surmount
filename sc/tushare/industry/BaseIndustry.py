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


class BaseIndustry(DbHandler, DbEngineHandler, object):

    def __init__(self):
        super(BaseIndustry, self).__init__()
        DbEngineHandler.__init__(self)
        print("BaseIndustry init")

    def get_down_count(self, data):
        data["symbol"] = "<"
        return self.get_up_down_count(data)

    def get_up_count(self, data):
        data["symbol"] = ">="
        return self.get_up_down_count(data)

    def get_down_avg(self, data):
        data["symbol"] = "<"
        return self.get_up_down_avg(data)

    def get_up_avg(self, data):
        data["symbol"] = ">="
        return self.get_up_down_avg(data)

    def get_up_down_avg(self, data):
        data["column"] = "avg(close_pre_close_diff_amt_ratio) as c"
        return self.get_up_down_column(data)

    def get_up_down_count(self, data):
        data["column"] = "count(*) as c"
        return self.get_up_down_column(data)

    def get_up_down_column(self, data):
        template_key = "day_industry_up_down_column_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_down_limit_count(self, data):
        data["up_down_column"] = "down_limit_type"
        return self.get_up_down_limit_count(data)

    def get_up_limit_count(self, data):
        data["up_down_column"] = "up_limit_type"
        return self.get_up_down_limit_count(data)

    def get_up_down_limit_count(self, data):
        data["column"] = "count(*) as c"
        return self.get_up_down_limt_column(data)

    def get_up_down_limit_avg(self, data):
        data["column"] = "avg(close_pre_close_diff_amt_ratio) as c"

    def get_up_down_limt_column(self, data):
        template_key = "day_industry_up_down_limit_column_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_up_top3_name(self, data):
        template_key = "day_industry_up_top3_stock_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql(sql)

    def get_down_top3_name(self, data):
        template_key = "day_industry_down_top3_stock_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql(sql)

    def get_pre_day_avg_trade_count(self, data, limit):
        return round(self.get_pre_day_industry_column_value(data, limit, "avg(trade_count)"), 2)

    def get_pre_day_avg_trade_amt(self, data, limit):
        return round(self.get_pre_day_industry_column_value(data, limit, "avg(trade_amt)"), 6)

    def get_pre_day_avg_trade_volume(self, data, limit):
        return round(self.get_pre_day_industry_column_value(data, limit, "avg(trade_volume)"), 6)

    def get_pre_day_avg_close_price_ratio(self, data, limit):
        return round(self.get_pre_day_industry_column_value(data, limit, "avg(avg_close_price_ratio)"), 2)

    def get_pre_day_sum_close_price_ratio(self, data, limit):
        return round(self.get_pre_day_industry_column_value(data, limit, "sum(avg_close_price_ratio)"), 2)

    def get_pre_day_industry_column_value(self, data, limit, column):
        template_key = "pre_day_industry_column_value.sql"
        data["column"] = column
        data["limit"] = limit
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_pre_one_day_totals_stock_amt(self, data, limit):
        return self.get_pre_one_day_industry_column_value(data, limit, "totals_stock_amt")

    def get_pre_one_day_circulation_stock_amt(self, data, limit):
        return self.get_pre_one_day_industry_column_value(data, limit, "circulation_stock_amt")

    def get_pre_one_day_totals_stock_volume(self, data, limit):
        return self.get_pre_one_day_industry_column_value(data, limit, "totals_stock_volume")

    def get_pre_one_day_circulation_stock_volume(self, data, limit):
        return self.get_pre_one_day_industry_column_value(data, limit, "circulation_stock_volume")

    def get_pre_one_day_industry_column_value(self, data, limit, column):
        template_key = "pre_one_day_industry_column_value.sql"
        data["column"] = column
        data["limit"] = limit
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        return path + "/sql/"

    # 两个数相除并保留两个小数点
    def cal_division_round_2(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100
        return round((first_value / second_value), 2)

    # 计算百分比，并进行四舍五入保留2为小数
    def cal_percent_round_2_not_zero(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100

        return round(((first_value - second_value) / second_value) * 100, 2)

    def get_date_str(self, date):
        return DateHandler.get_date_str(date)