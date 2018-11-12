#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportPlateBase(ExportBase, object):
    plate_name = "创投板块"
    plate_start_date = "2018-11-02"

    def __init__(self):
        super(ExportPlateBase, self).__init__()
        self.is_alone_file = False
        print("ExportPlateBase init ")

    def get_stock_list(self):
        sql = self.get_plate_sql()
        data_list = self.select_data_list(sql)
        if data_list is None or len(data_list) < 1:
            return None
        stock_list = []
        for data in data_list:
            stock_list.append(data["code"])
        return stock_list

    def get_plate_sql(self):
        sql = "select code from t_sunso_stock_plate_stock " \
              "where plate_name='" + self.plate_name + "' and plate_start_date='"+self.plate_start_date+"' " \
              "order by join_date desc "
              # "and code in ('600128','002054','600235','600462','600689','600783','002328')"

        return sql

    def get_sql_data(self, code):
        self.sql_data = {"code": code, "plate_name": self.plate_name, "plate_start_date": self.plate_start_date}