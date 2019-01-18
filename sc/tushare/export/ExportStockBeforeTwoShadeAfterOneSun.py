#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockBeforeTwoShadeAfterOneSun(ExportBaseSqlData, object):

    trade_date = "2019-01-15"

    def __init__(self):
        self.keywords = "export_stock_before_two_shade_after_one_sun"
        super(ExportStockBeforeTwoShadeAfterOneSun, self).__init__()
        print("ExportStockBeforeTwoShadeAfterOneSun init ")

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}


if __name__ == "__main__":
    one = ExportStockBeforeTwoShadeAfterOneSun()
    one.export_sql_data_to_excel()