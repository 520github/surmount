#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from TemplateHandler import TemplateHandler
from DateHandler import DateHandler


class StockPlateBase(DbHandler, object):

    def __init__(self):
        super(StockPlateBase, self).__init__()
        print("StockPlateBase init")

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_stock_plate_stock_data_list_by_one_plate(self, plate):
        sql = ""

    def get_plate_index_value(self, template_key, data):
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql_default_zero(sql)

    def get_now_ymd_str(self):
        return DateHandler.get_now_ymd_str()

    def get_tempalte_path(self):
        return "./sql/"

    # 两个数相除并保留两个小数点
    def cal_division_round_2(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100
        return round((first_value / second_value), 2)

