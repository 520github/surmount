#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 每日龙虎榜列表

from TushareBase import TushareBase
import tushare as ts


class TushareStockDragonTigerTodayData(TushareBase, object):

    def __init__(self):
        super(TushareStockDragonTigerTodayData, self).__init__()
        self.table_name = self.t_tushare_stock_dragon_tiger_today_data
        print("TushareStockDragonTigerTodayData init")

    def get_stock_dragon_tiger_today_data(self, date):
        return ts.top_list(date, pause=self.pause)

    def get_stock_dragon_tiger_today_data_to_db(self, date):
        if not self.is_exist_dragon_tiger_today_data_by_date(date):
            self.data_to_db_append(self.get_stock_dragon_tiger_today_data(date), self.table_name)

    def delete_dragon_tiger_today_data_by_date(self, date):
        sql = "delete from " + self.table_name + " where date='" + date + "' "
        self.delete_sql(sql)

    def is_exist_dragon_tiger_today_data_by_date(self, date):
        sql = "select count(*) as c from " + self.table_name + " where date='" + date + "'"
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False


top = TushareStockDragonTigerTodayData()
# top.get_stock_dragon_tiger_today_data_to_db("2018-10-19")
# top.get_stock_dragon_tiger_today_data_to_db("2018-10-18")
