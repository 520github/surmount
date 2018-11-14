#!/usr/bin/python
# -*- coding: UTF-8 -*-

from AlarmBase import AlarmBase


class AlarmTurnoverRateChangeBigMore(AlarmBase, object):

    def __init__(self):
        super(AlarmTurnoverRateChangeBigMore, self).__init__()
        self.trade_date = "2018-11-14"
        self.limit = 5
        self.plate_name = "换手率变大"
        self.plate_start_date = "2018-11-07"
        print("AlarmTurnoverRateChangeBigMore init")

    def alarm_stock_one(self, stock_data):
        code = stock_data["code"]
        stock_data_one = self.get_one_stock_data_by_date(code, self.trade_date)
        if stock_data_one is None:
            return False
        turnover_rate = stock_data_one["turnover_rate"]
        pre5_close_price_ratio = stock_data_one["pre5_close_price_ratio"]
        trade_amt = stock_data_one["trade_amt"]
        large_above_sum_trade_amt_ratio = stock_data_one["large_above_sum_trade_amt_ratio"]

        if large_above_sum_trade_amt_ratio < 45:
            return False

        if trade_amt < 10000000:
            return False

        if pre5_close_price_ratio > 2 and pre5_close_price_ratio < 100:
            return False

        pre_avg_turnover_rate = self.get_pre_day_avg_turnover_rate_value(stock_data)
        if turnover_rate < pre_avg_turnover_rate*3:
            return False

        return True

    def get_pre_day_avg_turnover_rate_value(self, stock_data):
        data = self.get_data_dict_by_stock_data(stock_data)
        data[self.date_compare_key] = "<"
        return self.get_avg_turnover_rate_value_by_trade_statistic_core_data(data)


if __name__ == "__main__":
    st = AlarmTurnoverRateChangeBigMore()
    data_list = st.alarm_stock_list()
    print(len(data_list))
    for data in data_list:
        code = data["code"]
        name = data["name"]
        print(code + "," + name)