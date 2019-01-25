#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockFiveShadeNDayBigTurnover(ExportBaseSqlData, object):

    trade_date = "2019-01-03"
    limit = 20

    def __init__(self):
        self.keywords = "export_stock_five_shade_and_n_day_big_turnover"
        super(ExportStockFiveShadeNDayBigTurnover, self).__init__()
        print("ExportStockFiveShadeNDayBigTurnover init ")

    def get_sql_data(self, code):
        self.sheet_name = self.limit
        self.sql_data = {"trade_date": self.trade_date, "limit": self.limit}


if __name__ == "__main__":
    one = ExportStockFiveShadeNDayBigTurnover()
    one.export_sql_data_to_excel()