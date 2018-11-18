#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 股票利润分配方案数据

import tushare as ts
from TushareBase import TushareBase


class TushareStockProfitShareData(TushareBase, object):

    def __init__(self):
        super(TushareStockProfitShareData, self).__init__()
        self.table_name = "t_tushare_stock_profit_share_data"
        self.log_info("init TushareStockProfitShareData")

    def get_stock_profit_share_data(self, year=2014, top=100000):
        return ts.profit_data(year, top)

    def get_stock_profit_share_data_to_db(self, year):
        self.data_to_db_append(self.get_stock_profit_share_data(year), self.table_name)


# profit = TushareStockProfitShareData()
# profit.get_stock_profit_share_data_to_db(2018)