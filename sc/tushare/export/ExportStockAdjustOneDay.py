#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockAdjustOneDay(ExportBaseSqlData, object):

    trade_date = "2019-01-10"

    def __init__(self):
        self.keywords = "export_stock_adjust_one_day"
        super(ExportStockAdjustOneDay, self).__init__()
        print("ExportStockAdjustOneDay init ")

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}


if __name__ == "__main__":
    one = ExportStockAdjustOneDay()
    one.export_sql_data_to_excel()