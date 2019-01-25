#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockTwoShadeFiveBigTurnover(ExportBaseSqlData, object):

    trade_date = "2019-01-17"
    limit = 5

    def __init__(self):
        self.keywords = "export_stock_two_shade_and_five_big_turnover"
        super(ExportStockTwoShadeFiveBigTurnover, self).__init__()
        print("ExportStockTwoShadeFiveBigTurnover init ")

    def get_sql_data(self, code):
        self.sheet_name = self.limit
        self.sql_data = {"trade_date": self.trade_date, "limit": self.limit}


if __name__ == "__main__":
    one = ExportStockTwoShadeFiveBigTurnover()
    one.export_sql_data_to_excel()