#!/usr/bin/python
# -*- coding: UTF-8 -*-

from TushareBase import TushareBase


class SunsoDayTradeStatisticVolumeData(TushareBase, object):
    large_above_avg_trade_price = "large_above_avg_trade_price"
    super_avg_trade_price = "super_avg_trade_price"
    large_avg_trade_price = "large_avg_trade_price"
    medium_before_avg_trade_price = "medium_before_avg_trade_price"
    medium_after_avg_trade_price = "medium_after_avg_trade_price"
    small_avg_trade_price = "small_avg_trade_price"
    large_above_buy_avg_trade_price = "large_above_buy_avg_trade_price"
    super_buy_avg_trade_price = "super_buy_avg_trade_price"
    large_buy_avg_trade_price = "large_buy_avg_trade_price"
    medium_before_buy_avg_trade_price = "medium_before_buy_avg_trade_price"
    medium_after_buy_avg_trade_price = "medium_after_buy_avg_trade_price"
    small_buy_avg_trade_price = "small_buy_avg_trade_price"
    large_above_sell_avg_trade_price = "large_above_sell_avg_trade_price"
    super_sell_avg_trade_price = "super_sell_avg_trade_price"
    large_sell_avg_trade_price = "large_sell_avg_trade_price"
    medium_before_sell_avg_trade_price = "medium_before_sell_avg_trade_price"
    medium_after_sell_avg_trade_price = "medium_after_sell_avg_trade_price"
    small_sell_avg_trade_price = "small_sell_avg_trade_price"
    all_buy_avg_trade_price = "all_buy_avg_trade_price"
    all_sell_avg_trade_price = "all_sell_avg_trade_price"

    def __init__(self):
        super(SunsoDayTradeStatisticVolumeData, self).__init__()
        self.table_name = self.t_sunso_stock_day_trade_statistic_volume_data
        print("SunsoDayTradeStatisticVolumeData init")

    def init_day_trade_statistic_volume_data(self, data):
        stock_code = data["code"]
        date = data["trade_date"]
        close_amt = data["close_amt"]
        trade_count = data["trade_count"]

        sum_trade_amt = self.get_stock_amt_by_size(stock_code, date, None)
        medium_before_sum_trade_amt = self.get_stock_amt_by_size(stock_code, date, self.volume_medium_before)
        medium_after_sum_trade_amt = self.get_stock_amt_by_size(stock_code, date, self.volume_medium_after)
        data["medium_before_sum_trade_amt_ratio"] = self.cal_percent_round_2(medium_before_sum_trade_amt, sum_trade_amt)
        data["medium_after_sum_trade_amt_ratio"] = self.cal_percent_round_2(medium_after_sum_trade_amt, sum_trade_amt)

        sum_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, None, self.outside_dish)
        data["sum_buy_trade_amt_ratio"] = self.cal_percent_round_2(sum_buy_trade_amt, sum_trade_amt)
        super_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.super_volume, self.outside_dish)
        data["super_buy_trade_amt_ratio"] = self.cal_percent_round_2(super_buy_trade_amt, sum_trade_amt)
        large_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.max_volume, self.outside_dish)
        data["large_buy_trade_amt_ratio"] = self.cal_percent_round_2(large_buy_trade_amt, sum_trade_amt)
        medium_before_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.volume_medium_before, self.outside_dish)
        data["medium_before_buy_trade_amt_ratio"] = self.cal_percent_round_2(medium_before_buy_trade_amt, sum_trade_amt)
        medium_after_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.volume_medium_after, self.outside_dish)
        data["medium_after_buy_trade_amt_ratio"] = self.cal_percent_round_2(medium_after_buy_trade_amt, sum_trade_amt)
        small_buy_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.min_volume, self.outside_dish)

        sum_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, None, self.inside_dish)
        data["sum_sell_trade_amt_ratio"] = self.cal_percent_round_2(sum_sell_trade_amt, sum_trade_amt)
        super_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.super_volume, self.inside_dish)
        data["super_sell_trade_amt_ratio"] = self.cal_percent_round_2(super_sell_trade_amt, sum_trade_amt)
        large_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.max_volume, self.inside_dish)
        data["large_sell_trade_amt_ratio"] = self.cal_percent_round_2(large_sell_trade_amt, sum_trade_amt)
        medium_before_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.volume_medium_before, self.inside_dish)
        data["medium_before_sell_trade_amt_ratio"] = self.cal_percent_round_2(medium_before_sell_trade_amt, sum_trade_amt)
        medium_after_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.volume_medium_after, self.inside_dish)
        data["medium_after_sell_trade_amt_ratio"] = self.cal_percent_round_2(medium_after_sell_trade_amt, sum_trade_amt)
        small_sell_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.min_volume, self.inside_dish)

        data["sum_trade_amt"] = self.get_hundred_million_amt(sum_trade_amt)
        data["large_above_buy_trade_amt"] = self.get_hundred_million_amt(super_buy_trade_amt + large_buy_trade_amt)
        data["super_buy_trade_amt"] = self.get_hundred_million_amt(super_buy_trade_amt)
        data["large_buy_trade_amt"] = self.get_hundred_million_amt(large_buy_trade_amt)
        data["medium_after_buy_trade_amt"] = self.get_hundred_million_amt(medium_after_buy_trade_amt)
        data["medium_before_buy_trade_amt"] = self.get_hundred_million_amt(medium_before_buy_trade_amt)
        data["small_buy_trade_amt"] = self.get_hundred_million_amt(small_buy_trade_amt)

        data["large_above_sell_trade_amt"] = self.get_hundred_million_amt(super_sell_trade_amt + large_sell_trade_amt)
        data["super_sell_trade_amt"] = self.get_hundred_million_amt(super_sell_trade_amt)
        data["large_sell_trade_amt"] = self.get_hundred_million_amt(large_sell_trade_amt)
        data["medium_after_sell_trade_amt"] = self.get_hundred_million_amt(medium_after_sell_trade_amt)
        data["medium_before_sell_trade_amt"] = self.get_hundred_million_amt(medium_before_sell_trade_amt)
        data["small_sell_trade_amt"] = self.get_hundred_million_amt(small_sell_trade_amt)

        large_above_bs_diff_trade_amt = data["large_above_day1_bs_diff_trade_amt"]
        large_above_day3_bs_diff_trade_amt = data["large_above_day3_bs_diff_trade_amt"]
        large_above_day5_bs_diff_trade_amt = data["large_above_day5_bs_diff_trade_amt"]
        data["large_above_day1_bs_diff_trade_amt_total_ratio"] = self.cal_percent_round_2(large_above_bs_diff_trade_amt, sum_trade_amt)
        data["large_above_day3_bs_diff_trade_amt_total_ratio"] = self.cal_percent_round_2(large_above_day3_bs_diff_trade_amt, sum_trade_amt)
        data["large_above_day5_bs_diff_trade_amt_total_ratio"] = self.cal_percent_round_2(large_above_day5_bs_diff_trade_amt, sum_trade_amt)

        data["large_above_day1_bs_diff_trade_amt_rise_ratio"] = round(data["large_above_day1_bs_diff_trade_amt_ratio"], 2)
        data["large_above_day3_bs_diff_trade_amt_rise_ratio"] = round(data["large_above_day3_bs_diff_trade_amt_ratio"], 2)
        data["large_above_day5_bs_diff_trade_amt_rise_ratio"] = round(data["large_above_day5_bs_diff_trade_amt_ratio"], 2)

        all_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, None, self.outside_dish)
        all_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, None, self.inside_dish)
        pre3_all_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.all_buy_avg_trade_price, 3)
        pre3_all_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.all_sell_avg_trade_price, 3)
        pre5_all_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.all_buy_avg_trade_price, 5)
        pre5_all_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.all_sell_avg_trade_price, 5)
        data["all_buy_avg_trade_price"] = all_buy_avg_trade_price
        data["all_sell_avg_trade_price"] = all_sell_avg_trade_price
        data["pre3_all_buy_avg_trade_price"] = pre3_all_buy_avg_trade_price
        data["pre3_all_sell_avg_trade_price"] = pre3_all_sell_avg_trade_price
        data["pre5_all_buy_avg_trade_price"] = pre5_all_buy_avg_trade_price
        data["pre5_all_sell_avg_trade_price"] = pre5_all_sell_avg_trade_price

        large_above_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, None)
        super_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.super_volume, None)
        large_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.max_volume, None)
        medium_before_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_before, None)
        medium_after_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_after, None)
        small_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.mid_volume, None)

        data["large_above_avg_trade_price"] = large_above_avg_trade_price
        data["super_avg_trade_price"] = super_avg_trade_price
        data["large_avg_trade_price"] = large_avg_trade_price
        data["medium_before_avg_trade_price"] = medium_before_avg_trade_price
        data["medium_after_avg_trade_price"] = medium_after_avg_trade_price
        data["small_avg_trade_price"] = small_avg_trade_price

        data["large_above_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_avg_trade_price, close_amt)
        data["super_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(super_avg_trade_price, close_amt)
        data["large_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_avg_trade_price, close_amt)
        data["medium_before_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_before_avg_trade_price, close_amt)
        data["medium_after_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_after_avg_trade_price, close_amt)
        data["small_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_avg_trade_price, close_amt)

        large_above_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, self.outside_dish)
        super_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.super_volume, self.outside_dish)
        large_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.max_volume, self.outside_dish)
        medium_before_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_before, self.outside_dish)
        medium_after_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_after, self.outside_dish)
        small_buy_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.min_volume, self.outside_dish)

        data["large_above_buy_avg_trade_price"] = large_above_buy_avg_trade_price
        data["super_buy_avg_trade_price"] = super_buy_avg_trade_price
        data["large_buy_avg_trade_price"] = large_buy_avg_trade_price
        data["medium_before_buy_avg_trade_price"] = medium_before_buy_avg_trade_price
        data["medium_after_buy_avg_trade_price"] = medium_after_buy_avg_trade_price
        data["small_buy_avg_trade_price"] = small_buy_avg_trade_price

        data["large_above_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_buy_avg_trade_price, close_amt)
        data["super_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(super_buy_avg_trade_price, close_amt)
        data["large_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_buy_avg_trade_price, close_amt)
        data["medium_before_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_before_buy_avg_trade_price, close_amt)
        data["medium_after_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_after_buy_avg_trade_price, close_amt)
        data["small_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_buy_avg_trade_price, close_amt)

        large_above_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, self.inside_dish)
        super_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.super_volume, self.inside_dish)
        large_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.max_volume,  self.inside_dish)
        medium_before_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_before, self.inside_dish)
        medium_after_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.volume_medium_after, self.inside_dish)
        small_sell_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.min_volume, self.inside_dish)

        data["large_above_sell_avg_trade_price"] = large_above_sell_avg_trade_price
        data["super_sell_avg_trade_price"] = super_sell_avg_trade_price
        data["large_sell_avg_trade_price"] = large_sell_avg_trade_price
        data["medium_before_sell_avg_trade_price"] = medium_before_sell_avg_trade_price
        data["medium_after_sell_avg_trade_price"] = medium_after_sell_avg_trade_price
        data["small_sell_avg_trade_price"] = small_sell_avg_trade_price

        data["large_above_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_sell_avg_trade_price, close_amt)
        data["super_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(super_sell_avg_trade_price, close_amt)
        data["large_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_sell_avg_trade_price, close_amt)
        data["medium_before_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_before_sell_avg_trade_price, close_amt)
        data["medium_after_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(medium_after_sell_avg_trade_price, close_amt)
        data["small_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_sell_avg_trade_price, close_amt)

        ################
        pre3_large_above_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_avg_trade_price, 3)
        pre3_super_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_avg_trade_price, 3)
        pre3_large_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_avg_trade_price, 3)
        pre3_medium_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_avg_trade_price, 3)
        pre3_medium_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_avg_trade_price, 3)
        pre3_small_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_avg_trade_price, 3)

        data["pre3_large_above_avg_trade_price"] = pre3_large_above_avg_trade_price
        data["pre3_super_avg_trade_price"] = pre3_super_avg_trade_price
        data["pre3_large_avg_trade_price"] = pre3_large_avg_trade_price
        data["pre3_medium_before_avg_trade_price"] = pre3_medium_before_avg_trade_price
        data["pre3_medium_after_avg_trade_price"] = pre3_medium_after_avg_trade_price
        data["pre3_small_avg_trade_price"] = pre3_small_avg_trade_price

        data["pre3_large_above_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_above_avg_trade_price, close_amt)
        data["pre3_super_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_super_avg_trade_price, close_amt)
        data["pre3_large_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_avg_trade_price, close_amt)
        data["pre3_medium_before_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_before_avg_trade_price, close_amt)
        data["pre3_medium_after_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_after_avg_trade_price, close_amt)
        data["pre3_small_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_small_avg_trade_price, close_amt)

        pre3_large_above_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_buy_avg_trade_price, 3)
        pre3_super_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_buy_avg_trade_price, 3)
        pre3_large_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_buy_avg_trade_price, 3)
        pre3_medium_buy_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_buy_avg_trade_price, 3)
        pre3_medium_buy_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_buy_avg_trade_price, 3)
        pre3_small_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_buy_avg_trade_price, 3)

        data["pre3_large_above_buy_avg_trade_price"] = pre3_large_above_buy_avg_trade_price
        data["pre3_super_buy_avg_trade_price"] = pre3_super_buy_avg_trade_price
        data["pre3_large_buy_avg_trade_price"] = pre3_large_buy_avg_trade_price
        data["pre3_medium_before_buy_avg_trade_price"] = pre3_medium_buy_before_avg_trade_price
        data["pre3_medium_after_buy_avg_trade_price"] = pre3_medium_buy_after_avg_trade_price
        data["pre3_small_buy_avg_trade_price"] = pre3_small_buy_avg_trade_price

        data["pre3_large_above_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_above_buy_avg_trade_price, close_amt)
        data["pre3_super_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_super_buy_avg_trade_price, close_amt)
        data["pre3_large_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_buy_avg_trade_price, close_amt)
        data["pre3_medium_before_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_buy_before_avg_trade_price, close_amt)
        data["pre3_medium_after_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_buy_after_avg_trade_price, close_amt)
        data["pre3_small_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_small_buy_avg_trade_price, close_amt)

        pre3_large_above_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_sell_avg_trade_price, 3)
        pre3_super_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_sell_avg_trade_price, 3)
        pre3_large_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_sell_avg_trade_price, 3)
        pre3_medium_sell_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_sell_avg_trade_price, 3)
        pre3_medium_sell_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_sell_avg_trade_price, 3)
        pre3_small_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_sell_avg_trade_price, 3)

        data["pre3_large_above_sell_avg_trade_price"] = pre3_large_above_sell_avg_trade_price
        data["pre3_super_sell_avg_trade_price"] = pre3_super_sell_avg_trade_price
        data["pre3_large_sell_avg_trade_price"] = pre3_large_sell_avg_trade_price
        data["pre3_medium_before_sell_avg_trade_price"] = pre3_medium_sell_before_avg_trade_price
        data["pre3_medium_after_sell_avg_trade_price"] = pre3_medium_sell_after_avg_trade_price
        data["pre3_small_sell_avg_trade_price"] = pre3_small_sell_avg_trade_price

        data["pre3_large_above_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_above_sell_avg_trade_price, close_amt)
        data["pre3_super_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_super_sell_avg_trade_price, close_amt)
        data["pre3_large_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_large_sell_avg_trade_price, close_amt)
        data["pre3_medium_before_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_sell_before_avg_trade_price, close_amt)
        data["pre3_medium_after_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_medium_sell_after_avg_trade_price, close_amt)
        data["pre3_small_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre3_small_sell_avg_trade_price, close_amt)

        ########################

        pre5_large_above_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_avg_trade_price, 5)
        pre5_super_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_avg_trade_price, 5)
        pre5_large_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_avg_trade_price, 5)
        pre5_medium_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_avg_trade_price, 5)
        pre5_medium_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_avg_trade_price, 5)
        pre5_small_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_avg_trade_price, 5)

        data["pre5_large_above_avg_trade_price"] = pre5_large_above_avg_trade_price
        data["pre5_super_avg_trade_price"] = pre5_super_avg_trade_price
        data["pre5_large_avg_trade_price"] = pre5_large_avg_trade_price
        data["pre5_medium_before_avg_trade_price"] = pre5_medium_before_avg_trade_price
        data["pre5_medium_after_avg_trade_price"] = pre5_medium_after_avg_trade_price
        data["pre5_small_avg_trade_price"] = pre5_small_avg_trade_price

        data["pre5_large_above_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_above_avg_trade_price, close_amt)
        data["pre5_super_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_super_avg_trade_price, close_amt)
        data["pre5_large_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_avg_trade_price, close_amt)
        data["pre5_medium_before_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_before_avg_trade_price, close_amt)
        data["pre5_medium_after_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_after_avg_trade_price, close_amt)
        data["pre5_small_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_small_avg_trade_price, close_amt)

        pre5_large_above_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_buy_avg_trade_price, 5)
        pre5_super_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_buy_avg_trade_price, 5)
        pre5_large_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_buy_avg_trade_price, 5)
        pre5_medium_buy_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_buy_avg_trade_price, 5)
        pre5_medium_buy_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_buy_avg_trade_price, 5)
        pre5_small_buy_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_buy_avg_trade_price, 5)

        data["pre5_large_above_buy_avg_trade_price"] = pre5_large_above_buy_avg_trade_price
        data["pre5_super_buy_avg_trade_price"] = pre5_super_buy_avg_trade_price
        data["pre5_large_buy_avg_trade_price"] = pre5_large_buy_avg_trade_price
        data["pre5_medium_before_buy_avg_trade_price"] = pre5_medium_buy_before_avg_trade_price
        data["pre5_medium_after_buy_avg_trade_price"] = pre5_medium_buy_after_avg_trade_price
        data["pre5_small_buy_avg_trade_price"] = pre5_small_buy_avg_trade_price

        data["pre5_large_above_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_above_buy_avg_trade_price, close_amt)
        data["pre5_super_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_super_buy_avg_trade_price, close_amt)
        data["pre5_large_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_buy_avg_trade_price, close_amt)
        data["pre5_medium_before_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_buy_before_avg_trade_price, close_amt)
        data["pre5_medium_after_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_buy_after_avg_trade_price, close_amt)
        data["pre5_small_buy_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_small_buy_avg_trade_price, close_amt)

        pre5_large_above_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_above_sell_avg_trade_price, 5)
        pre5_super_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.super_sell_avg_trade_price, 5)
        pre5_large_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.large_sell_avg_trade_price, 5)
        pre5_medium_sell_before_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_before_sell_avg_trade_price, 5)
        pre5_medium_sell_after_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.medium_after_sell_avg_trade_price, 5)
        pre5_small_sell_avg_trade_price = self.get_column_avg_trade_price(stock_code, date, self.small_sell_avg_trade_price, 5)

        data["pre5_large_above_sell_avg_trade_price"] = pre5_large_above_sell_avg_trade_price
        data["pre5_super_sell_avg_trade_price"] = pre5_super_sell_avg_trade_price
        data["pre5_large_sell_avg_trade_price"] = pre5_large_sell_avg_trade_price
        data["pre5_medium_before_sell_avg_trade_price"] = pre5_medium_sell_before_avg_trade_price
        data["pre5_medium_after_sell_avg_trade_price"] = pre5_medium_sell_after_avg_trade_price
        data["pre5_small_sell_avg_trade_price"] = pre5_small_sell_avg_trade_price

        data["pre5_large_above_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_above_sell_avg_trade_price, close_amt)
        data["pre5_super_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_super_sell_avg_trade_price, close_amt)
        data["pre5_large_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_large_sell_avg_trade_price, close_amt)
        data["pre5_medium_before_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_sell_before_avg_trade_price, close_amt)
        data["pre5_medium_after_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_medium_sell_after_avg_trade_price, close_amt)
        data["pre5_small_sell_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(pre5_small_sell_avg_trade_price, close_amt)

        ########

        large_above_trade_count = self.get_all_day_trade_count(stock_code, date, self.large_above, None)
        super_trade_count = self.get_all_day_trade_count(stock_code, date, self.super_volume, None)
        large_trade_count = self.get_all_day_trade_count(stock_code, date, self.max_volume, None)
        medium_before_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_before, None)
        medium_after_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_after, None)
        small_trade_count = self.get_all_day_trade_count(stock_code, date, self.min_volume, None)

        data["large_above_trade_count"] = large_above_trade_count
        data["super_trade_count"] = super_trade_count
        data["large_trade_count"] = large_trade_count
        data["medium_before_trade_count"] = medium_before_trade_count
        data["medium_after_trade_count"] = medium_after_trade_count
        data["small_trade_count"] = small_trade_count

        data["large_above_trade_count_ratio"] = self.cal_percent_round_2(large_above_trade_count, trade_count)
        data["super_trade_count_ratio"] = self.cal_percent_round_2(super_trade_count, trade_count)
        data["large_trade_count_ratio"] = self.cal_percent_round_2(large_trade_count, trade_count)
        data["medium_before_trade_count_ratio"] = self.cal_percent_round_2(medium_before_trade_count, trade_count)
        data["medium_after_trade_count_ratio"] = self.cal_percent_round_2(medium_after_trade_count, trade_count)
        data["small_trade_count_ratio"] = self.cal_percent_round_2(small_trade_count, trade_count)

        ##########

        large_above_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.large_above, self.outside_dish)
        super_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.super_volume, self.outside_dish)
        large_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.max_volume, self.outside_dish)
        medium_before_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish)
        medium_after_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish)
        small_buy_trade_count = self.get_all_day_trade_count(stock_code, date, self.min_volume, self.outside_dish)

        data["large_above_buy_trade_count"] = large_above_buy_trade_count
        data["super_buy_trade_count"] = super_buy_trade_count
        data["large_buy_trade_count"] = large_buy_trade_count
        data["medium_before_buy_trade_count"] = medium_before_buy_trade_count
        data["medium_after_buy_trade_count"] = medium_after_buy_trade_count
        data["small_buy_trade_count"] = small_buy_trade_count

        data["large_above_buy_trade_count_ratio"] = self.cal_percent_round_2(large_above_buy_trade_count, trade_count)
        data["super_buy_trade_count_ratio"] = self.cal_percent_round_2(super_buy_trade_count, trade_count)
        data["large_buy_trade_count_ratio"] = self.cal_percent_round_2(large_buy_trade_count, trade_count)
        data["medium_before_buy_trade_count_ratio"] = self.cal_percent_round_2(medium_before_buy_trade_count, trade_count)
        data["medium_after_buy_trade_count_ratio"] = self.cal_percent_round_2(medium_after_buy_trade_count, trade_count)
        data["small_buy_trade_count_ratio"] = self.cal_percent_round_2(small_buy_trade_count, trade_count)

        ############

        large_above_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.large_above, self.inside_dish)
        super_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.super_volume, self.inside_dish)
        large_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.max_volume, self.inside_dish)
        medium_before_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish)
        medium_after_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish)
        small_sell_trade_count = self.get_all_day_trade_count(stock_code, date, self.min_volume, self.inside_dish)

        data["large_above_sell_trade_count"] = large_above_sell_trade_count
        data["super_sell_trade_count"] = super_sell_trade_count
        data["large_sell_trade_count"] = large_sell_trade_count
        data["medium_before_sell_trade_count"] = medium_before_sell_trade_count
        data["medium_after_sell_trade_count"] = medium_after_sell_trade_count
        data["small_sell_trade_count"] = small_sell_trade_count

        data["large_above_sell_trade_count_ratio"] = self.cal_percent_round_2(large_above_sell_trade_count, trade_count)
        data["super_sell_trade_count_ratio"] = self.cal_percent_round_2(super_sell_trade_count, trade_count)
        data["large_sell_trade_count_ratio"] = self.cal_percent_round_2(large_sell_trade_count, trade_count)
        data["medium_before_sell_trade_count_ratio"] = self.cal_percent_round_2(medium_before_sell_trade_count, trade_count)
        data["medium_after_sell_trade_count_ratio"] = self.cal_percent_round_2(medium_after_sell_trade_count, trade_count)
        data["small_sell_trade_count_ratio"] = self.cal_percent_round_2(small_sell_trade_count, trade_count)

        ##########
        super_time9_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_9)
        super_time10_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_10)
        super_time11_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_11)
        super_time13_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_13)
        super_time14_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_14)
        super_time15_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.outside_dish, self.time_15)

        data["super_time9_buy_count"] = super_time9_buy_count
        data["super_time10_buy_count"] = super_time10_buy_count
        data["super_time11_buy_count"] = super_time11_buy_count
        data["super_time13_buy_count"] = super_time13_buy_count
        data["super_time14_buy_count"] = super_time14_buy_count
        data["super_time15_buy_count"] = super_time15_buy_count

        super_time9_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_9)
        super_time10_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_10)
        super_time11_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_11)
        super_time13_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_13)
        super_time14_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_14)
        super_time15_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.super_volume, self.inside_dish, self.time_15)

        data["super_time9_sell_count"] = super_time9_sell_count
        data["super_time10_sell_count"] = super_time10_sell_count
        data["super_time11_sell_count"] = super_time11_sell_count
        data["super_time13_sell_count"] = super_time13_sell_count
        data["super_time14_sell_count"] = super_time14_sell_count
        data["super_time15_sell_count"] = super_time15_sell_count

        #############
        large_time9_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_9)
        large_time10_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_10)
        large_time11_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_11)
        large_time13_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_13)
        large_time14_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_14)
        large_time15_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.outside_dish, self.time_15)

        data["large_time9_buy_count"] = large_time9_buy_count
        data["large_time10_buy_count"] = large_time10_buy_count
        data["large_time11_buy_count"] = large_time11_buy_count
        data["large_time13_buy_count"] = large_time13_buy_count
        data["large_time14_buy_count"] = large_time14_buy_count
        data["large_time15_buy_count"] = large_time15_buy_count

        large_time9_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_9)
        large_time10_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_10)
        large_time11_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_11)
        large_time13_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_13)
        large_time14_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_14)
        large_time15_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.max_volume, self.inside_dish, self.time_15)

        data["large_time9_sell_count"] = large_time9_sell_count
        data["large_time10_sell_count"] = large_time10_sell_count
        data["large_time11_sell_count"] = large_time11_sell_count
        data["large_time13_sell_count"] = large_time13_sell_count
        data["large_time14_sell_count"] = large_time14_sell_count
        data["large_time15_sell_count"] = large_time15_sell_count

        ###############
        medium_before_time9_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_9)
        medium_before_time10_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_10)
        medium_before_time11_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_11)
        medium_before_time13_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_13)
        medium_before_time14_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_14)
        medium_before_time15_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.outside_dish, self.time_15)

        data["medium_before_time9_buy_count"] = medium_before_time9_buy_count
        data["medium_before_time10_buy_count"] = medium_before_time10_buy_count
        data["medium_before_time11_buy_count"] = medium_before_time11_buy_count
        data["medium_before_time13_buy_count"] = medium_before_time13_buy_count
        data["medium_before_time14_buy_count"] = medium_before_time14_buy_count
        data["medium_before_time15_buy_count"] = medium_before_time15_buy_count

        medium_before_time9_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_9)
        medium_before_time10_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_10)
        medium_before_time11_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_11)
        medium_before_time13_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_13)
        medium_before_time14_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_14)
        medium_before_time15_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_before, self.inside_dish, self.time_15)

        data["medium_before_time9_sell_count"] = medium_before_time9_sell_count
        data["medium_before_time10_sell_count"] = medium_before_time10_sell_count
        data["medium_before_time11_sell_count"] = medium_before_time11_sell_count
        data["medium_before_time13_sell_count"] = medium_before_time13_sell_count
        data["medium_before_time14_sell_count"] = medium_before_time14_sell_count
        data["medium_before_time15_sell_count"] = medium_before_time15_sell_count

        #############

        medium_after_time9_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_9)
        medium_after_time10_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_10)
        medium_after_time11_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_11)
        medium_after_time13_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_13)
        medium_after_time14_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_14)
        medium_after_time15_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.outside_dish, self.time_15)

        data["medium_after_time9_buy_count"] = medium_after_time9_buy_count
        data["medium_after_time10_buy_count"] = medium_after_time10_buy_count
        data["medium_after_time11_buy_count"] = medium_after_time11_buy_count
        data["medium_after_time13_buy_count"] = medium_after_time13_buy_count
        data["medium_after_time14_buy_count"] = medium_after_time14_buy_count
        data["medium_after_time15_buy_count"] = medium_after_time15_buy_count

        medium_after_time9_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_9)
        medium_after_time10_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_10)
        medium_after_time11_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_11)
        medium_after_time13_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_13)
        medium_after_time14_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_14)
        medium_after_time15_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.volume_medium_after, self.inside_dish, self.time_15)

        data["medium_after_time9_sell_count"] = medium_after_time9_sell_count
        data["medium_after_time10_sell_count"] = medium_after_time10_sell_count
        data["medium_after_time11_sell_count"] = medium_after_time11_sell_count
        data["medium_after_time13_sell_count"] = medium_after_time13_sell_count
        data["medium_after_time14_sell_count"] = medium_after_time14_sell_count
        data["medium_after_time15_sell_count"] = medium_after_time15_sell_count

        #############

        small_time9_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_9)
        small_time10_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_10)
        small_time11_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_11)
        small_time13_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_13)
        small_time14_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_14)
        small_time15_buy_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.outside_dish, self.time_15)

        data["small_time9_buy_count"] = small_time9_buy_count
        data["small_time10_buy_count"] = small_time10_buy_count
        data["small_time11_buy_count"] = small_time11_buy_count
        data["small_time13_buy_count"] = small_time13_buy_count
        data["small_time14_buy_count"] = small_time14_buy_count
        data["small_time15_buy_count"] = small_time15_buy_count

        small_time9_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_9)
        small_time10_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_10)
        small_time11_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_11)
        small_time13_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_13)
        small_time14_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_14)
        small_time15_sell_count = self.get_fixed_time_trade_count(stock_code, date, self.min_volume, self.inside_dish, self.time_15)

        data["small_time9_sell_count"] = small_time9_sell_count
        data["small_time10_sell_count"] = small_time10_sell_count
        data["small_time11_sell_count"] = small_time11_sell_count
        data["small_time13_sell_count"] = small_time13_sell_count
        data["small_time14_sell_count"] = small_time14_sell_count
        data["small_time15_sell_count"] = small_time15_sell_count

        ####
        data["super_buy_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.super_volume, self.outside_dish)
        data["super_sell_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.super_volume, self.inside_dish)
        data["large_buy_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.max_volume, self.outside_dish)
        data["large_sell_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.max_volume, self.inside_dish)
        data["medium_before_buy_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.volume_medium_before, self.outside_dish)
        data["medium_before_sell_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.volume_medium_before, self.inside_dish)
        data["medium_after_buy_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.volume_medium_after, self.outside_dish)
        data["medium_after_sell_times"] = self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.volume_medium_after, self.inside_dish)

        return data

    def get_column_avg_trade_price(self,stock_code, date, column_name, days):
        sql = "select avg(" + column_name + ") as c from " + self.table_name + " " \
              "where code='" + stock_code + "' and trade_date<'" + date + "' order by trade_date desc limit " + str(days)
        return round(self.count_sql_default_zero(sql),2)

    def get_hundred_million_amt(self, amt):
        return round(amt/100000000, 6)