#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
from TushareBase import TushareBase


class TushareStockDragonTigerSaleTotalData(TushareBase, object):

    def __init__(self):
        super(TushareStockDragonTigerSaleTotalData, self).__init__()
        self.table_name = "t_tushare_stock_dragon_tiger_sale_total_data"
        print("TushareStockDragonTigerSaleTotalData init")

    def get_stock_dragon_tiger_sale_total_data(self, days):
        data_list = ts.broker_tops(days)
        data_list["days"] = days
        data_list["date"] = self.get_latest_work_day()
        return data_list

    def get_stock_dragon_tiger_sale_total_data_to_db(self, days):
        if not self.is_exist_dragon_tiger_sale_total_data_by_date_and_days(days):
            self.data_to_db_append(self.get_stock_dragon_tiger_sale_total_data(days), self.table_name)

    def delete_stock_dragon_tiger_sale_total_data_by_date_and_days(self, days):
        sql = "delete from " + self.table_name + " where date='" + self.get_latest_work_day() + "' and days= " + str(days)
        self.delete_sql(sql)

    def is_exist_dragon_tiger_sale_total_data_by_date_and_days(self, days):
        sql = "select count(*) as c from " + self.table_name + " " \
              "where date='" + self.get_latest_work_day() + "' and days=" + str(days)
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False


# organ_top = TushareStockDragonTigerSaleTotalData()
# organ_top.get_stock_dragon_tiger_sale_total_data_to_db(5)