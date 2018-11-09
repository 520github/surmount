#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase


class ExportLargeBuyAmtAndOverfall(ExportBase, object):
    keywords = "export_large_buy_amt_and_overfall_data"
    stock_list = ["002668", "600122", "002680"]

    def __init__(self):
        super(ExportLargeBuyAmtAndOverfall, self).__init__()
        self.is_alone_file = False
        self.sql_template_key = self.keywords + ".sql"
        print("ExportLargeBuyAmtAndOverfall init ")

    def get_stock_list(self):
        sql = "select code from t_sunso_stock_plate_stock " \
              "where plate_name='大额资金净流入和短期内跌幅较大' and plate_start_date='2018-10-26' " \
              # "and code in ('600128','002054','600235','600462','600689','600783','002328')"
        return self.get_stock_list_by_sql(sql)


if __name__ == "__main__":
    large_overfall = ExportLargeBuyAmtAndOverfall()
    large_overfall.export_stock_list_to_excel()