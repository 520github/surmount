#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取近5、10、30、60日个股上榜统计数据
# 包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数

from TushareBase import TushareBase
import tushare as ts

class TushareStockDragonTigerTotalData(TushareBase, object):

    def __init__(self):
        super(TushareStockDragonTigerTotalData, self).__init__()
        self.table_name = self.t_tushare_stock_dragon_tiger_total_data
        print("TushareStockDragonTigerTotalData init ")

    def get_tushare_stock_dragon_tiger_total_data(self, days):
        data = ts.cap_tops(days)
        if data is None or len(data) <1:
            return None
        data["days"] = days
        data["date"] = self.get_latest_work_day()
        return data

    def get_tushare_stock_dragon_tiger_total_data_to_db(self, days):
        if not self.is_exist_stock_dragon_tiger_total_data_by_days_and_date(days):
            self.data_to_db_append(self.get_tushare_stock_dragon_tiger_total_data(days), self.table_name)

    def delete_stock_dragon_tiger_total_data_by_days_and_date(self, days):
        sql = "delete from " + self.table_name + " where date='" + self.get_latest_work_day() + "' and days= " + str(days)
        self.delete_sql(sql)

    def is_exist_stock_dragon_tiger_total_data_by_days_and_date(self, days):
        sql = "select count(*) as c from " + self.table_name + "" \
              " where date='" + self.get_latest_work_day() + "' and days= " + str(days)
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False

# stock_top = TushareStockDragonTigerTotalData()
# stock_top.get_tushare_stock_dragon_tiger_total_data_to_db(5)
# stock_top.get_tushare_stock_dragon_tiger_total_data_to_db(10)
# stock_top.get_tushare_stock_dragon_tiger_total_data_to_db(30)
# stock_top.get_tushare_stock_dragon_tiger_total_data_to_db(60)