#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取当日已成交的分笔交易数据

import datetime
from decimal import Decimal
from TushareBase import TushareBase
import tushare as ts


class TushareStockTodayTickTradeData(TushareBase, object):
    def __init__(self):
        super(TushareStockTodayTickTradeData, self).__init__()
        self.table_name = "t_tushare_stock_today_tick_trade_data"
        print("stock today tick trade data")

    def get_one_stock_date_tick_trade_data(self, stock_code=None, date=None):
        if date is None:
            date = self.get_latest_work_day()

        data = ts.get_tick_data(stock_code, date, src="tt")
        if data is None:
            return data

        data["date"] = date
        data["code"] = stock_code
        data.insert(2, "pchange", 0)
        return data

    def get_one_stock_date_tick_trade_data_to_db(self, stock_code, date=None):
        self.delete_today_tick_trade_data(stock_code, date)
        self.data_to_db_append(self.get_one_stock_date_tick_trade_data(stock_code, date), self.table_name)

    def get_one_stock_today_tick_trade_data(self, stock_code):
        data = ts.get_today_ticks(stock_code, pause=self.pause)
        data["date"] = self.get_latest_work_day()
        data["code"] = stock_code

        return data

    def get_one_stock_today_tick_trade_data_replace_to_db(self, stock_code):
        self.delete_today_tick_trade_data(stock_code)
        self.data_to_db_append(self.get_one_stock_today_tick_trade_data(stock_code), self.table_name)

    # 获取当日涨停板股票的交易数据
    def get_limit_up_stock_today_tick_trade_data_replace_to_db(self):
        data_list = self.get_limit_up_stock_from_newly()
        for data in data_list:
            stock_code = data["code"]
            if self.is_exist_stock_today_tick_trade_data(stock_code):
                self.log_info("stock " + stock_code + " is exist_stock_today_tick_trade_data")
                continue
            self.get_one_stock_today_tick_trade_data_replace_to_db(stock_code)
            self.sleep_one_second()

    # 获取所有股票的今日成交交易数据(原有存在的数据直接被覆盖)
    def get_all_stock_today_tick_trade_data_replay_to_db(self):
        df = self.get_stock_basics()
        for stock_code, row in df.iterrows():
            self.get_one_stock_today_tick_trade_data_replace_to_db(stock_code)
            self.sleep_five_second()

    # 获取所有股票的今日成交交易数据(已存在数据的股票直接跳过)
    def get_all_stock_today_tick_trade_data_append_to_db(self):
        df = self.get_stock_basics()
        for index, row in df.iterrows():
            sql = "select count(*) as c from " + self.table_name + " where code='" + index + "' "
            if self.is_exist_data_sql(sql):
                continue

            self.get_one_stock_today_tick_trade_data_replace_to_db(index)
            self.sleep_five_second()

    # 获取指定几个股票今日成交的交易数据
    def get_mulit_stock_today_tick_trade_data_to_db(self, mulit_stock_codes):
        for stock_code in mulit_stock_codes:
            self.get_one_stock_today_tick_trade_data_replace_to_db(stock_code)

    def get_loss_stock_today_tick_trade_data_to_db(self, stock_codes):
        for stock_code in stock_codes:
            sql = "select count(*) as c from  " + self.table_name + " where code = '" + stock_code+"'"
            count = self.count_sql(sql)
            if count > 0:
                continue

            print("stock_code-->" + stock_code)
            self.get_one_stock_today_tick_trade_data_replace_to_db(stock_code)
            self.sleep_five_second()

    def is_exist_stock_today_tick_trade_data(self, stock_code):
        sql = "select count(*) as c from " + self.table_name + " where code='" + stock_code + "' "
        return self.is_exist_data_sql(sql)

    def insert_to_sunso_stock_day_trade_statistic_data_from_today_tick_trade(self):
        data_list = self.get_stocks_not_in_sunso_stock_day_trade_statistic_data()
        if len(data_list) < 1:
            print("date " + self.get_latest_work_day() + " not found today_tick_trade handle to day_trade_statistic_data")
            return
        for data in data_list:
            self.insert_to_sunso_stock_day_trade_statistic_data(data)

    # 需要依赖到的相关表
    #
    def insert_to_sunso_stock_day_trade_statistic_data(self, data):
        stock_code = data["code"]
        date = data["date"]
        if isinstance(date, datetime.date):
            date = self.get_date_str(date)
        open_amt = data["open"]
        close_amt = data["trade"]
        high_amt = data["high"]
        low_amt = data["low"]
        change_percent = data["changepercent"]

        settlement_key = "settlement"
        if settlement_key in data.keys():
            pre_close_amt = data[settlement_key]
        else:
            pre_close_amt = Decimal(self.cal_division_round_2(close_amt, (1 + change_percent / 100)))

        sum_trade_volume = self.get_stock_today_sum_volume(stock_code, date)
        sum_trade_amt = self.get_stock_today_sum_amt(stock_code, date)
        trade_volume = data["volume"]

        amount_key = "amount"
        if amount_key in data.keys():
            trade_amt = data["amount"]
        else:
            trade_amt = sum_trade_amt

        trade_count = self.get_all_count(stock_code, date)
        trade_per_count_avg_volume = self.cal_division_round_2(trade_volume, trade_count)

        sunso_stock_baise = self.get_one_sunso_stock_basic(stock_code, date)
        name_key = "name"
        if name_key in data.keys():
            name = data[name_key]
        else:
            name = sunso_stock_baise["name"]

        turnoverratio_key = "turnoverratio"
        if turnoverratio_key in data.keys():
            turnover_ratio = data[turnoverratio_key]
        else:
            turnover_ratio = str(self.cal_percent_round_2(
                trade_volume, sunso_stock_baise["circulation_stock_volume"]*self.unit_hundred_million))

        avg_amt = str(self.cal_division_round_2(sum_trade_amt, sum_trade_volume*100))

        price_change_percent = str(round(change_percent, 2))
        price_wave_amt = high_amt - low_amt
        price_wave_percent = str(self.cal_percent_round_2(price_wave_amt, pre_close_amt))

        close_low_diff_amt = close_amt - low_amt
        high_close_diff_amt = high_amt - close_amt
        close_low_diff_amt_percent = str(self.cal_percent_round_2(close_low_diff_amt, price_wave_amt))
        high_close_diff_amt_percent = str(self.cal_percent_round_2(high_close_diff_amt, price_wave_amt))
        open_pre_close_diff_amt = open_amt - pre_close_amt
        open_pre_close_diff_amt_percent = str(self.cal_percent_round_2(open_pre_close_diff_amt, pre_close_amt))
        low_pre_close_diff_amt = low_amt - pre_close_amt
        low_pre_close_diff_amt_percent = str(self.cal_percent_round_2(low_pre_close_diff_amt, pre_close_amt))
        high_pre_close_diff_amt = high_amt - pre_close_amt
        high_pre_close_diff_amt_percent = str(self.cal_percent_round_2(high_pre_close_diff_amt, pre_close_amt))

        pre1_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 1)
        pre5_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 5)
        pre10_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 10)
        pre20_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 20)
        pre60_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 60)
        pre90_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 90)
        pre250_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 250)
        pre365_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(
            stock_code, date, 365)

        pre1_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre1_close_price, pre1_close_price))
        pre5_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre5_close_price, pre5_close_price))
        pre10_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre10_close_price, pre10_close_price))
        pre20_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre20_close_price, pre20_close_price))
        pre60_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre60_close_price, pre60_close_price))
        pre90_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre90_close_price, pre90_close_price))
        pre250_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre250_close_price, pre250_close_price))
        pre365_close_price_up_down_percent = str(self.cal_percent_round_2(close_amt - pre365_close_price, pre365_close_price))

        pre1_low_price_up_down_percent = str(self.cal_percent_round_2(low_amt - pre1_close_price, pre1_close_price))
        pre5_low_price_up_down_percent = str(self.cal_percent_round_2(low_amt - pre5_close_price, pre5_close_price))
        pre10_low_price_up_down_percent = str(self.cal_percent_round_2(low_amt - pre10_close_price, pre10_close_price))

        pre_avg1_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 1)
        pre_avg5_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 5)
        pre_avg10_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 10)
        pre_avg20_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 20)
        pre_avg60_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 60)
        pre_avg90_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 90)
        pre_avg250_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 250)
        pre_avg365_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic(stock_code, date, 365)

        pre_avg1_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg1_trade_price, pre_avg1_trade_price))
        pre_avg5_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg5_trade_price, pre_avg5_trade_price))
        pre_avg10_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg10_trade_price, pre_avg10_trade_price))
        pre_avg20_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg20_trade_price, pre_avg20_trade_price))
        pre_avg60_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg60_trade_price, pre_avg60_trade_price))
        pre_avg90_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg90_trade_price, pre_avg90_trade_price))
        pre_avg250_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg250_trade_price, pre_avg250_trade_price))
        pre_avg365_trade_price_percent = str(
            self.cal_percent_round_2(close_amt - pre_avg365_trade_price, pre_avg365_trade_price))

        pre_avg1_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 1)
        pre_avg5_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 5)
        pre_avg10_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 10)
        pre_avg20_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 20)
        pre_avg60_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 60)
        pre_avg90_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 90)
        pre_avg250_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 250)
        pre_avg365_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 365)

        pre_avg1_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg1_trade_volume, pre_avg1_trade_volume))
        pre_avg5_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg5_trade_volume, pre_avg5_trade_volume))
        pre_avg10_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg10_trade_volume, pre_avg10_trade_volume))
        pre_avg20_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg20_trade_volume, pre_avg20_trade_volume))
        pre_avg60_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg60_trade_volume, pre_avg60_trade_volume))
        pre_avg90_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg90_trade_volume, pre_avg90_trade_volume))
        pre_avg250_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg250_trade_volume, pre_avg250_trade_volume))
        pre_avg365_trade_volume_percent = str(
            self.cal_percent_round_2(trade_volume - pre_avg365_trade_volume, pre_avg365_trade_volume))

        pre_avg1_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 1)
        pre_avg5_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 5)
        pre_avg10_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 10)
        pre_avg20_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 20)
        pre_avg60_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 60)
        pre_avg90_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 90)
        pre_avg250_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 250)
        pre_avg365_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic(stock_code, date, 365)

        pre_avg1_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg1_trade_count, pre_avg1_trade_count))
        pre_avg5_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg5_trade_count, pre_avg5_trade_count))
        pre_avg10_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg10_trade_count, pre_avg10_trade_count))
        pre_avg20_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg20_trade_count, pre_avg20_trade_count))
        pre_avg60_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg60_trade_count, pre_avg60_trade_count))
        pre_avg90_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg90_trade_count, pre_avg90_trade_count))
        pre_avg250_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg250_trade_count, pre_avg250_trade_count))
        pre_avg365_trade_count_percent = str(
            self.cal_percent_round_2(trade_count - pre_avg365_trade_count, pre_avg365_trade_count))

        pre_avg1_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 1)
        pre_avg5_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 5)
        pre_avg10_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 10)
        pre_avg20_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 20)
        pre_avg60_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 60)
        pre_avg90_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 90)
        pre_avg250_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 250)
        pre_avg365_trade_per_count_avg_volume = self.get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(stock_code, date, 365)

        pre_avg1_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg1_trade_per_count_avg_volume, pre_avg1_trade_per_count_avg_volume))
        pre_avg5_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg5_trade_per_count_avg_volume, pre_avg5_trade_per_count_avg_volume))
        pre_avg10_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg10_trade_per_count_avg_volume, pre_avg10_trade_per_count_avg_volume))
        pre_avg20_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg20_trade_per_count_avg_volume, pre_avg20_trade_per_count_avg_volume))
        pre_avg60_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg60_trade_per_count_avg_volume, pre_avg60_trade_per_count_avg_volume))
        pre_avg90_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg90_trade_per_count_avg_volume, pre_avg90_trade_per_count_avg_volume))
        pre_avg250_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg250_trade_per_count_avg_volume, pre_avg250_trade_per_count_avg_volume))
        pre_avg365_trade_per_count_avg_volume_percent = str(
            self.cal_percent_round_2(trade_per_count_avg_volume - pre_avg365_trade_per_count_avg_volume, pre_avg365_trade_per_count_avg_volume))


        pre_avg1_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 1)
        pre_avg5_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 5)
        pre_avg10_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 10)
        pre_avg20_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 20)
        pre_avg60_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 60)
        pre_avg90_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 90)
        pre_avg250_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 250)
        pre_avg365_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic(stock_code, date, 365)

        pre_avg1_trade_amt_percent = str(self.cal_percent_round_2(trade_amt-pre_avg1_trade_amt, pre_avg1_trade_amt))
        pre_avg5_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg5_trade_amt, pre_avg5_trade_amt))
        pre_avg10_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg10_trade_amt, pre_avg10_trade_amt))
        pre_avg20_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg20_trade_amt, pre_avg20_trade_amt))
        pre_avg60_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg60_trade_amt, pre_avg60_trade_amt))
        pre_avg90_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg90_trade_amt, pre_avg90_trade_amt))
        pre_avg250_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg250_trade_amt, pre_avg250_trade_amt))
        pre_avg365_trade_amt_percent = str(self.cal_percent_round_2(trade_amt - pre_avg365_trade_amt, pre_avg365_trade_amt))

        inside_dish_volume = self.get_inside_dish_volume(stock_code, date)
        outside_dish_volume = self.get_outside_dish_volume(stock_code, date)
        midside_dish_volume = self.get_midside_dish_volume(stock_code, date)
        sum_dish_volume = self.get_sum_dish_volume(stock_code, date)
        oi_dish_diff_volume = str(outside_dish_volume - inside_dish_volume)
        oi_dish_volume_percent = str(self.cal_percent_round_2(outside_dish_volume, inside_dish_volume))

        inside_dish_amt = self.get_inside_dish_amt(stock_code, date)
        outside_dish_amt = self.get_outside_dish_amt(stock_code, date)
        midside_dish_amt = self.get_midside_dish_amt(stock_code, date)
        sum_dish_amt = self.get_sum_dish_amt(stock_code, date)
        oi_dish_diff_amt = str(outside_dish_amt - inside_dish_amt)
        oi_dish_amt_percent = str(self.cal_percent_round_2(outside_dish_amt, inside_dish_amt))

        inside_dish_count = self.get_inside_dish_count(stock_code, date)
        outside_dish_count = self.get_outside_dish_count(stock_code, date)
        midside_dish_count = self.get_midside_dish_count(stock_code, date)
        sum_dish_count = self.get_sum_dish_count(stock_code, date)
        oi_dish_diff_count = str(outside_dish_count - inside_dish_count)
        oi_dish_count_percent = str(self.cal_percent_round_2(outside_dish_count, inside_dish_count))

        min_trade_volume = self.get_min_volume(stock_code, date)
        mid_trade_volume = self.get_mid_volume(stock_code, date)
        max_trade_volume = self.get_max_volume(stock_code, date)
        super_trade_volume = self.get_super_volume(stock_code, date)
        sum_trade_volume = min_trade_volume + mid_trade_volume + max_trade_volume + super_trade_volume
        min_trade_volume_percent = str(self.cal_percent_round_2(min_trade_volume, sum_trade_volume))
        mid_trade_volume_percent = str(self.cal_percent_round_2(mid_trade_volume, sum_trade_volume))
        max_trade_volume_percent = str(self.cal_percent_round_2(max_trade_volume, sum_trade_volume))
        super_trade_volume_percent = str(self.cal_percent_round_2(super_trade_volume, sum_trade_volume))

        min_trade_amt = self.get_min_amt(stock_code, date)
        mid_trade_amt = self.get_mid_amt(stock_code, date)
        max_trade_amt = self.get_max_amt(stock_code, date)
        super_trade_amt = self.get_super_amt(stock_code, date)
        sum_trade_amt = min_trade_amt + mid_trade_amt + max_trade_amt + super_trade_amt
        min_trade_amt_percent = str(self.cal_percent_round_2(min_trade_amt, sum_trade_amt))
        mid_trade_amt_percent = str(self.cal_percent_round_2(mid_trade_amt, sum_trade_amt))
        max_trade_amt_percent = str(self.cal_percent_round_2(max_trade_amt, sum_trade_amt))
        super_trade_amt_percent = str(self.cal_percent_round_2(super_trade_amt, sum_trade_amt))

        min_trade_count = self.get_min_count(stock_code, date)
        mid_trade_count = self.get_mid_count(stock_code, date)
        max_trade_count = self.get_max_count(stock_code, date)
        super_trade_count = self.get_super_count(stock_code, date)
        sum_trade_count = min_trade_count + mid_trade_count + max_trade_count + super_trade_count
        min_trade_count_percent = str(self.cal_percent_round_2(min_trade_count, sum_trade_count))
        mid_trade_count_percent = str(self.cal_percent_round_2(mid_trade_count, sum_trade_count))
        max_trade_count_percent = str(self.cal_percent_round_2(max_trade_count, sum_trade_count))
        super_trade_count_percent = str(self.cal_percent_round_2(super_trade_count, sum_trade_count))

        max_trade_distribution_time = self.get_max_trade_distribution_time(stock_code, date)
        super_trade_distribution_time = self.get_super_trade_distribution_time(stock_code, date)

        max_buy_data = self.get_stock_buy_max_amt_trade_data_by_date(stock_code, date)
        max_sell_data = self.get_stock_sell_max_amt_trade_data_by_date(stock_code, date)
        single_max_buy_trade_volume = max_buy_data["volume"]
        single_max_buy_trade_amt = max_buy_data["amount"]
        single_max_buy_trade_time = max_buy_data["time"]
        single_max_sell_trade_volume = max_sell_data["volume"]
        single_max_sell_trade_amt = max_sell_data["amount"]
        single_max_sell_trade_time = max_sell_data["time"]
        single_max_buy_trade_volume_percent = str(self.cal_percent_round_2(single_max_buy_trade_volume, sum_trade_volume))
        single_max_buy_trade_amt_percent = str(self.cal_percent_round_2(single_max_buy_trade_amt, sum_trade_amt))
        single_max_sell_trade_volume_percent = str(self.cal_percent_round_2(single_max_sell_trade_volume, sum_trade_volume))
        single_max_sell_trade_amt_percent = str(self.cal_percent_round_2(single_max_sell_trade_amt, sum_trade_amt))

        max_volume = self.max_volume
        super_volume = self.super_volume
        outside_dish = self.outside_dish
        inside_dish = self.inside_dish

        early_before_min_trade_price = self.get_early_before_trade_price(stock_code, date, self.func_min)
        early_before_max_trade_price = self.get_early_before_trade_price(stock_code, date, self.func_max)
        early_before_avg_trade_price = self.get_early_before_avg_trade_price(stock_code, date)
        early_before_diff_trade_price = early_before_max_trade_price - early_before_min_trade_price
        early_after_min_trade_price = self.get_early_after_trade_price(stock_code, date, self.func_min)
        early_after_max_trade_price = self.get_early_after_trade_price(stock_code, date, self.func_max)
        early_after_avg_trade_price = self.get_early_after_avg_trade_price(stock_code, date)
        early_after_diff_trade_price = early_after_max_trade_price - early_after_min_trade_price
        noon_before_min_trade_price = self.get_noon_before_trade_price(stock_code, date, self.func_min)
        noon_before_max_trade_price = self.get_noon_before_trade_price(stock_code, date, self.func_max)
        noon_before_avg_trade_price = self.get_noon_before_avg_trade_price(stock_code, date)
        noon_before_diff_trade_price = noon_before_max_trade_price - noon_before_min_trade_price
        noon_after_min_trade_price = self.get_noon_after_trade_price(stock_code, date, self.func_min)
        noon_after_max_trade_price = self.get_noon_after_trade_price(stock_code, date, self.func_max)
        noon_after_avg_trade_price = self.get_noon_after_avg_trade_price(stock_code, date)
        noon_after_diff_trade_price = noon_after_max_trade_price - noon_after_min_trade_price

        early_before_sum_trade_amt = self.get_early_before_trade_amt(stock_code, date, None, None)
        early_before_buy_trade_amt = self.get_early_before_trade_amt(stock_code, date, None, outside_dish)
        early_before_sell_trade_amt = self.get_early_before_trade_amt(stock_code, date, None, inside_dish)
        early_before_sum_trade_amt_percent = str(self.cal_percent_round_2(early_before_sum_trade_amt, trade_amt))
        early_before_buy_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_trade_amt, trade_amt))
        early_before_sell_trade_amt_percent = str(self.cal_percent_round_2(early_before_sell_trade_amt, trade_amt))

        early_after_sum_trade_amt = self.get_early_after_trade_amt(stock_code, date, None, None)
        early_after_buy_trade_amt = self.get_early_after_trade_amt(stock_code, date, None, outside_dish)
        early_after_sell_trade_amt = self.get_early_after_trade_amt(stock_code, date, None, inside_dish)
        early_after_sum_trade_amt_percent = str(self.cal_percent_round_2(early_before_sum_trade_amt, trade_amt))
        early_after_buy_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_trade_amt, trade_amt))
        early_after_sell_trade_amt_percent = str(self.cal_percent_round_2(early_before_sell_trade_amt, trade_amt))

        noon_before_sum_trade_amt = self.get_noon_before_trade_amt(stock_code, date, None, None)
        noon_before_buy_trade_amt = self.get_noon_before_trade_amt(stock_code, date, None, outside_dish)
        noon_before_sell_trade_amt = self.get_noon_before_trade_amt(stock_code, date, None, inside_dish)
        noon_before_sum_trade_amt_percent = str(self.cal_percent_round_2(early_before_sum_trade_amt, trade_amt))
        noon_before_buy_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_trade_amt, trade_amt))
        noon_before_sell_trade_amt_percent = str(self.cal_percent_round_2(early_before_sell_trade_amt, trade_amt))

        noon_after_sum_trade_amt = self.get_noon_after_trade_amt(stock_code, date, None, None)
        noon_after_buy_trade_amt = self.get_noon_after_trade_amt(stock_code, date, None, outside_dish)
        noon_after_sell_trade_amt = self.get_noon_after_trade_amt(stock_code, date, None, inside_dish)
        noon_after_sum_trade_amt_percent = str(self.cal_percent_round_2(early_before_sum_trade_amt, trade_amt))
        noon_after_buy_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_trade_amt, trade_amt))
        noon_after_sell_trade_amt_percent = str(self.cal_percent_round_2(early_before_sell_trade_amt, trade_amt))

        early_before_max_trade_volume = self.get_early_before_trade_volume(stock_code, date, max_volume, None)
        early_before_max_trade_amt = self.get_early_before_trade_amt(stock_code, date, max_volume, None)
        early_before_max_trade_count = self.get_early_before_trade_count(stock_code, date, max_volume, None)
        early_before_buy_max_trade_volume = self.get_early_before_trade_volume(stock_code, date, max_volume, outside_dish)
        early_before_buy_max_trade_amt = self.get_early_before_trade_amt(stock_code, date, max_volume, outside_dish)
        early_before_buy_max_trade_count = self.get_early_before_trade_count(stock_code, date, max_volume, outside_dish)
        early_before_sell_max_trade_volume = self.get_early_before_trade_volume(stock_code, date, max_volume, inside_dish)
        early_before_sell_max_trade_amt = self.get_early_before_trade_amt(stock_code, date, max_volume, inside_dish)
        early_before_sell_max_trade_count = self.get_early_before_trade_count(stock_code, date, max_volume, inside_dish)
        early_before_bs_max_trade_volume_percent = str(self.cal_percent_round_2(early_before_buy_max_trade_volume, early_before_sell_max_trade_volume))
        early_before_bs_max_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_max_trade_amt, early_before_sell_max_trade_amt))
        early_before_bs_max_trade_count_percent = str(self.cal_percent_round_2(early_before_buy_max_trade_count, early_before_sell_max_trade_count))
        early_before_super_trade_volume = self.get_early_before_trade_volume(stock_code, date, super_volume, None)
        early_before_super_trade_amt = self.get_early_before_trade_amt(stock_code, date, super_volume, None)
        early_before_super_trade_count = self.get_early_before_trade_count(stock_code, date, super_volume, None)
        early_before_buy_super_trade_volume = self.get_early_before_trade_volume(stock_code, date, super_volume, outside_dish)
        early_before_buy_super_trade_amt = self.get_early_before_trade_amt(stock_code, date, super_volume, outside_dish)
        early_before_buy_super_trade_count = self.get_early_before_trade_count(stock_code, date, super_volume, outside_dish)
        early_before_sell_super_trade_volume = self.get_early_before_trade_volume(stock_code, date, super_volume, inside_dish)
        early_before_sell_super_trade_amt = self.get_early_before_trade_amt(stock_code, date, super_volume, inside_dish)
        early_before_sell_super_trade_count = self.get_early_before_trade_count(stock_code, date, super_volume, inside_dish)
        early_before_bs_super_trade_volume_percent = str(self.cal_percent_round_2(early_before_buy_super_trade_volume, early_before_sell_super_trade_volume))
        early_before_bs_super_trade_amt_percent = str(self.cal_percent_round_2(early_before_buy_super_trade_amt, early_before_sell_super_trade_amt))
        early_before_bs_super_trade_count_percent = str(self.cal_percent_round_2(early_before_buy_super_trade_count, early_before_sell_super_trade_count))

        limit_up_price = round(pre_close_amt * Decimal(1.1), 2)
        limit_down_price = round(pre_close_amt * Decimal(0.9), 2)

        open_bid_trade_volume = self.get_stock_volume_by_open_bid(stock_code, date)
        open_bid_trade_amt = self.get_stock_amt_by_open_bid(stock_code, date)
        open_bid_trade_type = self.get_stock_trade_type_by_open_bid(stock_code, date)
        open_bid_trade_amt_percent = str(self.cal_percent_round_2(open_bid_trade_amt, trade_amt))
        close_bid_trade_volume = self.get_stock_volume_by_close_bid(stock_code, date)
        close_bid_trade_amt = self.get_stock_amt_by_close_bid(stock_code, date)
        close_bid_trade_type = self.get_stock_trade_type_by_close_bid(stock_code, date)
        close_bid_trade_amt_percent = str(self.cal_percent_round_2(close_bid_trade_amt, trade_amt))

        limit_up_volume = self.get_stock_volume_by_limit_up_price(stock_code, date, limit_up_price)
        limit_up_amt = self.get_stock_amt_by_limit_up_price(stock_code, date, limit_up_price)
        limit_up_amt_percent = str(self.cal_percent_round_2(limit_up_amt, trade_amt))
        limit_down_volume = self.get_stock_volume_by_limit_down_price(stock_code, date, limit_down_price)
        limit_down_amt = self.get_stock_amt_by_limit_down_price(stock_code, date, limit_down_price)
        limit_down_amt_percent = str(self.cal_percent_round_2(limit_down_amt, trade_amt))

        first_limit_up_time = self.get_stock_first_limit_up_time(stock_code, date, limit_up_price)
        first_limit_down_time = self.get_stock_first_limit_down_time(stock_code, date, limit_down_price)
        last_limit_up_time = self.get_stock_newly_limit_up_time(stock_code, date, limit_up_price)
        last_limit_down_time = self.get_stock_newly_limit_down_time(stock_code, date, limit_down_price)

        continue_up_down_data = self.get_stock_continue_up_down_data(data)
        continue_up_down_days = str(continue_up_down_data["continue_up_down_days"])
        contiune_up_down_percent = str(round(continue_up_down_data["contiune_up_down_percent"], 2))

        dragon_tiger_today = self.get_stock_dragon_tiger_today_data(stock_code, date)
        dragon_tiger_organ_today = self.get_stock_dragon_tiger_organ_today_data(stock_code, date)

        dragon_tiger_today_is = dragon_tiger_today["is_dragon_tiger"]
        dragon_tiger_today_reason = dragon_tiger_today["reason"]
        dragon_tiger_all_today_buy_amt = dragon_tiger_today["buy"]
        dragon_tiger_all_today_sell_amt = dragon_tiger_today["sell"]
        dragon_tiger_organ_today_buy_amt = dragon_tiger_organ_today["buy"]
        dragon_tiger_organ_today_sell_amt = dragon_tiger_organ_today["sell"]
        dragon_tiger_sale_today_buy_amt = dragon_tiger_all_today_buy_amt - dragon_tiger_organ_today_buy_amt
        dragon_tiger_sale_today_sell_amt = dragon_tiger_all_today_sell_amt - dragon_tiger_organ_today_sell_amt

        today_sum_amt = self.cal_division_round_2(trade_amt, 10000)
        dragon_tiger_all_today_buy_amt_percent = str(dragon_tiger_today["buy_percent"]*100)
        dragon_tiger_all_today_sell_amt_percent = str(dragon_tiger_today["sell_percent"]*100)
        dragon_tiger_organ_today_buy_amt_percent = str(self.cal_percent_round_2(dragon_tiger_organ_today_buy_amt, today_sum_amt))
        dragon_tiger_organ_today_sell_amt_percent = str(self.cal_percent_round_2(dragon_tiger_organ_today_sell_amt, today_sum_amt))
        dragon_tiger_sale_today_buy_amt_percent = str(self.cal_percent_round_2(dragon_tiger_sale_today_buy_amt, today_sum_amt))
        dragon_tiger_sale_today_sell_amt_percent = str(self.cal_percent_round_2(dragon_tiger_sale_today_sell_amt, today_sum_amt))

        dragon_tiger_total = self.get_stock_dragon_tiger_total_data(stock_code, date)
        dragon_tiger_organ_total = self.get_stock_dragon_tiger_organ_total_data(stock_code, date)

        dragon_tiger_total_is = dragon_tiger_total["is_dragon_tiger"]
        dragon_tiger_total_reason = dragon_tiger_total["reason"]
        dragon_tiger_all_total_buy_amt = dragon_tiger_total["buy"]
        dragon_tiger_all_total_sell_amt = dragon_tiger_total["sell"]
        dragon_tiger_organ_total_buy_amt = dragon_tiger_organ_total["buy"]
        dragon_tiger_organ_total_sell_amt = dragon_tiger_organ_total["sell"]
        dragon_tiger_sale_total_buy_amt = dragon_tiger_all_total_buy_amt - dragon_tiger_organ_total_buy_amt
        dragon_tiger_sale_total_sell_amt = dragon_tiger_all_total_sell_amt - dragon_tiger_organ_total_sell_amt

        dragon_tiger_organ_total_buy_amt_percent = str(self.cal_percent_round_2(dragon_tiger_organ_total_buy_amt, dragon_tiger_all_total_buy_amt))
        dragon_tiger_organ_total_sell_amt_percent = str(self.cal_percent_round_2(dragon_tiger_organ_total_sell_amt, dragon_tiger_all_total_sell_amt))
        dragon_tiger_sale_total_buy_amt_percent = str(self.cal_percent_round_2(dragon_tiger_sale_total_buy_amt, dragon_tiger_all_total_buy_amt))
        dragon_tiger_sale_total_sell_amt_percent = str(self.cal_percent_round_2(dragon_tiger_sale_total_sell_amt, dragon_tiger_all_total_sell_amt))

        n_day_data = self.get_stock_dragon_tiger_n_day_data(stock_code, date, 5)
        organ_n_day_data = self.get_stock_dragon_tiger_organ_n_day_data(stock_code, date, 5)

        dragon_tiger_all_5day_count = n_day_data["all_count"]
        dragon_tiger_all_5day_buy_count = n_day_data["buy_count"]
        dragon_tiger_all_5day_sell_count = n_day_data["sell_count"]
        dragon_tiger_all_5day_bs_count_percent = str(self.cal_percent_round_2(dragon_tiger_all_5day_buy_count, dragon_tiger_all_5day_sell_count))
        dragon_tiger_all_5day_buy_amt = n_day_data["buy_amt"]
        dragon_tiger_all_5day_sell_amt = n_day_data["sell_amt"]
        dragon_tiger_all_5day_diff_amt = n_day_data["diff_amt"]
        dragon_tiger_all_5day_bs_amt_percent = str(self.cal_percent_round_2(dragon_tiger_all_5day_buy_amt, dragon_tiger_all_5day_sell_amt))

        dragon_tiger_organ_5day_buy_count = organ_n_day_data["buy_count"]
        dragon_tiger_organ_5day_sell_count = organ_n_day_data["sell_count"]
        dragon_tiger_organ_5day_buy_amt = organ_n_day_data["buy_amt"]
        dragon_tiger_organ_5day_sell_amt = organ_n_day_data["sell_amt"]
        dragon_tiger_organ_5day_diff_amt = organ_n_day_data["diff_amt"]
        dragon_tiger_sale_5day_buy_amt = dragon_tiger_all_5day_buy_amt - dragon_tiger_organ_5day_buy_amt
        dragon_tiger_sale_5day_sell_amt = dragon_tiger_all_5day_sell_amt - dragon_tiger_organ_5day_sell_amt
        dragon_tiger_sale_5day_name = self.get_stock_dragon_tiger_sale_name_n_day_data(name, date, 5)

        insert_sql = "insert into " + self.t_sunso_stock_day_trade_statistic_data + "" \
                     "(code,name,open_amt,close_amt,low_amt,high_amt,avg_amt,pre_close_amt,close_low_diff_amt,high_close_diff_amt," \
                     "close_low_diff_amt_percent,high_close_diff_amt_percent," \
                     "open_pre_close_diff_amt,open_pre_close_diff_amt_percent," \
                     "low_pre_close_diff_amt,low_pre_close_diff_amt_percent," \
                     "high_pre_close_diff_amt,high_pre_close_diff_amt_percent," \
                     "trade_volume,trade_amt,trade_count,trade_per_count_avg_volume,turnover_rate," \
                     "price_change_percent,price_wave_amt,price_wave_percent,pre1_close_price,pre5_close_price," \
                     "pre10_close_price,pre20_close_price,pre60_close_price,pre90_close_price,pre250_close_price," \
                     "pre365_close_price,pre1_close_price_up_down_percent,pre5_close_price_up_down_percent," \
                     "pre10_close_price_up_down_percent,pre20_close_price_up_down_percent," \
                     "pre60_close_price_up_down_percent,pre90_close_price_up_down_percent," \
                     "pre250_close_price_up_down_percent,pre365_close_price_up_down_percent," \
                     "pre1_low_price_up_down_percent,pre5_low_price_up_down_percent,pre10_low_price_up_down_percent," \
                     "pre_avg1_trade_price,pre_avg5_trade_price,pre_avg10_trade_price,pre_avg20_trade_price," \
                     "pre_avg60_trade_price,pre_avg90_trade_price,pre_avg250_trade_price,pre_avg365_trade_price," \
                     "pre_avg1_trade_price_percent,pre_avg5_trade_price_percent,pre_avg10_trade_price_percent,pre_avg20_trade_price_percent," \
                     "pre_avg60_trade_price_percent,pre_avg90_trade_price_percent,pre_avg250_trade_price_percent,pre_avg365_trade_price_percent," \
                     "pre_avg1_trade_volume,pre_avg5_trade_volume,pre_avg10_trade_volume,pre_avg20_trade_volume," \
                     "pre_avg60_trade_volume,pre_avg90_trade_volume,pre_avg250_trade_volume,pre_avg365_trade_volume," \
                     "pre_avg1_trade_volume_percent,pre_avg5_trade_volume_percent,pre_avg10_trade_volume_percent,pre_avg20_trade_volume_percent," \
                     "pre_avg60_trade_volume_percent,pre_avg90_trade_volume_percent,pre_avg250_trade_volume_percent,pre_avg365_trade_volume_percent," \
                     "pre_avg1_trade_count,pre_avg5_trade_count,pre_avg10_trade_count,pre_avg20_trade_count," \
                     "pre_avg60_trade_count,pre_avg90_trade_count,pre_avg250_trade_count,pre_avg365_trade_count," \
                     "pre_avg1_trade_count_percent,pre_avg5_trade_count_percent,pre_avg10_trade_count_percent,pre_avg20_trade_count_percent," \
                     "pre_avg60_trade_count_percent,pre_avg90_trade_count_percent,pre_avg250_trade_count_percent,pre_avg365_trade_count_percent," \
                     "pre_avg1_trade_per_count_avg_volume,pre_avg5_trade_per_count_avg_volume,pre_avg10_trade_per_count_avg_volume,pre_avg20_trade_per_count_avg_volume," \
                     "pre_avg60_trade_per_count_avg_volume,pre_avg90_trade_per_count_avg_volume,pre_avg250_trade_per_count_avg_volume,pre_avg365_trade_per_count_avg_volume," \
                     "pre_avg1_trade_per_count_avg_volume_percent,pre_avg5_trade_per_count_avg_volume_percent,pre_avg10_trade_per_count_avg_volume_percent,pre_avg20_trade_per_count_avg_volume_percent," \
                     "pre_avg60_trade_per_count_avg_volume_percent,pre_avg90_trade_per_count_avg_volume_percent,pre_avg250_trade_per_count_avg_volume_percent,pre_avg365_trade_per_count_avg_volume_percent," \
                     "pre_avg1_trade_amt,pre_avg5_trade_amt,pre_avg10_trade_amt,pre_avg20_trade_amt," \
                     "pre_avg60_trade_amt,pre_avg90_trade_amt,pre_avg250_trade_amt,pre_avg365_trade_amt," \
                     "pre_avg1_trade_amt_percent,pre_avg5_trade_amt_percent,pre_avg10_trade_amt_percent,pre_avg20_trade_amt_percent," \
                     "pre_avg60_trade_amt_percent,pre_avg90_trade_amt_percent,pre_avg250_trade_amt_percent,pre_avg365_trade_amt_percent," \
                     "inside_dish_volume,outside_dish_volume," \
                     "midside_dish_volume,sum_dish_volume,oi_dish_diff_volume,oi_dish_volume_percent,inside_dish_amt," \
                     "outside_dish_amt,midside_dish_amt,sum_dish_amt,oi_dish_diff_amt,oi_dish_amt_percent," \
                     "inside_dish_count,outside_dish_count,midside_dish_count,sum_dish_count," \
                     "oi_dish_diff_count,oi_dish_count_percent," \
                     "min_trade_volume,mid_trade_volume,max_trade_volume,super_trade_volume,sum_trade_volume,min_trade_volume_percent," \
                     "mid_trade_volume_percent,max_trade_volume_percent,super_trade_volume_percent,min_trade_amt,mid_trade_amt,max_trade_amt," \
                     "super_trade_amt,sum_trade_amt,min_trade_amt_percent,mid_trade_amt_percent,max_trade_amt_percent,super_trade_amt_percent,min_trade_count," \
                     "mid_trade_count,max_trade_count,super_trade_count,sum_trade_count,min_trade_count_percent,mid_trade_count_percent," \
                     "max_trade_count_percent,super_trade_count_percent,max_trade_distribution_time,super_trade_distribution_time," \
                     "single_max_buy_trade_volume,single_max_buy_trade_amt,single_max_buy_trade_time," \
                     "single_max_sell_trade_volume,single_max_sell_trade_amt,single_max_sell_trade_time," \
                     "single_max_buy_trade_volume_percent,single_max_buy_trade_amt_percent," \
                     "single_max_sell_trade_volume_percent,single_max_sell_trade_amt_percent," \
                     "early_before_min_trade_price,early_before_max_trade_price,early_before_avg_trade_price,early_before_diff_trade_price," \
                     "early_after_min_trade_price,early_after_max_trade_price,early_after_avg_trade_price,early_after_diff_trade_price," \
                     "noon_before_min_trade_price,noon_before_max_trade_price,noon_before_avg_trade_price,noon_before_diff_trade_price," \
                     "noon_after_min_trade_price,noon_after_max_trade_price,noon_after_avg_trade_price,noon_after_diff_trade_price," \
                     "early_before_sum_trade_amt,early_before_buy_trade_amt,early_before_sell_trade_amt," \
                     "early_before_sum_trade_amt_percent,early_before_buy_trade_amt_percent,early_before_sell_trade_amt_percent," \
                     "early_after_sum_trade_amt,early_after_buy_trade_amt,early_after_sell_trade_amt," \
                     "early_after_sum_trade_amt_percent,early_after_buy_trade_amt_percent,early_after_sell_trade_amt_percent," \
                     "noon_before_sum_trade_amt,noon_before_buy_trade_amt,noon_before_sell_trade_amt," \
                     "noon_before_sum_trade_amt_percent,noon_before_buy_trade_amt_percent,noon_before_sell_trade_amt_percent," \
                     "noon_after_sum_trade_amt,noon_after_buy_trade_amt,noon_after_sell_trade_amt," \
                     "noon_after_sum_trade_amt_percent,noon_after_buy_trade_amt_percent,noon_after_sell_trade_amt_percent," \
                     "early_before_max_trade_volume,early_before_max_trade_amt,early_before_max_trade_count," \
                     "early_before_buy_max_trade_volume,early_before_buy_max_trade_amt,early_before_buy_max_trade_count," \
                     "early_before_sell_max_trade_volume,early_before_sell_max_trade_amt,early_before_sell_max_trade_count," \
                     "early_before_bs_max_trade_volume_percent,early_before_bs_max_trade_amt_percent,early_before_bs_max_trade_count_percent," \
                     "early_before_super_trade_volume,early_before_super_trade_amt,early_before_super_trade_count," \
                     "early_before_buy_super_trade_volume,early_before_buy_super_trade_amt,early_before_buy_super_trade_count," \
                     "early_before_sell_super_trade_volume,early_before_sell_super_trade_amt,early_before_sell_super_trade_count," \
                     "early_before_bs_super_trade_volume_percent,early_before_bs_super_trade_amt_percent,early_before_bs_super_trade_count_percent," \
                     "open_bid_trade_volume,open_bid_trade_amt,open_bid_trade_type,open_bid_trade_amt_percent,close_bid_trade_volume," \
                     "close_bid_trade_amt,close_bid_trade_type,close_bid_trade_amt_percent," \
                     "limit_up_volume,limit_up_amt,limit_up_amt_percent,limit_down_volume,limit_down_amt,limit_down_amt_percent," \
                     "first_limit_up_time,first_limit_down_time,last_limit_up_time,last_limit_down_time," \
                     "continue_up_down_days,contiune_up_down_percent," \
                     "dragon_tiger_today_is,dragon_tiger_today_reason,dragon_tiger_all_today_buy_amt," \
                     "dragon_tiger_all_today_sell_amt,dragon_tiger_organ_today_buy_amt,dragon_tiger_organ_today_sell_amt," \
                     "dragon_tiger_sale_today_buy_amt,dragon_tiger_sale_today_sell_amt,dragon_tiger_all_today_buy_amt_percent," \
                     "dragon_tiger_all_today_sell_amt_percent,dragon_tiger_organ_today_buy_amt_percent,dragon_tiger_organ_today_sell_amt_percent," \
                     "dragon_tiger_sale_today_buy_amt_percent,dragon_tiger_sale_today_sell_amt_percent," \
                     "dragon_tiger_total_is,dragon_tiger_total_reason,dragon_tiger_all_total_buy_amt,dragon_tiger_all_total_sell_amt,dragon_tiger_organ_total_buy_amt," \
                     "dragon_tiger_organ_total_sell_amt,dragon_tiger_sale_total_buy_amt,dragon_tiger_sale_total_sell_amt," \
                     "dragon_tiger_organ_total_buy_amt_percent,dragon_tiger_organ_total_sell_amt_percent," \
                     "dragon_tiger_sale_total_buy_amt_percent,dragon_tiger_sale_total_sell_amt_percent," \
                     "dragon_tiger_all_5day_count,dragon_tiger_all_5day_buy_count,dragon_tiger_all_5day_sell_count,dragon_tiger_all_5day_bs_count_percent," \
                     "dragon_tiger_all_5day_buy_amt,dragon_tiger_all_5day_sell_amt,dragon_tiger_all_5day_diff_amt,dragon_tiger_all_5day_bs_amt_percent," \
                     "dragon_tiger_organ_5day_buy_count,dragon_tiger_organ_5day_sell_count,dragon_tiger_organ_5day_buy_amt," \
                     "dragon_tiger_organ_5day_sell_amt,dragon_tiger_organ_5day_diff_amt,dragon_tiger_sale_5day_buy_amt," \
                     "dragon_tiger_sale_5day_sell_amt,dragon_tiger_sale_5day_name,trade_date) " \
                     "values(" \
                     "'" + stock_code + "'," + \
                     "'" + name + "'," + \
                     "" + str(open_amt) + "," + \
                     "" + str(close_amt) + "," + \
                     "" + str(low_amt) + "," + \
                     "" + str(high_amt) + "," + \
                     "" + str(avg_amt) + "," + \
                     "" + str(pre_close_amt) + "," + \
                     "" + str(close_low_diff_amt) + "," + \
                     "" + str(high_close_diff_amt) + "," + \
                     "" + str(close_low_diff_amt_percent) + "," + \
                     "" + str(high_close_diff_amt_percent) + "," + \
                     "" + str(open_pre_close_diff_amt) + "," + \
                     "" + str(open_pre_close_diff_amt_percent) + "," + \
                     "" + str(low_pre_close_diff_amt) + "," + \
                     "" + str(low_pre_close_diff_amt_percent) + "," + \
                     "" + str(high_pre_close_diff_amt) + "," + \
                     "" + str(high_pre_close_diff_amt_percent) + "," + \
                     "" + str(trade_volume) + "," + \
                     "" + str(trade_amt) + "," + \
                     "" + str(trade_count) + "," + \
                     "" + str(trade_per_count_avg_volume) + "," + \
                     "" + str(turnover_ratio) + "," + \
                     "" + str(price_change_percent) + "," + \
                     "" + str(price_wave_amt) + "," + \
                     "" + str(price_wave_percent) + "," + \
                     "" + str(pre1_close_price) + "," + \
                     "" + str(pre5_close_price) + "," + \
                     "" + str(pre10_close_price) + "," + \
                     "" + str(pre20_close_price) + "," + \
                     "" + str(pre60_close_price) + "," + \
                     "" + str(pre90_close_price) + "," + \
                     "" + str(pre250_close_price) + "," + \
                     "" + str(pre365_close_price) + "," + \
                     "" + str(pre1_close_price_up_down_percent) + "," + \
                     "" + str(pre5_close_price_up_down_percent) + "," + \
                     "" + str(pre10_close_price_up_down_percent) + "," + \
                     "" + str(pre20_close_price_up_down_percent) + "," + \
                     "" + str(pre60_close_price_up_down_percent) + "," + \
                     "" + str(pre90_close_price_up_down_percent) + "," + \
                     "" + str(pre250_close_price_up_down_percent) + "," + \
                     "" + str(pre365_close_price_up_down_percent) + "," + \
                     "" + str(pre1_low_price_up_down_percent) + "," + \
                     "" + str(pre5_low_price_up_down_percent) + "," + \
                     "" + str(pre10_low_price_up_down_percent) + "," + \
                     "" + str(pre_avg1_trade_price) + "," + \
                     "" + str(pre_avg5_trade_price) + "," + \
                     "" + str(pre_avg10_trade_price) + "," + \
                     "" + str(pre_avg20_trade_price) + "," + \
                     "" + str(pre_avg60_trade_price) + "," + \
                     "" + str(pre_avg90_trade_price) + "," + \
                     "" + str(pre_avg250_trade_price) + "," + \
                     "" + str(pre_avg365_trade_price) + "," + \
                     "" + str(pre_avg1_trade_price_percent) + "," + \
                     "" + str(pre_avg5_trade_price_percent) + "," + \
                     "" + str(pre_avg10_trade_price_percent) + "," + \
                     "" + str(pre_avg20_trade_price_percent) + "," + \
                     "" + str(pre_avg60_trade_price_percent) + "," + \
                     "" + str(pre_avg90_trade_price_percent) + "," + \
                     "" + str(pre_avg250_trade_price_percent) + "," + \
                     "" + str(pre_avg365_trade_price_percent) + "," + \
                     "" + str(pre_avg1_trade_volume) + "," + \
                     "" + str(pre_avg5_trade_volume) + "," + \
                     "" + str(pre_avg10_trade_volume) + "," + \
                     "" + str(pre_avg20_trade_volume) + "," + \
                     "" + str(pre_avg60_trade_volume) + "," + \
                     "" + str(pre_avg90_trade_volume) + "," + \
                     "" + str(pre_avg250_trade_volume) + "," + \
                     "" + str(pre_avg365_trade_volume) + "," + \
                     "" + str(pre_avg1_trade_volume_percent) + "," + \
                     "" + str(pre_avg5_trade_volume_percent) + "," + \
                     "" + str(pre_avg10_trade_volume_percent) + "," + \
                     "" + str(pre_avg20_trade_volume_percent) + "," + \
                     "" + str(pre_avg60_trade_volume_percent) + "," + \
                     "" + str(pre_avg90_trade_volume_percent) + "," + \
                     "" + str(pre_avg250_trade_volume_percent) + "," + \
                     "" + str(pre_avg365_trade_volume_percent) + "," + \
                     "" + str(pre_avg1_trade_count) + "," + \
                     "" + str(pre_avg5_trade_count) + "," + \
                     "" + str(pre_avg10_trade_count) + "," + \
                     "" + str(pre_avg20_trade_count) + "," + \
                     "" + str(pre_avg60_trade_count) + "," + \
                     "" + str(pre_avg90_trade_count) + "," + \
                     "" + str(pre_avg250_trade_count) + "," + \
                     "" + str(pre_avg365_trade_count) + "," + \
                     "" + str(pre_avg1_trade_count_percent) + "," + \
                     "" + str(pre_avg5_trade_count_percent) + "," + \
                     "" + str(pre_avg10_trade_count_percent) + "," + \
                     "" + str(pre_avg20_trade_count_percent) + "," + \
                     "" + str(pre_avg60_trade_count_percent) + "," + \
                     "" + str(pre_avg90_trade_count_percent) + "," + \
                     "" + str(pre_avg250_trade_count_percent) + "," + \
                     "" + str(pre_avg365_trade_count_percent) + "," + \
                     "" + str(pre_avg1_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg5_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg10_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg20_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg60_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg90_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg250_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg365_trade_per_count_avg_volume) + "," + \
                     "" + str(pre_avg1_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg5_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg10_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg20_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg60_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg90_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg250_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg365_trade_per_count_avg_volume_percent) + "," + \
                     "" + str(pre_avg1_trade_amt) + "," + \
                     "" + str(pre_avg5_trade_amt) + "," + \
                     "" + str(pre_avg10_trade_amt) + "," + \
                     "" + str(pre_avg20_trade_amt) + "," + \
                     "" + str(pre_avg60_trade_amt) + "," + \
                     "" + str(pre_avg90_trade_amt) + "," + \
                     "" + str(pre_avg250_trade_amt) + "," + \
                     "" + str(pre_avg365_trade_amt) + "," + \
                     "" + str(pre_avg1_trade_amt_percent) + "," + \
                     "" + str(pre_avg5_trade_amt_percent) + "," + \
                     "" + str(pre_avg10_trade_amt_percent) + "," + \
                     "" + str(pre_avg20_trade_amt_percent) + "," + \
                     "" + str(pre_avg60_trade_amt_percent) + "," + \
                     "" + str(pre_avg90_trade_amt_percent) + "," + \
                     "" + str(pre_avg250_trade_amt_percent) + "," + \
                     "" + str(pre_avg365_trade_amt_percent) + "," + \
                     "" + str(inside_dish_volume) + "," + \
                     "" + str(outside_dish_volume) + "," + \
                     "" + str(midside_dish_volume) + "," + \
                     "" + str(sum_dish_volume) + "," + \
                     "" + str(oi_dish_diff_volume) + "," + \
                     "" + str(oi_dish_volume_percent) + "," + \
                     "" + str(inside_dish_amt) + "," + \
                     "" + str(outside_dish_amt) + "," + \
                     "" + str(midside_dish_amt) + "," + \
                     "" + str(sum_dish_amt) + "," + \
                     "" + str(oi_dish_diff_amt) + "," + \
                     "" + str(oi_dish_amt_percent) + "," + \
                     "" + str(inside_dish_count) + "," + \
                     "" + str(outside_dish_count) + "," + \
                     "" + str(midside_dish_count) + "," + \
                     "" + str(sum_dish_count) + "," + \
                     "" + str(oi_dish_diff_count) + "," + \
                     "" + str(oi_dish_count_percent) + "," + \
                     "" + str(min_trade_volume) + "," + \
                     "" + str(mid_trade_volume) + "," + \
                     "" + str(max_trade_volume) + "," + \
                     "" + str(super_trade_volume) + "," + \
                     "" + str(sum_trade_volume) + "," + \
                     "" + str(min_trade_volume_percent) + "," + \
                     "" + str(mid_trade_volume_percent) + "," + \
                     "" + str(max_trade_volume_percent) + "," + \
                     "" + str(super_trade_volume_percent) + "," + \
                     "" + str(min_trade_amt) + "," + \
                     "" + str(mid_trade_amt) + "," + \
                     "" + str(max_trade_amt) + "," + \
                     "" + str(super_trade_amt) + "," + \
                     "" + str(sum_trade_amt) + "," + \
                     "" + str(min_trade_amt_percent) + "," + \
                     "" + str(mid_trade_amt_percent) + "," + \
                     "" + str(max_trade_amt_percent) + "," + \
                     "" + str(super_trade_amt_percent) + "," + \
                     "" + str(min_trade_count) + "," + \
                     "" + str(mid_trade_count) + "," + \
                     "" + str(max_trade_count) + "," + \
                     "" + str(super_trade_count) + "," + \
                     "" + str(sum_trade_count) + "," + \
                     "" + str(min_trade_count_percent) + "," + \
                     "" + str(mid_trade_count_percent) + "," + \
                     "" + str(max_trade_count_percent) + "," + \
                     "" + str(super_trade_count_percent) + "," + \
                     "'" + str(max_trade_distribution_time) + "'," + \
                     "'" + str(super_trade_distribution_time) + "'," + \
                     "" + str(single_max_buy_trade_volume) + "," + \
                     "" + str(single_max_buy_trade_amt) + "," + \
                     "'" + str(single_max_buy_trade_time) + "'," + \
                     "" + str(single_max_sell_trade_volume) + "," + \
                     "" + str(single_max_sell_trade_amt) + "," + \
                     "'" +str( single_max_sell_trade_time) + "'," + \
                     "" + str(single_max_buy_trade_volume_percent) + "," + \
                     "" + str(single_max_buy_trade_amt_percent) + "," + \
                     "" + str(single_max_sell_trade_volume_percent) + "," + \
                     "" + str(single_max_sell_trade_amt_percent) + "," + \
                     "" + str(early_before_min_trade_price) + "," + \
                     "" + str(early_before_max_trade_price) + "," + \
                     "" + str(early_before_avg_trade_price) + "," + \
                     "" + str(early_before_diff_trade_price) + "," + \
                     "" + str(early_after_min_trade_price) + "," + \
                     "" + str(early_after_max_trade_price) + "," + \
                     "" + str(early_after_avg_trade_price) + "," + \
                     "" + str(early_after_diff_trade_price) + "," + \
                     "" + str(noon_before_min_trade_price) + "," + \
                     "" + str(noon_before_max_trade_price) + "," + \
                     "" + str(noon_before_avg_trade_price) + "," + \
                     "" + str(noon_before_diff_trade_price) + "," + \
                     "" + str(noon_after_min_trade_price) + "," + \
                     "" + str(noon_after_max_trade_price) + "," + \
                     "" + str(noon_after_avg_trade_price) + "," + \
                     "" + str(noon_after_diff_trade_price) + "," + \
                     "" + str(early_before_sum_trade_amt) + "," + \
                     "" + str(early_before_buy_trade_amt) + "," + \
                     "" + str(early_before_sell_trade_amt) + "," + \
                     "" + str(early_before_sum_trade_amt_percent) + "," + \
                     "" + str(early_before_buy_trade_amt_percent) + "," + \
                     "" + str(early_before_sell_trade_amt_percent) + "," + \
                     "" + str(early_after_sum_trade_amt) + "," + \
                     "" + str(early_after_buy_trade_amt) + "," + \
                     "" + str(early_after_sell_trade_amt) + "," + \
                     "" + str(early_after_sum_trade_amt_percent) + "," + \
                     "" + str(early_after_buy_trade_amt_percent) + "," + \
                     "" + str(early_after_sell_trade_amt_percent) + "," + \
                     "" + str(noon_before_sum_trade_amt) + "," + \
                     "" + str(noon_before_buy_trade_amt) + "," + \
                     "" + str(noon_before_sell_trade_amt) + "," + \
                     "" + str(noon_before_sum_trade_amt_percent) + "," + \
                     "" + str(noon_before_buy_trade_amt_percent) + "," + \
                     "" + str(noon_before_sell_trade_amt_percent) + "," + \
                     "" + str(noon_after_sum_trade_amt) + "," + \
                     "" + str(noon_after_buy_trade_amt) + "," + \
                     "" + str(noon_after_sell_trade_amt) + "," + \
                     "" + str(noon_after_sum_trade_amt_percent) + "," + \
                     "" + str(noon_after_buy_trade_amt_percent) + "," + \
                     "" + str(noon_after_sell_trade_amt_percent) + "," + \
                     "" + str(early_before_max_trade_volume) + "," + \
                     "" + str(early_before_max_trade_amt) + "," + \
                     "" + str(early_before_max_trade_count) + "," + \
                     "" + str(early_before_buy_max_trade_volume) + "," + \
                     "" + str(early_before_buy_max_trade_amt) + "," + \
                     "" + str(early_before_buy_max_trade_count) + "," + \
                     "" + str(early_before_sell_max_trade_volume) + "," + \
                     "" + str(early_before_sell_max_trade_amt) + "," + \
                     "" + str(early_before_sell_max_trade_count) + "," + \
                     "" + str(early_before_bs_max_trade_volume_percent) + "," + \
                     "" + str(early_before_bs_max_trade_amt_percent) + "," + \
                     "" + str(early_before_bs_max_trade_count_percent) + "," + \
                     "" + str(early_before_super_trade_volume) + "," + \
                     "" + str(early_before_super_trade_amt) + "," + \
                     "" + str(early_before_super_trade_count) + "," + \
                     "" + str(early_before_buy_super_trade_volume) + "," + \
                     "" + str(early_before_buy_super_trade_amt) + "," + \
                     "" + str(early_before_buy_super_trade_count) + "," + \
                     "" + str(early_before_sell_super_trade_volume) + "," + \
                     "" + str(early_before_sell_super_trade_amt) + "," + \
                     "" + str(early_before_sell_super_trade_count) + "," + \
                     "" + str(early_before_bs_super_trade_volume_percent) + "," + \
                     "" + str(early_before_bs_super_trade_amt_percent) + "," + \
                     "" + str(early_before_bs_super_trade_count_percent) + "," + \
                     "" + str(open_bid_trade_volume) + "," + \
                     "" + str(open_bid_trade_amt) + "," + \
                     "'" + str(open_bid_trade_type) + "'," + \
                     "" + str(open_bid_trade_amt_percent) + "," + \
                     "" + str(close_bid_trade_volume) + "," + \
                     "" + str(close_bid_trade_amt) + "," + \
                     "'" + str(close_bid_trade_type) + "'," + \
                     "" + str(close_bid_trade_amt_percent) + "," + \
                     "" + str(limit_up_volume) + "," + \
                     "" + str(limit_up_amt) + "," + \
                     "" + str(limit_up_amt_percent) + "," + \
                     "" + str(limit_down_volume) + "," + \
                     "" + str(limit_down_amt) + "," + \
                     "" + str(limit_down_amt_percent) + "," + \
                     "'" + str(first_limit_up_time) + "'," + \
                     "'" + str(first_limit_down_time) + "', " + \
                     "'" + str(last_limit_up_time) + "'," + \
                     "'" + str(last_limit_down_time) + "', " \
                     "" + str(continue_up_down_days) + "," \
                     "" + str(contiune_up_down_percent) + "," \
                     "" + str(dragon_tiger_today_is) + "," \
                     "'" + str(dragon_tiger_today_reason) + "'," \
                     "" + str(dragon_tiger_all_today_buy_amt) + "," \
                     "" + str(dragon_tiger_all_today_sell_amt) + "," \
                     "" + str(dragon_tiger_organ_today_buy_amt) + "," \
                     "" + str(dragon_tiger_organ_today_sell_amt) + "," \
                     "" + str(dragon_tiger_sale_today_buy_amt) + "," \
                     "" + str(dragon_tiger_sale_today_sell_amt) + "," \
                     "" + str(dragon_tiger_all_today_buy_amt_percent) + "," \
                     "" + str(dragon_tiger_all_today_sell_amt_percent) + "," \
                     "" + str(dragon_tiger_organ_today_buy_amt_percent) + "," \
                     "" + str(dragon_tiger_organ_today_sell_amt_percent) + "," \
                     "" + str(dragon_tiger_sale_today_buy_amt_percent) + "," \
                     "" + str(dragon_tiger_sale_today_sell_amt_percent) + "," \
                     "" + str(dragon_tiger_total_is) + "," \
                     "'" + str(dragon_tiger_total_reason) + "'," \
                     "" + str(dragon_tiger_all_total_buy_amt) + "," \
                     "" + str(dragon_tiger_all_total_sell_amt) + "," \
                     "" + str(dragon_tiger_organ_total_buy_amt) + "," \
                     "" + str(dragon_tiger_organ_total_sell_amt) + "," \
                     "" + str(dragon_tiger_sale_total_buy_amt) + "," \
                     "" + str(dragon_tiger_sale_total_sell_amt) + "," \
                     "" + str(dragon_tiger_organ_total_buy_amt_percent) + "," \
                     "" + str(dragon_tiger_organ_total_sell_amt_percent) + "," \
                     "" + str(dragon_tiger_sale_total_buy_amt_percent) + "," \
                     "" + str(dragon_tiger_sale_total_sell_amt_percent) + "," \
                     "" + str(dragon_tiger_all_5day_count) + "," \
                     "" + str(dragon_tiger_all_5day_buy_count) + "," \
                     "" + str(dragon_tiger_all_5day_sell_count) + "," \
                     "" + str(dragon_tiger_all_5day_bs_count_percent) + "," \
                     "" + str(dragon_tiger_all_5day_buy_amt) + "," \
                     "" + str(dragon_tiger_all_5day_sell_amt) + "," \
                     "" + str(dragon_tiger_all_5day_diff_amt) + "," \
                     "" + str(dragon_tiger_all_5day_bs_amt_percent) + "," \
                     "" + str(dragon_tiger_organ_5day_buy_count) + "," \
                     "" + str(dragon_tiger_organ_5day_sell_count) + "," \
                     "" + str(dragon_tiger_organ_5day_buy_amt) + "," \
                     "" + str(dragon_tiger_organ_5day_sell_amt) + "," \
                     "" + str(dragon_tiger_organ_5day_diff_amt) + "," \
                     "" + str(dragon_tiger_sale_5day_buy_amt) + "," \
                     "" + str(dragon_tiger_sale_5day_sell_amt) + "," \
                     "'" + str(dragon_tiger_sale_5day_name) + "'," \
                     "'" + str(date) + "')"

        # print(insert_sql)
        # self.insert_sql(insert_sql)
        self.insert_into_about_sunso_stock_day_trade_statistic_data(data)

    # 从当日行情表中获取需要处理的股票数据
    def get_stocks_not_in_sunso_stock_day_trade_statistic_data(self):
        date = self.get_latest_work_day()
        sql = "select * from " + self.t_tushare_stock_newly_quotes_data + " " \
              "where code not in (select code from " + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where trade_date='" + date + "') and date='" + date + "' " \
              " and code in ('600518')"
        return self.select_sql(sql)

    # 从当日行情历史表中获取需要处理的股票数据
    def get_newly_quotes_hist_stocks_not_in_sunso_stock_day_trade_statistic_data(self, date):
        sql = "select * from " + self.t_tushare_stock_newly_quotes_data_hist + " " \
              "where code not in (select code from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where trade_date='" + date + "') and date='" + date + "' " \
              # " and code in ('300508')"
        return self.select_sql(sql)

    # t_tushare_stock_newly_quotes_data 获取某股票N日内平均的交易数量
    def get_avg_trade_volume_from_sunso_stock_day_trade_statistic(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic(stock_code, date, "trade_volume", days)

    # t_tushare_stock_newly_quotes_data 获取某股票N日内平均的交易金额
    def get_avg_trade_amt_from_sunso_stock_day_trade_statistic(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic(stock_code, date, "trade_amt", days)

    # t_tushare_stock_newly_quotes_data 获取某股票N日内平均的交易价格
    def get_avg_trade_price_from_sunso_stock_day_trade_statistic(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic(stock_code, date, "close_amt", days)

    # t_tushare_stock_newly_quotes_data 获取某股票N日内平均的交易次数
    def get_avg_trade_count_from_sunso_stock_day_trade_statistic(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic(stock_code, date, "trade_count", days)

    # t_tushare_stock_newly_quotes_data 获取某股票N日内平均的每日平均交易量
    def get_avg_trade_per_count_avg_volume_from_sunso_stock_day_trade_statistic(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic(stock_code, date, "trade_per_count_avg_volume", days)

    # t_tushare_stock_newly_quotes_data， 获取某个股票，某字段，N日内的平均值
    def get_avg_colum_value_from_sunso_stock_day_trade_statistic(self, stock_code, date, column, days):
        str_days = str(days)
        sql = "select sum(" + column + ")/count(*)  as c from " \
              "(select * from " + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' " \
              "order by trade_date desc limit " + str_days + ") as t"
        return self.count_sql_default_zero(sql)

    # 获取某个股票指定日期N天前的收盘价
    def get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit(self, stock_code, date, days):
        str_days = str(days)
        sql_count = "select count(*) as c from ("\
              "select * from " + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' " \
              "limit  " + str_days + ") as t "
        count_value = self.count_sql_default_zero(sql_count)
        if not count_value == days:
            return 0

        sql = "select close_amt as c from ("\
              "select * from " + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' " \
              "limit  " + str_days + ") as t order by trade_date asc limit 1"
        close_amt = self.count_sql_default_zero(sql)
        # return float(close_amt)
        return close_amt

    def is_exist_today_tick_trade_data(self, stock_code, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select count(*) as c from " + self.table_name + " " \
              "where code='" + stock_code + "' and date='" + date + "' "
        count_value = self.count_sql_default_zero(sql)
        if count_value > 100:
            return True
        return False

    def delete_today_tick_trade_data(self, stock_code, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "delete from " + self.table_name + " " \
              "where code='" + stock_code + "' and date='" + date + "' "
        self.delete_sql(sql)


# print(ts.trade_cal())
today_tick = TushareStockTodayTickTradeData()
# value = today_tick.get_close_price_from_sunso_stock_day_trade_statistic_by_date_and_limit("603978", "2018-10-19", 1)
# print(value)
# print(float(value))
# today_tick.get_limit_up_stock_today_tick_trade_data_replace_to_db()
# today_tick.insert_to_sunso_stock_day_trade_statistic_data_from_today_tick_trade()
# data = ts.get_today_ticks("300748")
# print(data)
# today_tick.get_all_stock_today_tick_trade_data_replay_to_db()
# today_tick.get_one_stock_today_tick_trade_data_replace_to_db("000509")
# today_tick.get_loss_stock_today_tick_trade_data_to_db(['300216','601011','000662','002476','300514','002895','002134','603798','603538','300670','300257','300089','002915','603032','600532','300749','300748','300644','002898','002629','002199','603895','603722','300702','300503','002931','002856','603320','300690','300281','002937','603356','002501'])