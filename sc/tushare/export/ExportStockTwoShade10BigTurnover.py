#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockTwoShade10BigTurnover(ExportBaseSqlData, object):

    trade_date = "2019-01-17"

    def __init__(self):
        self.keywords = "export_stock_two_shade_and_10_big_turnover"
        super(ExportStockTwoShade10BigTurnover, self).__init__()
        print("ExportStockTwoShade10BigTurnover init ")

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}


if __name__ == "__main__":
    one = ExportStockTwoShade10BigTurnover()
    one.export_sql_data_to_excel()