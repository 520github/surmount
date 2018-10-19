#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 每日龙虎榜列表

from TushareBase import TushareBase
import tushare as ts


class TushareStockTopListData(TushareBase, object):

    def __init__(self):
        super(TushareStockTopListData, self).__init__()
        self.table_name = "t_tushare_stock_top_list_data"
        print("TushareStockTopListData init")

    def get_stock_top_list_data(self, date):
        return ts.top_list(date, pause=self.pause)

    def get_stock_top_list_data_to_db(self, date):
        self.data_to_db_append(self.get_stock_top_list_data(date), self.table_name)


top = TushareStockTopListData()
top.get_stock_top_list_data_to_db("2018-10-17")
