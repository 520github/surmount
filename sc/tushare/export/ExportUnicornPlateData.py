#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportUnicornPlateData(ExportBase, object):
    keywords = "export_unicorn_plate_data"

    def __init__(self):
        super(ExportUnicornPlateData, self).__init__()
        self.is_alone_file = False
        self.sql_template_key = self.keywords + ".sql"
        print("ExportSuperLargeBuyAmtData init ")

    def get_stock_list(self):
        sql = "select code from t_sunso_stock_plate_stock " \
              "where plate_name='创投板块' and plate_start_date='2018-11-02' " \
              "and code in ('600128','002054','600235','600462','600689','600783','002328')"
        data_list = self.select_data_list(sql)
        if data_list is None or len(data_list) < 1:
            return None
        stock_list = []
        for data in data_list:
            stock_list.append(data["code"])
        return stock_list

    def get_sql_data(self, code):
        self.sql_data = {"code": code, "plate_name": "创投板块", "plate_start_date": "2018-11-02"}


if __name__ == "__main__":
    unicorn = ExportUnicornPlateData()
    unicorn.export_stock_list_to_excel()