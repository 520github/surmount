#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportRandomStockData(ExportBase, object):
    stock_list = [
        # "000622",
        # "603389",
        # "002360",
        # "002680",
        # "002445",
        # "002477",
        #
        # "600053",
        # "000892",
        # "603366",
        # "002676",
        # "600796",
        # "300126",
        # "002871",
        "600122",
    ]

    def __init__(self):
        # self.keywords = "export_stock_price_analysis_data"
        self.keywords = "export_stock_watch_data"
        super(ExportRandomStockData, self).__init__()
        print("ExportRandomStockData init ")

    def get_stock_list(self):
        return self.stock_list


if __name__ == "__main__":
    random = ExportRandomStockData()
    random.export_stock_list_to_excel()