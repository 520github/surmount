#!/usr/bin/python
# -*- coding: UTF-8 -*-

from AlarmBase import AlarmBase


class AlarmTodayFirstUpAfterDownAndYesterdayUpLimit(AlarmBase, object):

    def __init__(self):
        super(AlarmTodayFirstUpAfterDownAndYesterdayUpLimit, self).__init__()
        self.trade_date = "2018-11-22"
        self.limit = 1
        self.plate_name = "昨日涨停今日先涨后跌"
        self.plate_start_date = "2018-11-22"
        self.alarm_stock_data_list = []
        print("AlarmTodayFirstUpAfterDownAndYesterdayUpLimit init")

    def get_stock_data_list(self):
        limit_value = "10"
        sql = "select * from t_sunso_stock_day_trade_statistic_core_data " \
              "where trade_date='" + self.trade_date + "' " \
              "and open_amt > 0 " \
              "and close_pre_close_diff_amt_ratio < 0 " \
              "and open_pre_close_diff_amt_ratio between 0 and  " + limit_value + " "\
              "and high_pre_close_diff_amt_ratio - open_pre_close_diff_amt_ratio < " + limit_value + " " \
              "and high_pre_close_diff_amt_ratio > open_pre_close_diff_amt_ratio " \
              "and pre1_avg_turnover_rate_ratio > 1.2 " \
              "order by low_high_diff_amt_ratio desc "
              #
              # "and open_pre_close_diff_amt_ratio - close_pre_close_diff_amt_ratio < 5 " \
        return self.select_data_list(sql)

    def alarm_stock_one(self, stock_data):
        code = stock_data["code"]
        pre_stock_data_one = self.get_one_stock_data_by_pre_day(code, self.trade_date, self.limit)
        if pre_stock_data_one is None:
            return False

        up_limit_type = pre_stock_data_one["up_limit_type"]
        if up_limit_type <= 0:
            return False

        if up_limit_type >= 30:
            return False

        low_high_diff_amt_ratio = pre_stock_data_one["low_high_diff_amt_ratio"]
        if low_high_diff_amt_ratio > 10:
            return False

        return True


if __name__ == "__main__":
    ty = AlarmTodayFirstUpAfterDownAndYesterdayUpLimit()
    ty.alarm_stock_list()
