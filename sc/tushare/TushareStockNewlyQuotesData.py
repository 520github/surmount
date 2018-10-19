#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tushare as ts
from TushareBase import TushareBase


class TushareStockNewlyQuotesData(TushareBase, object):

    def __init__(self):
        super(TushareStockNewlyQuotesData, self).__init__()
        self.table_name = "t_tushare_stock_newly_quotes_data"
        print("newly quotes data")

    def get_all_stock_newly_quotes_data(self):
        data = ts.get_today_all()
        data["date"] = self.get_latest_work_day()
        return data

    def get_all_stock_newly_quotes_data_to_db(self):
        data = self.get_all_stock_newly_quotes_data()
        if self.is_none(data):
            return
        self.delete_stock_newly_quotes_data()
        self.data_to_db_append(data, self.table_name)
        self.delete_stock_newly_quotes_data_hist(self.get_latest_work_day())
        self.insert_to_stock_newly_quotes_data_hist()

    def clean_all_stock_newly_quotes_data_to_sunso(self):
        self.copy_all_stock_newly_quotes_data_to_sunso()
        self.update_all_sunso_stock_newly_quotes_data()

    def copy_all_stock_newly_quotes_data_to_sunso(self):
        sunso_newly_quotes_table_name = self.t_sunso_stock_newly_quotes_data
        sql_delete = "delete from  " + sunso_newly_quotes_table_name
        self.delete_sql(sql_delete)
        self.select_t_tushare_stock_newly_quotes_data_insert_table(sunso_newly_quotes_table_name)

    def insert_stock_newly_quotes_data_to_sunso_stock_all_quotes_data(self):
        date = self.get_tushare_stock_newly_quotes_data_date()
        if date is None:
            return

        sql_delete = "delete from " + self.t_sunso_stock_all_quotes_data + " where trade_date='" + date + "'"
        self.delete_sql(sql_delete)
        self.select_t_tushare_stock_newly_quotes_data_insert_table(self.t_sunso_stock_all_quotes_data)
        self.update_sunso_stock_all_quotes_data(date)

    def select_t_tushare_stock_newly_quotes_data_insert_table(self, table_name):
        sql_insert = "insert into " + table_name + "(code,name,open_amt,close_amt,low_amt,high_amt,avg_amt," \
        "pre_close_amt,turnover_rate,price_change_percent,price_wave_amt,price_wave_percent,trade_volume,trade_amt," \
        "per,pb,market_cap_amt,circulation_amt,trade_date) " \
        "select distinct code,name,open,trade,low,high,amount/volume,settlement,turnoverratio,changepercent," \
        "high-low,(high-low)/settlement*100,volume,amount,per,pb,mktcap,nmc,date from t_tushare_stock_newly_quotes_data " \
        "where " \
        "code in (select code from " + self.t_tushare_stock_newly_quotes_data + " " \
                  " where changepercent>" + str(self.limit_up_value) + ")"
        # "code in ('600239','600766','603008','603978') "
        self.insert_sql(sql_insert)

    # 更新t_sunso_stock_newly_quotes_data表相关的扩展字段
    def update_sunso_stock_all_quotes_data(self, date):
        # data_list = self.get_sunso_stock_newly_quotes_data()
        data_list = self.get_sunso_stock_all_quotes_data_by_date(date)
        for data in data_list:
            sql = self.get_sunso_stock_all_quotes_data_update_sql(data)
            self.update_sql(sql)

    # 获取t_sunso_stock_newly_quotes_data表的更新相关扩展字段的sql语句
    def get_sunso_stock_all_quotes_data_update_sql(self, data):
        stock_code = data["code"]
        date = data["trade_date"].strftime("%Y-%m-%d")
        avg5_trade_price = str(self.get_avg_trade_price_from_sunso_all_quotes(stock_code, date, 5))
        avg10_trade_price = str(self.get_avg_trade_price_from_sunso_all_quotes(stock_code, date, 10))
        avg20_trade_price = str(self.get_avg_trade_price_from_sunso_all_quotes(stock_code, date, 20))
        avg5_trade_volume = str(self.get_avg_trade_volume_from_sunso_all_quotes(stock_code, date, 5))
        avg10_trade_volume = str(self.get_avg_trade_volume_from_sunso_all_quotes(stock_code, date, 10))
        avg20_trade_volume = str(self.get_avg_trade_volume_from_sunso_all_quotes(stock_code, date, 20))
        avg5_trade_amt = str(self.get_avg_trade_amt_from_sunso_all_quotes(stock_code, date, 5))
        avg10_trade_amt = str(self.get_avg_trade_amt_from_sunso_all_quotes(stock_code, date, 10))
        avg20_trade_amt = str(self.get_avg_trade_amt_from_sunso_all_quotes(stock_code, date, 20))

        inside_dish_volume = self.get_inside_dish_volume(stock_code)
        outside_dish_volume = self.get_outside_dish_volume(stock_code)
        midside_dish_volume = self.get_midside_dish_volume(stock_code)
        oi_dish_diff_volume = str(outside_dish_volume - inside_dish_volume)
        oi_dish_volume_percent = str(self.cal_percent_round_2(outside_dish_volume, inside_dish_volume))

        inside_dish_amt = self.get_inside_dish_amt(stock_code)
        outside_dish_amt = self.get_outside_dish_amt(stock_code)
        midside_dish_amt = self.get_midside_dish_amt(stock_code)
        oi_dish_diff_amt = str(outside_dish_amt - inside_dish_amt)
        oi_dish_amt_percent = str(self.cal_percent_round_2(outside_dish_amt, inside_dish_amt))

        min_trade_volume = self.get_min_volume(stock_code)
        mid_trade_volume = self.get_mid_volume(stock_code)
        max_trade_volume = self.get_max_volume(stock_code)
        sum_trade_volume = min_trade_volume + mid_trade_volume + max_trade_volume
        min_trade_volume_percent = str(self.cal_percent_round_2(min_trade_volume, sum_trade_volume))
        mid_trade_volume_percent = str(self.cal_percent_round_2(mid_trade_volume, sum_trade_volume))
        max_trade_volume_percent = str(self.cal_percent_round_2(max_trade_volume, sum_trade_volume))

        min_trade_amt = self.get_min_amt(stock_code)
        mid_trade_amt = self.get_mid_amt(stock_code)
        max_trade_amt = self.get_max_amt(stock_code)
        sum_trade_amt = min_trade_amt + mid_trade_amt + max_trade_amt
        min_trade_amt_percent = str(self.cal_percent_round_2(min_trade_amt, sum_trade_amt))
        mid_trade_amt_percent = str(self.cal_percent_round_2(mid_trade_amt, sum_trade_amt))
        max_trade_amt_percent = str(self.cal_percent_round_2(max_trade_amt, sum_trade_amt))

        min_trade_count = self.get_min_count(stock_code)
        mid_trade_count = self.get_mid_count(stock_code)
        max_trade_count = self.get_max_count(stock_code)
        sum_trade_count = min_trade_count + mid_trade_count + max_trade_count
        min_trade_count_percent = str(self.cal_percent_round_2(min_trade_count, sum_trade_count))
        mid_trade_count_percent = str(self.cal_percent_round_2(mid_trade_count, sum_trade_count))
        max_trade_count_percent = str(self.cal_percent_round_2(max_trade_count, sum_trade_count))

        first_limit_up_time = self.get_stock_first_limit_up_time(stock_code)
        first_limit_down_time = self.get_stock_first_limit_down_time(stock_code)
        last_limit_up_time = self.get_stock_newly_limit_up_time(stock_code)
        last_limit_down_time = self.get_stock_newly_limit_down_time(stock_code)

        sql = "update " + self.t_sunso_stock_all_quotes_data + \
              " set " \
              "avg5_trade_price=" + avg5_trade_price + "," + \
              "avg10_trade_price=" + avg10_trade_price + "," + \
              "avg20_trade_price=" + avg20_trade_price + "," + \
              "avg5_trade_volume=" + avg5_trade_volume + "," + \
              "avg10_trade_volume=" + avg10_trade_volume + "," + \
              "avg20_trade_volume=" + avg20_trade_volume + "," + \
              "avg5_trade_amt=" + avg5_trade_amt + "," + \
              "avg10_trade_amt=" + avg10_trade_amt + "," + \
              "avg20_trade_amt=" + avg20_trade_amt + "," + \
              "inside_dish_volume=" + str(inside_dish_volume) + "," + \
              "outside_dish_volume=" + str(outside_dish_volume) + "," + \
              "midside_dish_volume=" + str(midside_dish_volume) + "," + \
              "oi_dish_diff_volume=" + oi_dish_diff_volume + "," + \
              "oi_dish_volume_percent=" + oi_dish_volume_percent + "," + \
              "inside_dish_amt=" + str(inside_dish_amt) + "," + \
              "outside_dish_amt=" + str(outside_dish_amt) + "," + \
              "midside_dish_amt=" + str(midside_dish_amt) + "," + \
              "oi_dish_diff_amt=" + oi_dish_diff_amt + "," + \
              "oi_dish_amt_percent=" + oi_dish_amt_percent + "," + \
              "min_trade_volume=" + str(min_trade_volume) + "," + \
              "mid_trade_volume=" + str(mid_trade_volume) + "," + \
              "max_trade_volume=" + str(max_trade_volume) + "," + \
              "sum_trade_volume=" + str(sum_trade_volume) + "," + \
              "min_trade_volume_percent=" + min_trade_volume_percent + "," + \
              "mid_trade_volume_percent=" + mid_trade_volume_percent + "," + \
              "max_trade_volume_percent=" + max_trade_volume_percent + "," + \
              "min_trade_amt=" + str(min_trade_amt) + "," + \
              "mid_trade_amt=" + str(mid_trade_amt) + "," + \
              "max_trade_amt=" + str(max_trade_amt) + "," + \
              "sum_trade_amt=" + str(sum_trade_amt) + "," + \
              "min_trade_amt_percent=" + min_trade_amt_percent + "," + \
              "mid_trade_amt_percent=" + mid_trade_amt_percent + "," + \
              "max_trade_amt_percent=" + max_trade_amt_percent + "," + \
              "min_trade_count=" + str(min_trade_count) + "," + \
              "mid_trade_count=" + str(mid_trade_count) + "," + \
              "max_trade_count=" + str(max_trade_count) + "," + \
              "sum_trade_count=" + str(sum_trade_count) + "," + \
              "min_trade_count_percent=" + min_trade_count_percent + "," + \
              "mid_trade_count_percent=" + mid_trade_count_percent + "," + \
              "max_trade_count_percent=" + max_trade_count_percent + "," + \
              "first_limit_up_time='" + first_limit_up_time + "'," + \
              "first_limit_down_time='" + first_limit_down_time + "', " + \
              "last_limit_up_time='" + last_limit_up_time + "'," + \
              "last_limit_down_time='" + last_limit_down_time + "' " + \
              "where code='" + stock_code + "' and trade_date='" + date + "'"
        return sql

    def get_all_stock_newly_quotes_data_from_db(self):
        sql = "select * from " + self.table_name
        data_list = self.select_sql(sql);
        return data_list

    def delete_stock_newly_quotes_data(self):
        sql = "delete from " + self.table_name + " where date='" + self.get_latest_work_day() + "'"
        self.delete_sql(sql)

    def delete_stock_newly_quotes_data_before_today(self):
        sql = "delete from " + self.table_name + " where date<'" + self.get_latest_work_day() + "'"
        self.delete_sql(sql)

    def delete_stock_newly_quotes_data_hist(self, date):
        sql = "delete from " + self.t_tushare_stock_newly_quotes_data_hist + " where date='" + date + "'"
        self.delete_sql(sql)

    def insert_to_stock_newly_quotes_data_hist(self):
        sql = "insert into " + self.t_tushare_stock_newly_quotes_data_hist + \
              " select * from " + self.table_name + " where date='" + self.get_latest_work_day() + "'"
        self.insert_sql(sql)

    def is_exist_today_newly_quotes_data(self):
        sql = "select count(*) as c from " + self.table_name + " where date='" + self.get_latest_work_day() + "' "
        count_value = self.count_sql_default_zero(sql)
        if count_value > 3000:
            return True
        return False


newly = TushareStockNewlyQuotesData()
# newly.insert_stock_newly_quotes_data_to_sunso_stock_all_quotes_data()
# newly.get_all_stock_newly_quotes_data_to_db()
# newly.copy_all_stock_newly_quotes_data_to_sunso()
# newly.update_all_sunso_stock_newly_quotes_data()
