#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportStockAvgPriceData(ExportBase, object):
    keywords = "export_stock_avg_price_data"
    start_trade_date = "2018-10-30"
    end_trade_date = "2018-11-08"
    stock_list = ["002617", "002668", "603386"]

    def __init__(self):
        super(ExportStockAvgPriceData, self).__init__()
        self.is_alone_file = False
        self.sql_template_key = self.keywords + ".sql"
        print("ExportStockAvgPriceData init ")

    def get_stock_list(self):
        # sql = "select code from t_sunso_stock_plate_stock " \
        #       "where plate_name='大额资金净流入和短期内跌幅较大' and plate_start_date='2018-10-26' " \
        #     # "and code in ('600128','002054','600235','600462','600689','600783','002328')"
        # return self.get_stock_list_by_sql(sql)
        return self.stock_list

    def get_sql_data(self, code):
        self.sql_data = {"code": code, "start_trade_date": self.start_trade_date, "end_trade_date": self.end_trade_date}


if __name__ == "__main__":
    avg_price = ExportStockAvgPriceData()
    avg_price.export_stock_list_to_excel()