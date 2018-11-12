#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportIndustryStockData(ExportBase, object):
    keywords = "export_industry_stock_data"
    trade_date = "2018-11-08"
    limit = 6
    stock_list = ["600128", "600235", "002054", "002575", "600689", "600462"]

    def __init__(self):
        super(ExportIndustryStockData, self).__init__()
        self.is_alone_file = False
        self.sql_template_key = self.keywords + ".sql"
        print("ExportIndustryStockData init ")

    def get_stock_list(self):
        return self.stock_list

    def get_sql_data(self, code):
        self.sql_data = {"code": code, "trade_date": self.trade_date, "limit": self.limit}


if __name__ == "__main__":
    watch = ExportIndustryStockData()
    watch.export_stock_list_to_excel()