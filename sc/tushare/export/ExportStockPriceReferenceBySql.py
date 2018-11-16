#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportStockPriceReferenceBySql(ExportBase, object):

    def __init__(self):
        self.keywords = "export_stock_price_reference"
        super(ExportStockPriceReferenceBySql, self).__init__()
        print("ExportStockPriceReferenceBySql init ")

    def get_stock_list(self):
        sql_data = {"trade_date": "2018-11-15", "limit": 1}
        sql = self.get_sql_by_template("export_stock_open_low_close_high.sql", sql_data)
        data_list = self.get_stock_list_by_sql(sql)
        return data_list

    def get_sql_data(self, code):
        type_name = "低开走高"
        self.sql_data = {"code": code, "type_name": type_name}


if __name__ == "__main__":
    price = ExportStockPriceReferenceBySql()
    price.export_stock_list_to_excel()