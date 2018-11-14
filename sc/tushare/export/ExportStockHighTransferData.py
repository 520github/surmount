#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockHighTransferData(ExportBaseSqlData, object):
    trade_date = "2018-11-13"
    year = 2018
    quarter = 2
    codes = "('300505','300645','002896','002917','300720')"

    def __init__(self):
        # self.keywords = "export_stock_high_transfer_data"
        self.keywords = "export_stock_high_transfer_data_by_code"
        super(ExportStockHighTransferData, self).__init__()
        self.sheet_name = None
        print("ExportStockHighTransferData init ")

    def get_sql_data(self, code):
        self.sql_data = {"codes": self.codes, "year": self.year,
                         "quarter": self.quarter, "trade_date": self.trade_date}


if __name__ == "__main__":
    high = ExportStockHighTransferData()
    high.export_sql_data_to_excel()