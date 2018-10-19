#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import TushareBase
import tushare as ts
from TushareBase import TushareBase


class TushareStockHistData(TushareBase, object):

    def __init__(self):
        super(TushareStockHistData, self).__init__()
        print("hist data")

    def get_one_stock_all_hist_data(self, stock_code):
        data = ts.get_hist_data(stock_code)
        data["code"] = stock_code
        return data;

    def get_one_stock_all_hist_data_to_db(self, stock_code):
        self.data_to_db_append(self.get_one_stock_all_hist_data(stock_code), "t_stock_hist_data")

    def get_one_stock_date_hist_data(self, stock_code, start_date, end_date):
        if end_date is None:
            end_date = self.get_now_ymd()
        data = ts.get_hist_data(stock_code, start_date, end_date)
        data["code"] = stock_code
        return data

    def get_one_stock_date_hist_data_to_db(self, stock_code, start_date=None, end_date=None):
        self.data_to_db_append(self.get_one_stock_date_hist_data(stock_code, start_date, end_date), "t_stock_hist_data")


hist_data = TushareStockHistData()
#realtime.get_one_stock_date_hist_data_to_db("002530", "2018-05-26")
hist_data.get_one_stock_all_hist_data_to_db("002530")
