#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockFourOneSun(ExportBaseSqlData, object):

    trade_date = "2019-01-17"

    def __init__(self):
        self.keywords = "export_stock_four_sun"
        super(ExportStockFourOneSun, self).__init__()
        print("ExportStockFourOneSun init ")

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}


if __name__ == "__main__":
    one = ExportStockFourOneSun()
    one.export_sql_data_to_excel()