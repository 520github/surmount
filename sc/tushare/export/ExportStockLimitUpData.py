#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockLimitUpData(ExportBaseSqlData, object):
    trade_date = "2018-11-14"

    def __init__(self):
        # self.keywords = "export_stock_high_transfer_data"
        self.keywords = "export_stock_limit_up_data"
        super(ExportStockLimitUpData, self).__init__()
        print("ExportStockLimitUpData init ")

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}


if __name__ == "__main__":
    limit_up = ExportStockLimitUpData()
    limit_up.export_sql_data_to_excel()