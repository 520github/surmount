#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
from TushareBase import TushareBase


class TushareStockOrganTradeData(TushareBase, object):

    def __init__(self):
        super(TushareStockOrganTradeData,self).__init__()
        self.table_name = "t_tushare_stock_organ_trade_data"
        print("TushareStockOrganTradeData init")

    def get_organ_trade_data(self):
        return ts.inst_detail(pause=self.pause)

    def get_organ_trade_data_to_db(self):
        self.data_to_db_append(self.get_organ_trade_data(), self.table_name)


organ = TushareStockOrganTradeData()
organ.get_organ_trade_data_to_db()