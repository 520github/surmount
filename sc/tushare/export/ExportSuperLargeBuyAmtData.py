#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportSuperLargeBuyAmtData(ExportBase, object):
    keywords = "export_super_large_buy_amt_data"
    # stock_list = ["002668", "600122", "002680"]
    stock_list = ["000669", "603031"]

    def __init__(self):
        super(ExportSuperLargeBuyAmtData, self).__init__()
        self.is_alone_file = False
        self.sql_template_key = self.keywords + ".sql"
        print("ExportSuperLargeBuyAmtData init ")

    def get_stock_list(self):
        return self.stock_list


if __name__ == "__main__":
    super_large = ExportSuperLargeBuyAmtData()
    super_large.export_stock_list_to_excel()