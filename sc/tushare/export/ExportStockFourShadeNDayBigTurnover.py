#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockFourShadeNDayBigTurnover(ExportBaseSqlData, object):

    trade_date = "2019-01-14"
    limit = 20

    def __init__(self):
        self.keywords = "export_stock_four_shade_and_n_day_big_turnover"
        super(ExportStockFourShadeNDayBigTurnover, self).__init__()
        print("ExportStockFiveShadeNDayBigTurnover init ")

    def get_sql_data(self, code):
        self.sheet_name = self.limit
        self.sql_data = {"trade_date": self.trade_date, "limit": self.limit}


if __name__ == "__main__":
    one = ExportStockFourShadeNDayBigTurnover()
    one.export_sql_data_to_excel()