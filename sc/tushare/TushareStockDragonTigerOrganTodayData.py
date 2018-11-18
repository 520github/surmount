#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取最近一个交易日机构席位成交明细统计数据

import tushare as ts
from TushareBase import TushareBase


class TushareStockDragonTigerOrganTodayData(TushareBase, object):

    def __init__(self):
        super(TushareStockDragonTigerOrganTodayData,self).__init__()
        self.table_name = self.t_tushare_stock_dragon_tiger_organ_today_data
        print("TushareStockDragonTigerOrganTodayData init")

    def get_dragon_tiger_organ_today_data(self):
        data = ts.inst_detail(pause=self.pause)
        data["get_date"] = self.get_latest_work_day()
        return data

    def get_dragon_tiger_organ_today_data_to_db(self):
        if not self.is_exist_dragon_tiger_organ_today_data_by_date():
            self.data_to_db_append(self.get_dragon_tiger_organ_today_data(), self.table_name)

    def delete_dragon_tiger_organ_today_data_by_date(self, date):
        sql = "delete from " + self.table_name + " where get_date='" + date + "' "
        self.delete_sql(sql)

    def is_exist_dragon_tiger_organ_today_data_by_date(self):
        sql = "select count(*) as c from " + self.table_name + " where get_date='" + self.get_latest_work_day() + "'"
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False


# organ = TushareStockDragonTigerOrganTodayData()
# organ.get_dragon_tiger_organ_today_data_to_db()