#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockOpenLowCloseHigh(ExportBaseSqlData, object):
    trade_date_key = "trade_date"
    limit_key = "limit"
    trade_date = "2018-11-15"

    def __init__(self):
        self.keywords = "export_stock_open_low_close_high"
        super(ExportStockOpenLowCloseHigh, self).__init__()
        print("ExportStockOpenLowCloseHigh init ")

    def get_export_sql_data_list(self):
        data = []
        limit1_data = self.get_data(1)
        limit2_data = self.get_data(2)
        limit3_data = self.get_data(3)
        limit5_data = self.get_data(5)
        data.append(limit1_data)
        data.append(limit2_data)
        data.append(limit3_data)
        data.append(limit5_data)
        self.data_list = data

    def get_data(self, limit):
        return {self.trade_date_key: self.trade_date, self.limit_key: limit}

    def get_sql_data_custom(self, data):
        self.sql_data = data


if __name__ == "__main__":
    low_high = ExportStockOpenLowCloseHigh()
    low_high.export_sql_data_list_to_excel("limit")