#!/usr/bin/python
# -*- coding: UTF-8 -*-

from AlarmBase import AlarmBase


class AlarmLowPriceRise(AlarmBase, object):

    def __init__(self):
        super(AlarmLowPriceRise, self).__init__()
        self.trade_date = "2018-11-16"
        self.limit = 5
        self.plate_name = "换手率变大"
        self.plate_start_date = "2018-11-07"
        print("AlarmLowPriceRise init")

    def get_stock_data_list(self):
        sql = "select * from t_sunso_stock_day_trade_statistic_core_data " \
              "where trade_date='" + self.trade_date + "' " \
              "and open_amt > 0 and pre5_close_price_ratio between 5 and 15 "
        return self.select_data_list(sql)

    def alarm_stock_one(self, stock_data):
        code = stock_data["code"]
        pre_stock_data_one = self.get_one_stock_data_by_pre_day(code, self.trade_date, self.limit)
        if pre_stock_data_one is None:
            return False

        pre5_close_price_ratio = pre_stock_data_one["pre5_close_price_ratio"]
        if pre5_close_price_ratio > -10:
            return False

        pre10_close_price_ratio = pre_stock_data_one["pre10_close_price_ratio"]
        if pre10_close_price_ratio > -20:
            return False

        return True


if __name__ == "__main__":
    st = AlarmLowPriceRise()
    st.alarm_stock_list()
