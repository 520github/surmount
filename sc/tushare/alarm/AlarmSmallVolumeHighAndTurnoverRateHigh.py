#!/usr/bin/python
# -*- coding: UTF-8 -*-

from AlarmBase import AlarmBase


class AlarmSmallVolumeHighAndTurnoverRateHigh(AlarmBase, object):

    def __init__(self):
        super(AlarmSmallVolumeHighAndTurnoverRateHigh, self).__init__()
        self.trade_date = "2018-11-07"
        self.limit = 5
        print("AlarmSmallVolumeHighAndTurnoverRateHigh init")

    def alarm_stock_one(self, stock_data):
        pre_avg_turnover_rate = self.get_pre_day_avg_turnover_rate_value(stock_data)
        if pre_avg_turnover_rate < 15 or pre_avg_turnover_rate > 20:
            return False

        pre_avg_small_sum_trade_amt_ratio = self.get_pre_day_avg_small_sum_trade_amt_ratio(stock_data)
        if pre_avg_small_sum_trade_amt_ratio < 70:
            return False

        return True

    def get_pre_day_avg_turnover_rate_value(self, stock_data):
        data = self.get_data_dict_by_stock_data(stock_data)
        return self.get_avg_turnover_rate_value_by_trade_statistic_core_data(data)

    def get_pre_day_avg_small_sum_trade_amt_ratio(self, stock_data):
        data = self.get_data_dict_by_stock_data(stock_data)
        return self.get_avg_small_sum_trade_amt_ratio_by_trade_statistic_volume_data(data)


if __name__ == "__main__":
    st = AlarmSmallVolumeHighAndTurnoverRateHigh()
    data_list = st.alarm_stock_list()
    print(len(data_list))
    for data in data_list:
        code = data["code"]
        name = data["name"]
        print(code + "," + name)