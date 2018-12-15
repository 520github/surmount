#!/usr/bin/python
# -*- coding: UTF-8 -*-
from StatisticBase import StatisticBase


class StatisticRangeAvgData(StatisticBase, object):
    limit_2 = 2
    limit_3 = 3
    limit_5 = 5
    limit_10 = 10
    limit_20 = 20
    limit_30 = 30
    limit_60 = 60

    is_delete_before_insert = True

    def __init__(self):
        super(StatisticRangeAvgData, self).__init__()
        print("StatisticRangeAvgData init")

    def handle_one_stock_data(self, data):
        pre2_avg_close_pre_close_diff_amt_ratio = self.get_pre_avg_close_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_avg_open_pre_close_diff_amt_ratio = self.get_pre_avg_open_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_avg_low_pre_close_diff_amt_ratio = self.get_pre_avg_low_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_avg_high_pre_close_diff_amt_ratio = self.get_pre_avg_high_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_avg_low_high_diff_amt_ratio = self.get_pre_avg_low_high_diff_amt_ratio(data, self.limit_2)
        data["pre2_avg_close_pre_close_diff_amt_ratio"] = pre2_avg_close_pre_close_diff_amt_ratio
        data["pre2_avg_open_pre_close_diff_amt_ratio"] = pre2_avg_open_pre_close_diff_amt_ratio
        data["pre2_avg_low_pre_close_diff_amt_ratio"] = pre2_avg_low_pre_close_diff_amt_ratio
        data["pre2_avg_high_pre_close_diff_amt_ratio"] = pre2_avg_high_pre_close_diff_amt_ratio
        data["pre2_avg_low_high_diff_amt_ratio"] = pre2_avg_low_high_diff_amt_ratio

        pre2_plus_count_close_pre_close_diff_amt_ratio = self.get_pre_plus_count_close_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_plus_count_open_pre_close_diff_amt_ratio = self.get_pre_plus_count_open_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_plus_count_low_pre_close_diff_amt_ratio = self.get_pre_plus_count_low_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_plus_count_high_pre_close_diff_amt_ratio = self.get_pre_plus_count_high_pre_close_diff_amt_ratio(data, self.limit_2)
        pre2_plus_count_low_high_diff_amt_ratio = self.get_pre_plus_count_low_high_diff_amt_ratio(data, self.limit_2)
        data["pre2_plus_count_close_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre2(pre2_plus_count_close_pre_close_diff_amt_ratio)
        data["pre2_plus_count_open_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre2(pre2_plus_count_open_pre_close_diff_amt_ratio)
        data["pre2_plus_count_low_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre2(pre2_plus_count_low_pre_close_diff_amt_ratio)
        data["pre2_plus_count_high_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre2(pre2_plus_count_high_pre_close_diff_amt_ratio)
        data["pre2_plus_count_low_high_diff_amt_ratio"] = self.cal_percent_by_pre2(pre2_plus_count_low_high_diff_amt_ratio)

        pre3_avg_close_pre_close_diff_amt_ratio = self.get_pre_avg_close_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_avg_open_pre_close_diff_amt_ratio = self.get_pre_avg_open_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_avg_low_pre_close_diff_amt_ratio = self.get_pre_avg_low_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_avg_high_pre_close_diff_amt_ratio = self.get_pre_avg_high_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_avg_low_high_diff_amt_ratio = self.get_pre_avg_low_high_diff_amt_ratio(data, self.limit_3)
        data["pre3_avg_close_pre_close_diff_amt_ratio"] = pre3_avg_close_pre_close_diff_amt_ratio
        data["pre3_avg_open_pre_close_diff_amt_ratio"] = pre3_avg_open_pre_close_diff_amt_ratio
        data["pre3_avg_low_pre_close_diff_amt_ratio"] = pre3_avg_low_pre_close_diff_amt_ratio
        data["pre3_avg_high_pre_close_diff_amt_ratio"] = pre3_avg_high_pre_close_diff_amt_ratio
        data["pre3_avg_low_high_diff_amt_ratio"] = pre3_avg_low_high_diff_amt_ratio

        pre3_plus_count_close_pre_close_diff_amt_ratio = self.get_pre_plus_count_close_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_plus_count_open_pre_close_diff_amt_ratio = self.get_pre_plus_count_open_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_plus_count_low_pre_close_diff_amt_ratio = self.get_pre_plus_count_low_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_plus_count_high_pre_close_diff_amt_ratio = self.get_pre_plus_count_high_pre_close_diff_amt_ratio(data, self.limit_3)
        pre3_plus_count_low_high_diff_amt_ratio = self.get_pre_plus_count_low_high_diff_amt_ratio(data, self.limit_3)
        data["pre3_plus_count_close_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre3(pre3_plus_count_close_pre_close_diff_amt_ratio)
        data["pre3_plus_count_open_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre3(pre3_plus_count_open_pre_close_diff_amt_ratio)
        data["pre3_plus_count_low_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre3(pre3_plus_count_low_pre_close_diff_amt_ratio)
        data["pre3_plus_count_high_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre3(pre3_plus_count_high_pre_close_diff_amt_ratio)
        data["pre3_plus_count_low_high_diff_amt_ratio"] = self.cal_percent_by_pre3(pre3_plus_count_low_high_diff_amt_ratio)

        pre5_avg_close_pre_close_diff_amt_ratio = self.get_pre_avg_close_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_avg_open_pre_close_diff_amt_ratio = self.get_pre_avg_open_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_avg_low_pre_close_diff_amt_ratio = self.get_pre_avg_low_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_avg_high_pre_close_diff_amt_ratio = self.get_pre_avg_high_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_avg_low_high_diff_amt_ratio = self.get_pre_avg_low_high_diff_amt_ratio(data, self.limit_5)
        data["pre5_avg_close_pre_close_diff_amt_ratio"] = pre5_avg_close_pre_close_diff_amt_ratio
        data["pre5_avg_open_pre_close_diff_amt_ratio"] = pre5_avg_open_pre_close_diff_amt_ratio
        data["pre5_avg_low_pre_close_diff_amt_ratio"] = pre5_avg_low_pre_close_diff_amt_ratio
        data["pre5_avg_high_pre_close_diff_amt_ratio"] = pre5_avg_high_pre_close_diff_amt_ratio
        data["pre5_avg_low_high_diff_amt_ratio"] = pre5_avg_low_high_diff_amt_ratio

        pre5_plus_count_close_pre_close_diff_amt_ratio = self.get_pre_plus_count_close_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_plus_count_open_pre_close_diff_amt_ratio = self.get_pre_plus_count_open_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_plus_count_low_pre_close_diff_amt_ratio = self.get_pre_plus_count_low_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_plus_count_high_pre_close_diff_amt_ratio = self.get_pre_plus_count_high_pre_close_diff_amt_ratio(data, self.limit_5)
        pre5_plus_count_low_high_diff_amt_ratio = self.get_pre_plus_count_low_high_diff_amt_ratio(data, self.limit_5)
        data["pre5_plus_count_close_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre5(pre5_plus_count_close_pre_close_diff_amt_ratio)
        data["pre5_plus_count_open_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre5(pre5_plus_count_open_pre_close_diff_amt_ratio)
        data["pre5_plus_count_low_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre5(pre5_plus_count_low_pre_close_diff_amt_ratio)
        data["pre5_plus_count_high_pre_close_diff_amt_ratio"] = self.cal_percent_by_pre5(pre5_plus_count_high_pre_close_diff_amt_ratio)
        data["pre5_plus_count_low_high_diff_amt_ratio"] = self.cal_percent_by_pre5(pre5_plus_count_low_high_diff_amt_ratio)

        data["nearly5_avg_close_price"] = self.get_nearly_avg_close_pre_close_diff_amt_ratio(data, self.limit_5)
        data["nearly10_avg_close_price"] = self.get_nearly_avg_close_pre_close_diff_amt_ratio(data, self.limit_10)
        data["nearly20_avg_close_price"] = self.get_nearly_avg_close_pre_close_diff_amt_ratio(data, self.limit_20)
        data["nearly30_avg_close_price"] = self.get_nearly_avg_close_pre_close_diff_amt_ratio(data, self.limit_30)
        data["nearly60_avg_close_price"] = self.get_nearly_avg_close_pre_close_diff_amt_ratio(data, self.limit_60)

        self.get_continue_above_avg_day_data(data)

        if self.is_delete_before_insert:
            self.delete_before_insert(data)

        template_key = "insert_t_sunso_stock_day_trade_statistic_range_avg_data.sql"
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def delete_before_insert(self, data):
        sql = "delete from t_sunso_stock_day_trade_statistic_range_avg_data " \
              "where trade_date='" + data["trade_date"] + "' " \
              "and code='" + data["code"] + "' "
        self.delete_sql(sql)

    def cal_percent_by_pre5(self, value):
        return self.cal_percent_round_2(value, self.limit_5)

    def cal_percent_by_pre3(self, value):
        return self.cal_percent_round_2(value, self.limit_3)

    def cal_percent_by_pre2(self, value):
        return self.cal_percent_round_2(value, self.limit_2)


if __name__ == "__main__":
    range = StatisticRangeAvgData()
    range.load_statistic_data()