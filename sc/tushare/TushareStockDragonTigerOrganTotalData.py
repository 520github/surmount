#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
from TushareBase import TushareBase
import traceback

class TushareStockDragonTigerOrganTotalData(TushareBase, object):

    def __init__(self):
        super(TushareStockDragonTigerOrganTotalData, self).__init__()
        self.table_name = self.t_tushare_stock_dragon_tiger_organ_total_data
        print("TushareStockDragonTigerOrganTotalData init")

    def get_tushare_stock_dragon_tiger_organ_total_data(self, days):
        try:
            data = ts.inst_tops(days)
            if data is None:
                return data
            data["days"] = days
            data["date"] = self.get_latest_work_day()
            return data
        except Exception, e:
            print e
            print(traceback.format_exc())
            return None

    def get_tushare_stock_dragon_tiger_organ_total_data_to_db(self, days):
        if not self.is_exist_dragon_tiger_organ_total_data_by_date_and_days(days):
            self.data_to_db_append(self.get_tushare_stock_dragon_tiger_organ_total_data(days), self.table_name)

    def delete_stock_dragon_tiger_organ_total_data_by_date_and_days(self, days):
        sql = "delete from " + self.table_name + " where date='" + self.get_latest_work_day() + "' and days= " + str(days)
        self.delete_sql(sql)

    def is_exist_dragon_tiger_organ_total_data_by_date_and_days(self, days):
        sql = "select count(*) as c from " + self.table_name + " " \
              "where date='" + self.get_latest_work_day() + "' and days=" + str(days)
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False


# organ_seat = TushareStockDragonTigerOrganTotalData()
# organ_seat.get_tushare_stock_dragon_tiger_organ_total_data_to_db(5)