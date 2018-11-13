#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportStockPriceReference(ExportBase, object):
    turnover_rate = "换手率变动"
    overfall = "超跌与大资金"
    large_buy = "超大资金"

    stock_list = {
        "300342": turnover_rate, "601118": turnover_rate,
        "002739": turnover_rate, "002602": turnover_rate,
        "002656": turnover_rate, "002665": turnover_rate,

        "002668": overfall, "002617": overfall,
        "600122": overfall, "600226": overfall, "603386": overfall,

        "600525": large_buy, "600522": large_buy, "002195": large_buy


    }

    def __init__(self):
        self.keywords = "export_stock_price_reference"
        super(ExportStockPriceReference, self).__init__()
        print("ExportStockPriceReference init ")

    def get_stock_list(self):
        list = []
        for key in self.stock_list.keys():
            list.append(key)
        return list

    def get_sql_data(self, code):
        type_name = self.stock_list.get(code)
        self.sql_data = {"code": code, "type_name": type_name}


if __name__ == "__main__":
    price = ExportStockPriceReference()
    price.export_stock_list_to_excel()