#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
from TushareBase import TushareBase


class TushareStockOrganTopData(TushareBase, object):

    def __init__(self):
        super(TushareStockOrganTopData, self).__init__()
        self.table_name = "t_tushare_stock_organ_top_data"
        print("TushareStockOrganTopData init")

    def get_stock_organ_top_data(self, days):
        data_list = ts.broker_tops(days)
        data_list["days"] = days
        return data_list

    def get_stock_organ_top_data_to_db(self, days):
        self.data_to_db_append(self.get_stock_organ_top_data(days), self.table_name)


organ_top = TushareStockOrganTopData()
organ_top.get_stock_organ_top_data_to_db(5)