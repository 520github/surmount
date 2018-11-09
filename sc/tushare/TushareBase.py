#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import sys
import os
import time
import datetime
from decimal import Decimal
import json
from sqlalchemy import create_engine
import tushare as ts
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../common'))
from ConfigReader import ConfigReader
from LightMysql import LightMysql
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/sql'))
from BaseSqlHandler import BaseSqlHandler


class TushareBase:
    table_name = ""
    pause = 1
    unit_hundred_million = 100000000
    # 股票涨停幅度值
    limit_up_value = 9.95
    inside_dish = "卖盘"
    outside_dish = "买盘"
    midside_dish = "中性盘"
    bidside_dish = "竞价盘"
    t_sunso_stock_basic = "t_sunso_stock_basic"
    t_sunso_stock_newly_quotes_data = "t_sunso_stock_newly_quotes_data"
    t_sunso_stock_all_quotes_data = "t_sunso_stock_all_quotes_data"
    t_sunso_stock_day_trade_statistic_data = "t_sunso_stock_day_trade_statistic_data"
    t_sunso_stock_day_trade_statistic_core_data = "t_sunso_stock_day_trade_statistic_core_data"
    t_sunso_stock_day_trade_statistic_volume_data = "t_sunso_stock_day_trade_statistic_volume_data"
    t_tushare_stock_today_tick_trade_data = "t_tushare_stock_today_tick_trade_data"
    t_tushare_stock_hist_tick_trade_data = "t_tushare_stock_hist_tick_trade_data"
    t_tushare_stock_newly_quotes_data = "t_tushare_stock_newly_quotes_data"
    t_tushare_stock_newly_quotes_data_hist = "t_tushare_stock_newly_quotes_data_hist"
    t_tushare_stock_basic = "t_tushare_stock_basic"
    t_tushare_stock_dragon_tiger_today_data = "t_tushare_stock_dragon_tiger_today_data"
    t_tushare_stock_dragon_tiger_organ_today_data = "t_tushare_stock_dragon_tiger_organ_today_data"
    t_tushare_stock_dragon_tiger_organ_total_data = "t_tushare_stock_dragon_tiger_organ_total_data"
    t_tushare_stock_dragon_tiger_total_data = "t_tushare_stock_dragon_tiger_total_data"
    t_tushare_stock_dragon_tiger_sale_total_data = "t_tushare_stock_dragon_tiger_sale_total_data"
    # 小单(手)
    min_volume = " < 200 "
    # 中单(手)
    mid_volume = " between 200 and 1000 "
    # 大单(手)
    max_volume = " between 1001 and 5000 "
    # 超大单(手)
    super_volume = " > 5000 "
    # 大单及超大单
    large_above = " > 1001 "
    # 中单前部分
    volume_medium_before = "between 200 and 700 "
    # 中单后部分
    volume_medium_after = "between 701 and 1000 "
    # 早盘前部分时间
    time_early_before = " between '09:30:00' and '10:00:00' "
    # 早盘后部分时间
    time_early_after = " between '10:00:01' and '11:31:00' "
    # 午盘前部分时间
    time_noon_before = " between '13:00:00' and '14:30:00' "
    # 午盘后部分时间
    time_noon_after = " between '14:30:01' and '14:59:00' "
    time_9 = " like '09:%' "
    time_10 = " like '10:%' "
    time_11 = " like '11:%' "
    time_13 = " like '13:%' "
    time_14 = " like '14:%' "
    time_15 = " like '15:%' "
    # 降序
    desc = "desc"
    # 升序
    asc = "asc"
    func_max = "max"
    func_min = "min"
    func_count = "count"
    func_sum = "sum"
    func_concat = "concat"
    yyyy_mm_dd_date_format = "%Y-%m-%d"
    db_engine = None
    db_execute = None
    sql_handler = BaseSqlHandler

    def __init__(self):
        self.configReader = ConfigReader().get_conf("main")
        TushareBase.db_engine = create_engine(self.configReader.mysql_url)

        dbconfig = {
            'host': '127.0.0.1',
            'port': 3307,
            'user': 'root',
            'passwd': 'root',
            'db': 'tushare',
            'charset': 'utf8'}

        TushareBase.db_execute = LightMysql(dbconfig)

        print("基类构造函数--" + self.configReader.mysql_url)

    def get_db_engine(self):
        print("get db engine~~~" + self.configReader.mysql_url)
        return create_engine(self.configReader.mysql_url)

    def get_one_sunso_stock_basic(self, stock_code, date):
        sql = "select * from " + self.t_sunso_stock_basic + \
              " where code='" + stock_code + "' and trade_date='" + date + "'"
        data = self.select_one_sql(sql)
        if data is None:
            sql = "select * from " + self.t_sunso_stock_basic + " where code='" + stock_code + "' " \
                  "order by trade_date desc limit 1"
            data = self.select_one_sql(sql)
        if data is None:
            return {"name":'', "circulation_stock_volume":0, "industry":"", "area":""}
        return data

    def get_one_stock_basic(self, stock_code):
        sql = "select * from " + self.t_tushare_stock_basic + " where code='" + stock_code + "'"
        data = self.select_sql(sql)[0]
        self.convert_dict_unicode_to_str(data)
        return data

    def get_stock_basics(self):
        data = ts.get_stock_basics()
        data["date"] = self.get_latest_work_day()
        return data

    def get_stock_basics_to_db(self):
        table_name = "t_tushare_stock_basic"
        sql = "delete from " + table_name
        self.delete_sql(sql)
        self.data_to_db_append(self.get_stock_basics(), table_name)

    def get_stock_basics_to_hist_db(self):
        table_name = "t_tushare_stock_basic_hist"
        sql = "delete from " + table_name + " where date='" + self.get_latest_work_day() + "'"
        self.delete_sql(sql)
        self.data_to_db_append(self.get_stock_basics(), table_name)

    def get_tushare_stock_newly_quotes_data_date(self):
        sql = "select max(date) as c from " + self.t_tushare_stock_newly_quotes_data
        return self.count_sql(sql)

    # 从历史交易行情中获取某日涨停板的股票列表
    def get_limit_up_stock(self, date):
        sql = "select code from t_tushare_stock_hist_quotes_data where p_change>9 and date='" + date + "'"
        data_list = self.select_sql(sql)
        for data in data_list:
            data["code"] = data["code"].encode('utf-8')
        return data_list

    # 从当日交易日中获取涨停股票数据
    def get_limit_up_stock_from_newly(self):
        sql = " select * from t_tushare_stock_newly_quotes_data where changepercent >" + str(self.limit_up_value)
        data_list = self.select_sql(sql)
        for data in data_list:
            self.convert_dict_unicode_to_str(data)
        return data_list

    # 获取sunso中最近交易日的股票行情数据
    def get_sunso_stock_newly_quotes_data(self):
        sql = "select * from " + self.t_sunso_stock_newly_quotes_data
        data_list = self.select_sql(sql)
        for data in data_list:
            self.convert_dict_unicode_to_str(data)
        return data_list

    # 获取sunso_stock_all_quotes_data指定日的股票行情数据
    def get_sunso_stock_all_quotes_data_by_date(self, date):
        sql = "select * from " + self.t_sunso_stock_all_quotes_data + " where trade_date='" + date + "'"
        data_list = self.select_sql(sql)
        self.convert_dict_list_unicode_to_str(data_list)
        return data_list

    # 把字典列表中的unicode值转换成字符串
    def convert_dict_list_unicode_to_str(self, data_list):
        if data_list is None:
            return  data_list
        for data in data_list:
            self.convert_dict_unicode_to_str(data)
        return data_list

    # 把字典中的unicode值转换成字符串
    def convert_dict_unicode_to_str(self, data):
        if data is None:
            return data

        for key in data:
            value = data[key]
            if isinstance(value, unicode):
                data[key] = self.encode(value)

        return data

    # 把unicode值转化成字符串
    def encode(self, value):
        return value.encode('utf-8')

    # 获取当日股票的涨停价
    def get_stock_limit_up_value(self, stock_code):
        return round(self.get_stock_pre_close_amt(stock_code) * 1.1, 2)

    # 获取当日股票的跌停价
    def get_stock_limit_down_value(self, stock_code):
        return round(self.get_stock_pre_close_amt(stock_code) * 0.9, 2)

    # 获取当日股票的涨停价
    def get_stock_limit_up_value_by_pre_close_amt(self, pre_close_amt):
        return round(pre_close_amt * Decimal(1.1), 2)

    # 获取当日股票的跌停价
    def get_stock_limit_down_value_by_pre_close_amt(self, pre_close_amt):
        return round(pre_close_amt * Decimal(0.9), 2)

    # 获取股票当前第一次涨停时间
    def get_stock_first_limit_up_time(self, stock_code, date, limit_up_value):
        # limit_up_value = self.get_stock_limit_up_value(stock_code)
        return self.get_stock_time_by_price(stock_code, date, limit_up_value, self.asc)

    # 获取股票当前最近一次涨停时间
    def get_stock_newly_limit_up_time(self, stock_code, date, limit_up_value):
        # limit_up_value = self.get_stock_limit_up_value(stock_code)
        return self.get_stock_time_by_price(stock_code, date, limit_up_value, self.desc)

    # 获取股票当前第一次跌停时间
    def get_stock_first_limit_down_time(self, stock_code, date, limit_down_value):
        # limit_down_value = self.get_stock_limit_down_value(stock_code)
        return self.get_stock_time_by_price(stock_code, date, limit_down_value, self.asc)

    # 获取股票当前最近一次跌停时间
    def get_stock_newly_limit_down_time(self, stock_code, date, limit_down_value):
        # limit_down_value = self.get_stock_limit_down_value(stock_code)
        return self.get_stock_time_by_price(stock_code, date, limit_down_value, self.desc)

    # 根据股价价格，获取出现该价格的时间点
    def get_stock_time_by_price(self, stock_code, date, price, time_sort):
        sql = "select time as c from " + self.t_tushare_stock_today_tick_trade_data + " where code='" + stock_code + \
              "' and price=" + str(price) + " and date='" + date + "' order by time " + time_sort + " limit 1"
        time_value = self.count_sql(sql)
        if time_value is None:
            time_value = ""
        # self.log_info("time-->" + time_value)
        time_value = self.encode(time_value)
        return time_value

    # 获取股票昨日收盘价
    def get_stock_pre_close_amt(self, stock_code):
        sql = "select settlement as c from " + self.t_tushare_stock_newly_quotes_data + \
              " where code='" + stock_code + "' "
        return self.count_sql(sql)

    def get_time_to_market_ymd(self, stock_basics_data):
        # print("value-->" + stock_basics_data["timeToMarket"])
        if stock_basics_data is None:
            print("stock_basics_data parameter is emtpy")
            return self.get_now_ymd()
        return time.strftime('%Y-%m-%d', time.strptime(str(stock_basics_data["timeToMarket"]), '%Y%m%d'))

    def get_avg_trade_volume_from_tushare_quotes(self, stock_code, days):
        sql = "select sum(volume)/" + str(days) + " as c from ( " \
                  "select volume from t_tushare_stock_newly_quotes_data where code='" + stock_code + "' union " \
                  "(select volume from t_tushare_stock_hist_quotes_data where code='" + stock_code + \
                  "' order by date desc limit " + str((days-1)) + ") "\
              " ) as t "
        return self.count_sql_default_zero(sql)

    def get_avg_trade_amt_from_sunso_quotes(self, stock_code, days):
        str_days = str(days)
        sql = "select sum(trade_amt)/" + str_days + " as c from t_sunso_stock_newly_quotes_data_hist where code='" \
              + stock_code + "' order by trade_date desc limit " + str_days
        return self.count_sql_default_zero(sql)

    # 从sunso_all_quotes 获取某股票N日内平均的交易数量
    def get_avg_trade_volume_from_sunso_all_quotes(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_all_quotes(stock_code, date, "trade_volume", days)

    # 从sunso_all_quotes 获取某股票N日内平均的交易金额
    def get_avg_trade_amt_from_sunso_all_quotes(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_all_quotes(stock_code, date, "trade_amt", days)

    # 从sunso_all_quotes 获取某股票N日内平均的交易价格
    def get_avg_trade_price_from_sunso_all_quotes(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_all_quotes(stock_code, date, "close_amt", days)

    # 从sunso_all_quotes， 获取某个股票，某字段，N日内的平均值
    def get_avg_colum_value_from_sunso_all_quotes(self, stock_code, date, column, days):
        str_days = str(days)
        sql = "select sum(" + column + ")/count(*)  as c from " + self.t_sunso_stock_all_quotes_data + " " \
              "where code='" + stock_code + "' and trade_date <='" + date + "' " \
              "order by trade_date desc limit " + str_days
        return self.count_sql_default_zero(sql)


    # 判断某个股票的交易日期数是否达到足够的天数
    def is_enough_trade_date_from_sunso_stock_all_quotes_data(self, stock_code, days):
        count_value = self.count_stock_from_sunso_stock_all_quotes_data(stock_code)
        if count_value >= days:
            return True
        return False

    # 统计某个股票的交易日数量
    def count_stock_from_sunso_stock_all_quotes_data(self, stock_code):
        sql = "select count(*) as c from " + self.t_sunso_stock_all_quotes_data + " where code='" + stock_code + "' "
        return self.count_sql(sql)

    # 获取sunso_stock_quotes_data的列字段
    def get_sunso_stock_quotes_data_column(self):
        sql = "code,name,open_amt,close_amt,low_amt,high_amt,avg_amt,pre_close_amt,turnover_rate,price_change_percent," \
              "price_wave_amt,price_wave_percent,trade_volume,trade_amt,avg5_trade_volume,avg10_trade_volume," \
              "avg20_trade_volume,avg5_trade_amt,avg10_trade_amt,avg20_trade_amt,inside_dish_volume," \
              "outside_dish_volume,oi_dish_diff_volume,oi_dish_volume_percent,inside_dish_amt,outside_dish_amt," \
              "oi_dish_diff_amt,oi_dish_amt_percent,min_trade_volume,mid_trade_volume,max_trade_volume,min_trade_amt," \
              "mid_trade_amt,max_trade_amt,first_limit_up_date,first_limit_down_date,per,pb,market_cap_amt," \
              "circulation_amt,trade_date"
        return sql

    # 获取某个股票的最小交易日期
    def get_min_trade_date_from_sunso_stock_all_quotes_data(self, stock_code):
        sql = "select min(date) as c from " + self.t_sunso_stock_all_quotes_data + " where code='" + stock_code + "' "
        return self.count_sql(sql)

    # 获取股票当日总交易量
    def get_stock_today_sum_volume(self, stock_code, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select sum(volume) as c from " + self.t_tushare_stock_today_tick_trade_data + " where " \
              "code='" + stock_code + "' and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日总交易金额
    def get_stock_today_sum_amt(self, stock_code, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select sum(amount) as c from " + self.t_tushare_stock_today_tick_trade_data + " where " \
              "code='" + stock_code + "' and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的内盘交易量
    def get_inside_dish_volume(self, stock_code, date):
        return self.get_stock_dish_volume_by_type(stock_code, date, self.inside_dish)

    # 获取股票当日的外盘交易量
    def get_outside_dish_volume(self, stock_code, date):
        return self.get_stock_dish_volume_by_type(stock_code, date, self.outside_dish)

    # 获取股票当日的中间盘交易量
    def get_midside_dish_volume(self, stock_code, date):
        return self.get_stock_dish_volume_by_type(stock_code, date, self.midside_dish)

    # 获取股票当日的竞价盘交易量
    def get_bidside_dish_volume(self, stock_code, date):
        return self.get_stock_dish_volume_by_type(stock_code, date, self.bidside_dish)

    # 获取股票当日的所有交易量
    def get_sum_dish_volume(self, stock_code, date):
        return self.get_stock_dish_volume_by_type(stock_code, date, None)

    def get_stock_dish_volume_by_type(self, stock_code, date, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, None, None, trade_type)
        # return self.get_stock_dish_volume_by_table_and_type(
        #     stock_code, self.t_tushare_stock_today_tick_trade_data, trade_type)

    # 获取股票指定日的内盘交易量
    def get_inside_dish_volume_date(self, stock_code, date):
        return self.get_stock_dish_volume_by_type_and_date(stock_code, self.inside_dish, date)

    # 获取股票指定日的外盘交易量
    def get_outside_dish_volume_date(self, stock_code, date):
        return self.get_stock_dish_volume_by_type_and_date(stock_code, self.outside_dish, date)

    # 获取股票指定日的中间盘交易量
    def get_midside_dish_volume_date(self, stock_code, date):
        return self.get_stock_dish_volume_by_type_and_date(stock_code, self.midside_dish, date)

    # 获取股票指定日的竞价盘交易量
    def get_bidside_dish_volume_date(self, stock_code, date):
        return self.get_stock_dish_volume_by_type_and_date(stock_code, self.bidside_dish, date)

    def get_stock_dish_volume_by_type_and_date(self, stock_code, trade_type, date):
        return self.get_stock_dish_volume_by_table_and_type(
            stock_code, self.t_tushare_stock_hist_tick_trade_data, trade_type, date)

    def get_stock_dish_volume_by_table_and_type(self, stock_code, table_name, trade_type, date=None):
        sql = "select sum(volume) as c from " + table_name + " where code='" + stock_code + "' "

        if trade_type is not None:
            sql = sql + " and type='" + trade_type + "'"

        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的内盘交易金额
    def get_inside_dish_amt(self, stock_code, date):
        return self.get_stock_dish_amt_by_type(stock_code, date, self.inside_dish)

    # 获取股票当日的外盘交易金额
    def get_outside_dish_amt(self, stock_code, date):
        return self.get_stock_dish_amt_by_type(stock_code, date, self.outside_dish)

    # 获取股票当日的中间盘交易金额
    def get_midside_dish_amt(self, stock_code, date):
        return self.get_stock_dish_amt_by_type(stock_code, date, self.midside_dish)

    # 获取股票当日的竞价盘交易金额
    def get_bidside_dish_amt(self, stock_code, date):
        return self.get_stock_dish_amt_by_type(stock_code, date, self.bidside_dish)

    # 获取股票当日的所有交易金额
    def get_sum_dish_amt(self, stock_code, date):
        return self.get_stock_dish_amt_by_type(stock_code, date, None)

    def get_stock_dish_amt_by_type(self, stock_code, date, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, None, None, trade_type)
        # return self.get_stock_dish_amt_by_table_and_type(
        #     stock_code, self.t_tushare_stock_today_tick_trade_data, trade_type, None)

    # 获取股票指定日的内盘交易金额
    def get_inside_dish_amt_date(self, stock_code, date):
        return self.get_stock_dish_amt_by_type_and_date(stock_code, self.inside_dish, date)

    # 获取股票指定日的外盘交易金额
    def get_outside_dish_amt_date(self, stock_code, date):
        return self.get_stock_dish_amt_by_type_and_date(stock_code, self.outside_dish, date)

    # 获取股票指定日的中间盘交易金额
    def get_midside_dish_amt_date(self, stock_code, date):
        return self.get_stock_dish_amt_by_type_and_date(stock_code, self.midside_dish, date)

    # 获取股票指定日的竞价盘交易金额
    def get_bidside_dish_amt_date(self, stock_code, date):
        return self.get_stock_dish_amt_by_type_and_date(stock_code, self.bidside_dish, date)

    def get_stock_dish_amt_by_type_and_date(self, stock_code, trade_type, date):
        return self.get_stock_dish_amt_by_table_and_type(
            stock_code, self.t_tushare_stock_hist_tick_trade_data, trade_type, date)

    def get_stock_dish_amt_by_table_and_type(self, stock_code, table_name, trade_type, date):
        sql = "select sum(amount) as c from " + table_name + " where code='" + stock_code + \
              "' "
        if trade_type is not None:
            sql = sql + " and type='" + trade_type + "'"

        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的内盘交易次数
    def get_inside_dish_count(self, stock_code, date):
        return self.get_stock_dish_count_by_type(stock_code, date, self.inside_dish)

    # 获取股票当日的外盘交易次数
    def get_outside_dish_count(self, stock_code, date):
        return self.get_stock_dish_count_by_type(stock_code, date, self.outside_dish)

    # 获取股票当日的中间盘交易次数
    def get_midside_dish_count(self, stock_code, date):
        return self.get_stock_dish_count_by_type(stock_code, date, self.midside_dish)

    # 获取股票当日的竞价盘交易次数
    def get_bidside_dish_count(self, stock_code, date):
        return self.get_stock_dish_count_by_type(stock_code, date, self.bidside_dish)

    # 获取股票当日的所有交易次数
    def get_sum_dish_count(self, stock_code, date):
        return self.get_stock_dish_count_by_type(stock_code, date, None)

    # 获取指定日期、交易类型股票的交易次数
    def get_stock_dish_count_by_type(self, stock_code, date, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, None, None, trade_type)
        # return self.get_stock_dish_count_by_table_and_type(
        #     stock_code, self.t_tushare_stock_today_tick_trade_data, trade_type, self.get_latest_work_day())

    # 获取指定日期、交易类型股票的交易次数
    def get_stock_dish_count_by_table_and_type(self, stock_code, table_name, trade_type, date):
        sql = "select count(*) as c from " + table_name + " where code='" + stock_code + \
              "' "
        if trade_type is not None:
            sql = sql + " and type='" + trade_type + "'"
        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的小单交易次数
    def get_min_count(self, stock_code, date):
        return self.get_stock_count_by_size(stock_code, date, self.min_volume)

    # 获取股票当日的中单交易次数
    def get_mid_count(self, stock_code, date):
        return self.get_stock_count_by_size(stock_code, date, self.mid_volume)

    # 获取股票当日的大单交易次数
    def get_max_count(self, stock_code, date):
        return self.get_stock_count_by_size(stock_code, date, self.max_volume)

    # 获取股票当日的超级大单交易次数
    def get_super_count(self, stock_code, date):
        return self.get_stock_count_by_size(stock_code, date, self.super_volume)

    # 获取当日的总成交次数
    def get_all_count(self, stock_code, date):
        return self.get_stock_count_by_size(stock_code, date, None)

    # 根据交易量大小类型，获取股票对应的交易次数
    def get_stock_count_by_size(self, stock_code, date, volume_condition):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, None, None)
        # return self.get_stock_count_by_table_and_size(
        #     stock_code, self.t_tushare_stock_today_tick_trade_data, volume_condition)

    # 根据对应数据表、交易量大小类型、交易日期， 获取股票对应交易次数
    def get_stock_count_by_table_and_size(self, stock_code, table_name, volume_condition, date=None):
        sql = "select count(*) as c from " + table_name + \
              " where code='" + stock_code + "' and volume " + volume_condition
        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的小单交易量
    def get_min_volume(self, stock_code, date):
        return self.get_stock_volume_by_size(stock_code, date, self.min_volume)

    # 获取股票当日的中单交易量
    def get_mid_volume(self, stock_code, date):
        return self.get_stock_volume_by_size(stock_code, date, self.mid_volume)

    # 获取股票当日的大单交易量
    def get_max_volume(self, stock_code, date):
        return self.get_stock_volume_by_size(stock_code, date, self.max_volume)

    # 获取股票当日的超级大单交易量
    def get_super_volume(self, stock_code, date):
        return self.get_stock_volume_by_size(stock_code, date, self.super_volume)

    def get_stock_volume_by_size(self, stock_code, date, volume_condition):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, None, None)
        # return self.get_stock_volume_by_table_and_size(stock_code, self.t_tushare_stock_today_tick_trade_data,
        #                                                volume_condition)

    # 获取股票指定日的小单交易量
    def get_min_volume_date(self, stock_code, date):
        return self.get_stock_volume_by_size_and_date(stock_code, self.min_volume, date)

    # 获取股票指定日的中单交易量
    def get_mid_volume_date(self, stock_code, date):
        return self.get_stock_volume_by_size_and_date(stock_code, self.mid_volume, date)

    # 获取股票指定日的大单交易量
    def get_max_volume_date(self, stock_code, date):
        return self.get_stock_volume_by_size_and_date(stock_code, self.max_volume, date)

    # 获取股票指定日的超级大单交易量
    def get_super_volume_date(self, stock_code, date):
        return self.get_stock_volume_by_size_and_date(stock_code, self.super_volume, date)

    # 根据交易量大小类型及交易日期， 获取股票对应交易量数据
    def get_stock_volume_by_size_and_date(self, stock_code, volume_condition, date):
        return self.get_stock_volume_by_table_and_size(stock_code, self.t_tushare_stock_hist_tick_trade_data,
                                                       volume_condition, date)

    # 根据对应数据表、交易量大小类型、交易日期， 获取股票对应交易量数据
    def get_stock_volume_by_table_and_size(self, stock_code, table_name, volume_condition, date=None):
        sql = "select sum(volume) as c from " + table_name + \
              " where code='" + stock_code + "' and volume " + volume_condition
        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票当日的小单交易金额
    def get_min_amt(self, stock_code, date):
        return self.get_stock_amt_by_size(stock_code, date, self.min_volume)

    # 获取股票当日的中单交易金额
    def get_mid_amt(self, stock_code, date):
        return self.get_stock_amt_by_size(stock_code, date, self.mid_volume)

    # 获取股票当日的大单交易金额
    def get_max_amt(self, stock_code, date):
        return self.get_stock_amt_by_size(stock_code, date, self.max_volume)

    # 获取股票当日的超级大单交易金额
    def get_super_amt(self, stock_code, date):
        return self.get_stock_amt_by_size(stock_code, date, self.super_volume)

    # 根据交易量大小类型， 获取股票当日对应交易金额数据
    def get_stock_amt_by_size(self, stock_code, date, volume_condition):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, None, None)
        # return self.get_stock_amt_by_table_and_size(stock_code, self.t_tushare_stock_today_tick_trade_data,
        #                                             volume_condition)

    # 获取股票指定日的小单交易金额
    def get_min_amt_date(self, stock_code, date):
        return self.get_stock_amt_by_size_and_date(stock_code, self.min_volume, date)

    # 获取股票指定日的中单交易金额
    def get_mid_amt_date(self, stock_code, date):
        return self.get_stock_amt_by_size_and_date(stock_code, self.mid_volume, date)

    # 获取股票指定日的大单交易金额
    def get_max_amt_date(self, stock_code, date):
        return self.get_stock_amt_by_size_and_date(stock_code, self.max_volume, date)

    # 获取股票指定日的超级大单交易金额
    def get_super_amt_date(self, stock_code, date):
        return self.get_stock_amt_by_size_and_date(stock_code, self.super_volume, date)

    # 根据交易量大小类型及交易日期， 获取股票对应交易金额数据
    def get_stock_amt_by_size_and_date(self, stock_code, volume_condition, date):
        return self.get_stock_amt_by_table_and_size(stock_code, self.t_tushare_stock_hist_tick_trade_data,
                                                    volume_condition, date)

    # 根据对应数据表、交易量大小类型、交易日期， 获取股票对应交易金额数据
    def get_stock_amt_by_table_and_size(self, stock_code, table_name, volume_condition, date=None):
        sql = "select sum(amount) as c from " + table_name + \
              " where code='" + stock_code + "' and volume " + volume_condition
        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票涨停价的交易金额
    def get_stock_amt_by_limit_up_price(self, stock_code, date, limit_up_value):
        # limit_up_value = self.get_stock_limit_up_value(stock_code)
        return self.get_stock_amt_by_price(stock_code, date, limit_up_value)

    # 获取股票跌停价的交易金额
    def get_stock_amt_by_limit_down_price(self, stock_code, date, limit_down_value):
        # limit_down_value = self.get_stock_limit_down_value(stock_code)
        return self.get_stock_amt_by_price(stock_code, date, limit_down_value)

    # 根据对应数据表、价格， 获取股票对应交易金额数据
    def get_stock_amt_by_price(self, stock_code, date, price):
        if date is None:
            date = self.get_latest_work_day()
        return self.get_stock_column_sum_by_table_and_price(
            stock_code, self.t_tushare_stock_today_tick_trade_data, "amount", price, date)

    # 获取股票涨停价的交易数量
    def get_stock_volume_by_limit_up_price(self, stock_code, date, limit_up_value):
        # limit_up_value = self.get_stock_limit_up_value(stock_code)
        return self.get_stock_volume_by_price(stock_code, date, limit_up_value)

    # 获取股票跌停价的交易数量
    def get_stock_volume_by_limit_down_price(self, stock_code, date, limit_down_value):
        # limit_down_value = self.get_stock_limit_down_value(stock_code)
        return self.get_stock_volume_by_price(stock_code, date, limit_down_value)

    # 根据对应数据表、价格， 获取股票对应交易数量数据
    def get_stock_volume_by_price(self, stock_code, date, price):
        if date is None:
            date = self.get_latest_work_day()
        return self.get_stock_column_sum_by_table_and_price(
            stock_code, self.t_tushare_stock_today_tick_trade_data, "volume", price, date)

    # 根据对应数据表、价格、交易日期， 获取股票对应字段的统计数
    def get_stock_column_sum_by_table_and_price(self, stock_code, table_name, column_name, price, date=None):
        sql = "select sum(" + column_name + ") as c from " + table_name + \
              " where code='" + stock_code + "' and price= " + str(price)
        if date is not None:
            sql = sql + " and date='" + date + "'"
        return self.count_sql_default_zero(sql)

    # 获取股票开盘集合竞价的交易数量
    def get_stock_volume_by_open_bid(self, stock_code, date):
        return self.get_stock_volume_by_order_time_and_limt(stock_code, date, self.asc, 1)

    # 获取股票闭盘集合竞价的交易数量
    def get_stock_volume_by_close_bid(self, stock_code, date):
        return self.get_stock_volume_by_order_time_and_limt(stock_code, date, self.desc, 1)

    def get_stock_volume_by_order_time_and_limt(self, stock_code, date, order, limit):
        if date is None:
            date = self.get_latest_work_day()
        return self.get_stock_column_sum_by_order_time_and_limt(stock_code, self.func_sum, "volume", order, limit, date)

    # 获取股票开盘集合竞价的交易金额
    def get_stock_amt_by_open_bid(self, stock_code, date):
        return self.get_stock_amt_by_order_time_and_limt(stock_code, date, self.asc, 1)

    # 获取股票闭盘集合竞价的交易金额
    def get_stock_amt_by_close_bid(self, stock_code, date):
        return self.get_stock_amt_by_order_time_and_limt(stock_code, date, self.desc, 1)

    def get_stock_amt_by_order_time_and_limt(self, stock_code, date, order, limit):
        if date is None:
            date = self.get_latest_work_day()
        return self.get_stock_column_sum_by_order_time_and_limt(stock_code, self.func_sum, "amount", order, limit, date)

    # 获取股票开盘集合竞价的交易类型
    def get_stock_trade_type_by_open_bid(self, stock_code, date):
        return self.get_stock_trade_type_by_order_time_and_limt(stock_code, date, self.asc, 1)

    # 获取股票闭盘集合竞价的交易类型
    def get_stock_trade_type_by_close_bid(self, stock_code, date):
        return self.get_stock_trade_type_by_order_time_and_limt(stock_code, date, self.desc, 1)

    def get_stock_trade_type_by_order_time_and_limt(self, stock_code, date, order, limit):
        if date is None:
            date = self.get_latest_work_day()
        return self.get_stock_column_sum_by_order_time_and_limt(stock_code, self.func_concat, "type", order, limit, date)

    # 根据对应交易日期，根据时间排序，及指定条数， 获取股票对应字段的统计数
    def get_stock_column_sum_by_order_time_and_limt(self, stock_code, func, column_name, order, limit, date=None):
        sql = "select "+func+"(" + column_name + ") as c from (" \
              "select * from " + self.t_tushare_stock_today_tick_trade_data + \
              " where code='" + stock_code + "' and volume > 0 "
        if date is not None:
            sql = sql + " and date='" + date + "'"
        sql = sql + "order by time " + order + " limit " + str(limit)
        sql = sql + ") as t "
        return self.count_sql_default_zero(sql)

    # 获取单笔最大买单交易数量
    def get_stock_single_max_buy_trade_volume(self, stock_code, date):
        return self.get_stock_column_func_value_by_date_and_type(
            stock_code, self.func_max, "volume", date, self.outside_dish)

    # 获取单笔最大买单交易金额
    def get_stock_single_max_buy_trade_amt(self, stock_code, date):
        return self.get_stock_column_func_value_by_date_and_type(
            stock_code, self.func_max, "amount", date, self.outside_dish)

    # 获取单笔最大买单交易时间
    def get_stock_single_max_buy_trade_time(self, stock_code, date):
        return self.get_stock_column_func_value_by_date_and_type(
            stock_code, self.func_max, "time", date, self.outside_dish)

    # 根据对应交易日期和交易类型，获取某个股票某个字段的函数计算值，如(max,min,avg)
    def get_stock_column_func_value_by_date_and_type(self, stock_code, func, column_name, date, trade_type):
        sql = "select " + func + "(" + column_name + ") as c from " + self.t_tushare_stock_today_tick_trade_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and type='" + trade_type + "'"
        return self.count_sql_default_zero(sql)

    # 获取交易日，某个股票，买票的最大交易金额记录
    def get_stock_buy_max_amt_trade_data_by_date(self, stock_code, date):
        return self.get_stock_max_amt_trade_data_by_date_and_type(stock_code, date, self.outside_dish)

    # 获取交易日，某个股票，卖盘的最大交易金额记录
    def get_stock_sell_max_amt_trade_data_by_date(self, stock_code, date):
        return self.get_stock_max_amt_trade_data_by_date_and_type(stock_code, date, self.inside_dish)

    # 获取交易日，某个股票，卖盘或买票的最大交易金额记录
    def get_stock_max_amt_trade_data_by_date_and_type(self, stock_code, date, trade_type):
        default_data = {"time": '', "volume": 0, "amount": 0}
        sql = "select time,volume,amount from " + self.t_tushare_stock_today_tick_trade_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and type='" + trade_type + "' " \
              "order by amount desc limit 1"
        data_list = self.select_sql(sql)
        if data_list is None:
            return default_data
        return data_list[0]

    # 根据相关条件获取全体的成交金额统计
    def get_all_day_trade_amt(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, None, trade_type)

    # 根据相关条件获取全体的成交量统计
    def get_all_day_trade_volume(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, None, trade_type)

    # 根据相关条件获取全体的成交次数统计
    def get_all_day_trade_count(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, None, trade_type)

    # 根据相关条件获取全体的成交次数统计
    def get_fixed_time_trade_count(self, stock_code, date, volume_condition, trade_type, times):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, times, trade_type)

    # 根据相关条件获取全体的交易平均价
    def get_all_day_avg_trade_price(self, stock_code, date, volume_condition, trade_type):
        amt = self.get_all_day_trade_amt(stock_code, date, volume_condition, trade_type)
        volume = self.get_all_day_trade_volume(stock_code, date, volume_condition, trade_type)
        return Decimal(str(self.cal_division_round_2(amt, volume*100)))

    # 根据相关条件获取全体的交易最小价
    def get_all_day_min_trade_price(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_min, "price", date, volume_condition, None, trade_type)

    # 根据相关条件获取全体的交易最大价
    def get_all_day_max_trade_price(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_max, "price", date, volume_condition, None, trade_type)

    # 获取早盘前部分的成交量统计
    def get_early_before_trade_volume(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, self.time_early_before, trade_type)

    # 获取早盘前部分的成交金额统计
    def get_early_before_trade_amt(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, self.time_early_before, trade_type)

    # 获取早盘前部分相关函数的成交价格统计
    def get_early_before_trade_price(self, stock_code, date, func):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, func, "price", date, None, self.time_early_before, None)

    # 获取早盘前部分的成交次数统计
    def get_early_before_trade_count(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, self.time_early_before, trade_type)

    # 获取早盘后部分的成交量统计
    def get_early_after_trade_volume(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, self.time_early_after, trade_type)

    # 获取早盘后部分的成交金额统计
    def get_early_after_trade_amt(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, self.time_early_after, trade_type)

    # 获取早盘后部分相关函数的成交价格统计
    def get_early_after_trade_price(self, stock_code, date, func):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, func, "price", date, None, self.time_early_after, None)

    # 获取早盘后部分的成交次数统计
    def get_early_after_trade_count(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, self.time_early_after, trade_type)

    # 获取午盘前部分的成交量统计
    def get_noon_before_trade_volume(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, self.time_noon_before, trade_type)

    # 获取午盘前部分的成交金额统计
    def get_noon_before_trade_amt(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, self.time_noon_before, trade_type)

    # 获取午盘前部分相关函数的成交价格统计
    def get_noon_before_trade_price(self, stock_code, date, func):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, func, "price", date, None, self.time_noon_before, None)

    # 获取午盘前部分的成交次数统计
    def get_noon_before_trade_count(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, self.time_noon_before, trade_type)

    # 获取午盘后部分的成交量统计
    def get_noon_after_trade_volume(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "volume", date, volume_condition, self.time_noon_after, trade_type)

    # 获取午盘后部分的成交金额统计
    def get_noon_after_trade_amt(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_sum, "amount", date, volume_condition, self.time_noon_after, trade_type)

    # 获取午盘后部分相关函数的成交价格统计
    def get_noon_after_trade_price(self, stock_code, date, func):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, func, "price", date, None, self.time_noon_after, None)

    # 获取午盘后部分的成交次数统计
    def get_noon_after_trade_count(self, stock_code, date, volume_condition, trade_type):
        return self.get_stock_column_func_value_by_date_time_and_volume_and_type(
            stock_code, self.func_count, "*", date, volume_condition, self.time_noon_after, trade_type)

    # 根据交易日、交易量大小类型、交易类型、时间点，获取某个列对应函数计算值
    def get_stock_column_func_value_by_date_time_and_volume_and_type(
            self, stock_code, func, column_name, date, volume_condition, time_condition, trade_type):
        sql = "select " + func + "(" + column_name + ") as c from " + self.t_tushare_stock_today_tick_trade_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' "
        if volume_condition is not None:
            sql = sql + " and volume " + volume_condition + " "
        if trade_type is not None:
            sql = sql + " and type='" + trade_type + "'"
        if time_condition is not None:
            sql = sql + " and time " + time_condition + " "
        return self.count_sql_default_zero(sql)

    # 获取早盘前部分股票的平均价格
    def get_early_before_avg_trade_price(self, stock_code, date):
        return self.get_stock_avg_trade_price_by_amount_divison_volume(stock_code, date, self.time_early_before)

    # 获取早盘后部分股票的平均价格
    def get_early_after_avg_trade_price(self, stock_code, date):
        return self.get_stock_avg_trade_price_by_amount_divison_volume(stock_code, date, self.time_early_after)

    # 获取午盘前部分股票的平均价格
    def get_noon_before_avg_trade_price(self, stock_code, date):
        return self.get_stock_avg_trade_price_by_amount_divison_volume(stock_code, date, self.time_noon_before)

    # 获取午盘后部分股票的平均价格
    def get_noon_after_avg_trade_price(self, stock_code, date):
        return self.get_stock_avg_trade_price_by_amount_divison_volume(stock_code, date, self.time_noon_after)

    # 交易金额/交易数量，获取平均价格
    def get_stock_avg_trade_price_by_amount_divison_volume(self, stock_code, date, time_condition):
        sql ="select round(sum(amount)/sum(volume*100),2) as c from " + self.t_tushare_stock_today_tick_trade_data + " " \
             "where code='" + stock_code + "' and date='" + date + "' "
        if time_condition is not None:
            sql = sql + " and time " + time_condition + " "
        return self.count_sql_default_zero(sql)

    # 获取大单交易类型时间分布
    def get_max_trade_distribution_time(self, stock_code, date):
        return self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.max_volume, None)

    # 获取超级大单交易类型时间分布
    def get_super_trade_distribution_time(self, stock_code, date):
        return self.get_stock_trade_distribution_time_by_trade_type(stock_code, date, self.super_volume, None)

    # 获取某种交易类型的交易时间分布情况
    def get_stock_trade_distribution_time_by_trade_type(self, stock_code, date, volume_condition, trade_type=None):
        sql_select = "select * from " + self.t_tushare_stock_today_tick_trade_data + " " \
                     "where code='" + stock_code + "' and date='" + date + "' and volume " + volume_condition + " "
        if trade_type is not None:
            sql_select = sql_select + " and type='" + trade_type + "'"

        sql = "select group_concat(time) as c from (" + " " \
              " " + sql_select + " "\
              " order by time asc ) as t"
        distribution_time = self.count_sql(sql)
        if distribution_time is None:
            distribution_time = ""
        distribution_time = self.encode(distribution_time)
        if len(distribution_time) > 512:
            distribution_time = distribution_time[0:512]
        return distribution_time

    # 获取股票连续涨跌相关数据
    def get_stock_continue_up_down_data(self, data):
        result_data = {"continue_up_down_days": 0, "contiune_up_down_percent": 0}
        if data is None:
            return result_data

        stock_code = data["code"]
        date = self.get_date_str(data["date"])
        change_percent = data["changepercent"]

        # newly_quotes_data = self.get_stock_newly_quotes_data(stock_code, date)
        # if newly_quotes_data is None:
        #     return result_data

        # change_percent = newly_quotes_data["changepercent"]
        if change_percent == 0:
            return result_data

        if change_percent > 0:
            up_data = self.get_stock_continue_up_down_data_by_up_down_type(stock_code, date, "<")
            return self.get_stock_continue_up_down_data_by_data(data, up_data)

        if change_percent < 0:
            down_data = self.get_stock_continue_up_down_data_by_up_down_type(stock_code, date, ">")
            return self.get_stock_continue_up_down_data_by_data(data, down_data)

        return result_data

    def get_stock_continue_up_down_data_by_data(self, newly_quotes_data, up_down_data):
        change_percent = newly_quotes_data["changepercent"]
        result_data = {"continue_up_down_days": 1, "contiune_up_down_percent": change_percent}
        if up_down_data is None:
            return result_data

        stock_code = newly_quotes_data["code"]
        date = self.get_date_str(newly_quotes_data["date"])
        newly_close_amt = newly_quotes_data["trade"]

        trade_date = self.get_date_str(up_down_data["trade_date"])
        pre_close_amt = up_down_data["pre_close_amt"]
        result_data["continue_up_down_days"] = self.get_stock_continue_up_down_count_by_trade_date(stock_code, trade_date, date) + 1
        result_data["contiune_up_down_percent"] = self.cal_percent_round_2(newly_close_amt - pre_close_amt, pre_close_amt)
        return result_data

    def get_stock_continue_up_down_data_by_up_down_type(self, stock_code, date, up_down_type):
        sql = "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where  code='" + stock_code + "' and trade_date<'" + date + "' and trade_date>"  \
              "(select trade_date from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where  code='" + stock_code + "' and trade_date<'" + date + "' and close_pre_close_diff_amt_ratio " \
              "" + up_down_type + " 0 order by trade_date desc limit 1) " \
              " order by trade_date asc limit 1 "
        data = self.select_one_sql(sql)
        if data is None:
            sql = "select count(*) as c from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
                  "where code='" + stock_code + "' and trade_date<'" + date + "' and close_pre_close_diff_amt_ratio " \
                   "" + up_down_type + " 0 "
            count_value = self.count_sql_default_zero(sql)
            if count_value <= 0:
                sql = "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
                      "where code='" + stock_code + "' and trade_date<'" + date + "' " \
                      "order by trade_date asc limit 1 "
                data = self.select_one_sql(sql)
        return data

    # 根据交易日获取股票连续涨跌的次数
    def get_stock_continue_up_down_count_by_trade_date(self, stock_code, begin_date, end_date):
        sql = "select count(*) as c from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where  code='" + stock_code + "' and trade_date between '" + begin_date + "' and '" + end_date + "' "
        return self.count_sql_default_zero(sql)

    def get_stock_newly_quotes_data(self, stock_code, date):
        sql = "select * from " + self.t_tushare_stock_newly_quotes_data + " " \
              "where code='" + stock_code + "' and date='" + date + "'"
        return self.select_one_sql(sql)

    # 获取非累计类原因的龙虎榜数据
    def get_stock_dragon_tiger_today_data(self, stock_code, date=None):
        return self.get_stock_dragon_tiger_data_by_reason_type(stock_code, " not like ", date)

    # 获取累计类原因的龙虎榜数据
    def get_stock_dragon_tiger_total_data(self, stock_code, date=None):
        return self.get_stock_dragon_tiger_data_by_reason_type(stock_code, " like ", date)

    # 根据原因类型获取龙虎榜数据
    def get_stock_dragon_tiger_data_by_reason_type(self, stock_code, reason_type, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select amount,buy,sell,reason,bratio as buy_percent,sratio as sell_percent, 1 as 'is_dragon_tiger' from " \
              + self.t_tushare_stock_dragon_tiger_today_data + " " \
              "where code ='" + stock_code + "' and date='" + date + "' and reason " + reason_type + " '%累计%' limit 1"
        data = self.select_one_sql(sql)
        if data is None:
            return {"amount":0,"buy":0, "sell":0, "reason":'', "buy_percent":0, "sell_percent":0, "is_dragon_tiger":0}
        return data

    # 获取非累计类原因的机构龙虎榜数据
    def get_stock_dragon_tiger_organ_today_data(self, stock_code, date=None):
        return self.get_stock_dragon_tiger_organ_data_by_reason_type(stock_code, "not like", date)

    # 获取累计类原因的机构龙虎榜数据
    def get_stock_dragon_tiger_organ_total_data(self, stock_code, date=None):
        return self.get_stock_dragon_tiger_organ_data_by_reason_type(stock_code, "like", date)

    # 根据原因类型获取龙虎榜数据
    def get_stock_dragon_tiger_organ_data_by_reason_type(self, stock_code, reason_type, date=None):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select bamount as buy,samount as sell,type as reason, 1 as 'is_dragon_tiger' from " \
              + self.t_tushare_stock_dragon_tiger_organ_today_data + " " \
              "where code ='" + stock_code + "' and date='" + date + "' and type " + reason_type + " '%累计%' limit 1"
        data = self.select_one_sql(sql)
        if data is None:
            return {"buy":0, "sell":0, "reason":'',  "is_dragon_tiger":0}
        return data

    # 获取某个股票N日内的龙虎榜统计数据
    def get_stock_dragon_tiger_n_day_data(self, stock_code, date, days):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select count as all_count,bamount+samount as all_amt,bcount as buy_count,bamount as buy_amt," \
              "scount as sell_count,samount as sell_amt,net as diff_amt  " \
              "from " + self.t_tushare_stock_dragon_tiger_total_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and days='" + str(days) + "' limit 1 "
        data = self.select_one_sql(sql)
        if data is None:
            return {"all_count":0, "all_amt":0, "buy_count":0, "buy_amt":0, "sell_count":0, "sell_amt":0, "diff_amt":0}
        return data

    # 获取某个股票N日内机构的龙虎榜统计数据
    def get_stock_dragon_tiger_organ_n_day_data(self, stock_code, date, days):
        if date is None:
            date = self.get_latest_work_day()
        sql = "select bcount as buy_count,bamount as buy_amt,scount as sell_count,samount as sell_amt,net as diff_amt " \
              "from " + self.t_tushare_stock_dragon_tiger_organ_total_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and days='" + str(days) + "' limit 1"
        data = self.select_one_sql(sql)
        if data is None:
            return {"all_count": 0, "all_amt": 0, "buy_count": 0, "buy_amt": 0, "sell_count": 0, "sell_amt": 0,
                    "diff_amt": 0}
        return data

    # 获取某个股票N日内进行该股票买卖的营业部名称
    def get_stock_dragon_tiger_sale_name_n_day_data(self, stock_name, date, days):
        sql = "select group_concat(broker) as c from (" \
              " select * from " + self.t_tushare_stock_dragon_tiger_sale_total_data + " " \
              " where date='" + date + "' and days=" + str(days) + " and top3 like '%" + stock_name +"%' " \
              " order by (bamount+samount) desc) as t "
        return self.count_sql_default_zero(sql)

    def insert_into_t_sunso_stock_day_trade_statistic_core_data(self, data):
        if self.is_exist_data(self.t_sunso_stock_day_trade_statistic_core_data, data):
            return
        sql = self.sql_handler.get_t_sunso_stock_day_trade_statistic_core_data_insert_sql(data)
        self.insert_sql(sql)

    def insert_into_t_sunso_stock_day_trade_statistic_volume_data(self, data):
        if self.is_exist_data(self.t_sunso_stock_day_trade_statistic_volume_data, data):
            return
        sql = self.sql_handler.get_t_sunso_stock_day_trade_statistic_volume_data_insert_sql(data)
        self.insert_sql(sql)

    def is_exist_data(self, table_name, data):
        sql = "select count(*) as c from " + table_name + " " \
              "where code='" + data["code"] + "' and trade_date='" + data["trade_date"] + "'"
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False

    def get_sum_amount_from_newly_quotes_data_hist_by_pre_two_date(self, data):
        data["limit"] = 2
        data["column"] = "sum(amount)"
        return self.select_column_from_newly_quotes_data_hist_by_pre_date(data)

    def get_circulation_amt_from_newly_quotes_data_hist_by_pre_one_date(self, data):
        data["limit"] = 1
        data["column"] = "nmc"
        return self.select_column_from_newly_quotes_data_hist_by_pre_date(data)

    def select_column_from_newly_quotes_data_hist_by_pre_date(self, data):
        sql = self.sql_handler.tp_select_column_from_newly_quotes_data_hist_by_pre_date(data)
        return self.count_sql_default_zero(sql)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的交易数量
    def get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "trade_volume", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的交易金额
    def get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "trade_amt", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的净流入金额
    def get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "trade_net_amt", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的交易价格
    def get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "close_amt", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的交易次数
    def get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "trade_count", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的每日平均交易量
    def get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "trade_per_avg_volume", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的换手率
    def get_avg_turnover_rate_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "turnover_rate", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的大额以上买盘交易金额比例
    def get_avg_large_above_buy_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "large_above_buy_trade_amt_ratio", days)

    # t_sunso_stock_day_trade_statistic_core_data 获取某股票N日内平均的大额以上卖盘交易金额比例
    def get_avg_large_above_sell_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, days):
        return self.get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date,  "large_above_sell_trade_amt_ratio", days)

    # t_sunso_stock_day_trade_statistic_core_data， 获取某个股票，某字段，N日内的平均值
    def get_avg_colum_value_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, column, days):
        str_days = str(days)
        sql = "select sum(" + column + ")/count(*)  as c from " \
              "(select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
               "where code='" + stock_code + "' and trade_date <'" + date + "' " \
               "order by trade_date desc limit " + str_days + ") as t"
        return self.count_sql_default_zero(sql)

    # 获取前一天的股票数据
    def get_pre_date_data_from_sunso_stock_day_trade_statistic_core(self, stock_code, date):
        sql = "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' order by trade_date desc limit 1"
        data = self.select_one_sql(sql)
        if data is None:
            return {"large_above_day1_bs_diff_trade_amt":0,"large_above_day3_bs_diff_trade_amt":0,"large_above_day5_bs_diff_trade_amt":0, "continue_down_limit_days":0, "continue_up_limit_days":0}
        return data

    # 获取前N天，当日大单及以上买盘和卖盘之间的差额的汇总值
    def get_pre_n_days_sum_large_above_bs_diff_trade_amt(self, stock_code, date, days):
        return self.get_pre_n_days_sum_value_from_sunso_stock_day_trade_statistic_core(stock_code, date, "sum(large_above_day1_bs_diff_trade_amt)", days)

    # 获取前N天的统计值
    def get_pre_n_days_sum_value_from_sunso_stock_day_trade_statistic_core(self, stock_code, date, column, days):
        sql = "select " + column + " as c from ("\
              "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' " \
              "order by trade_date desc limit " + str(days) + ") " \
              " as t "
        return self.count_sql_default_zero(sql)

    # 获取某个股票指定日期N天前的收盘价
    def get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(self, stock_code, date, days):
        str_days = str(days)
        sql_count = "select count(*) as c from (" \
                    "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
                    "where code='" + stock_code + "' and trade_date <'" + date + "' " \
                    "limit  " + str_days + ") as t "
        count_value = self.count_sql_default_zero(sql_count)
        if not count_value == days:
            return 0

        sql = "select close_amt as c from (" \
              "select * from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where code='" + stock_code + "' and trade_date <'" + date + "' " \
              "order by trade_date desc limit  " + str_days + ") as t order by trade_date asc limit 1"
        close_amt = self.count_sql_default_zero(sql)
        # return float(close_amt)
        return close_amt

    # 获取股票10点的交易数据
    def get_stock_ten_time_data_from_today_tick_trade_data(self, stock_code, date):
        sql = "select * from " + self.t_tushare_stock_today_tick_trade_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and time like '10:%' order by time asc limit 1"
        return self.select_one_sql(sql)

    # 获取10点的交易价格
    def get_stock_ten_time_price_from_today_tick_trade_data(self, stock_coe, date):
        data = self.get_stock_ten_time_data_from_today_tick_trade_data(stock_coe, date)
        if data is None:
            return 0
        return data["price"]

    # 是否涨停
    def is_up_limit(self, pre_close_amt, close_amt):
        up_limit_amt = self.get_stock_limit_up_value_by_pre_close_amt(pre_close_amt)
        if str(up_limit_amt) == str(round(close_amt, 2)):
            return True
        return False

    # 是否跌停
    def is_down_limit(self, pre_close_amt, close_amt):
        down_limit_amt = self.get_stock_limit_down_value_by_pre_close_amt(pre_close_amt)
        if str(down_limit_amt) == str(round(close_amt, 2)):
            return True
        return False

    # 获取涨停类型
    def get_up_limit_type(self, stock_code, date, pre_close_amt, close_amt, low_high_diff_amt):
        up_limit_type = 0
        if close_amt <= 0:
            return up_limit_type
        if not self.is_up_limit(pre_close_amt, close_amt):
            return up_limit_type

        up_limit_type = 10
        if low_high_diff_amt == 0:
            up_limit_type = 30
            return up_limit_type

        up_limit_amt = self.get_stock_limit_up_value_by_pre_close_amt(pre_close_amt)
        if self.is_continue_price_by_after_time(stock_code, date, up_limit_amt):
            up_limit_type = 20

        return up_limit_type

    # 获取跌停类型
    def get_down_limit_type(self, stock_code, date, pre_close_amt, close_amt, low_high_diff_amt):
        down_limit_type = 0
        if close_amt <= 0:
            return down_limit_type

        if not self.is_down_limit(pre_close_amt, close_amt):
            return down_limit_type

        down_limit_type = 10
        if low_high_diff_amt == 0:
            down_limit_type = 30
            return down_limit_type

        down_limit_amt = self.get_stock_limit_down_value_by_pre_close_amt(pre_close_amt)
        if self.is_continue_price_by_after_time(stock_code, date, down_limit_amt):
            down_limit_type = 20

        return down_limit_type

    # 某个时间点之后是否是只出现某个价格交易
    def is_continue_price_by_after_time(self, stock_code, date, price):
        sql = "select count(*) as c from " + self.t_tushare_stock_today_tick_trade_data + " " \
              "where code='" + stock_code + "' and date='" + date + "' and time>'10:30:00' and price<>" + str(price)
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return False
        return True

    # 获取连续涨停天数
    def get_continue_up_limit_days(self, stock_code, date, up_limit_type):
        if up_limit_type < 1:
            return 0
        pre_up_limit_days = 0
        data = self.get_pre_date_data_from_sunso_stock_day_trade_statistic_core(stock_code, date)
        if data is not None:
            pre_up_limit_days = data["continue_up_limit_days"]
        if pre_up_limit_days < 0:
            pre_up_limit_days = 0
        return pre_up_limit_days + 1

    # 获取连续跌停天数
    def get_continue_down_limit_days(self, stock_code, date, down_limit_type):
        if down_limit_type < 1:
            return 0
        pre_down_limit_days = 0
        data = self.get_pre_date_data_from_sunso_stock_day_trade_statistic_core(stock_code, date)
        if data is not None:
            pre_down_limit_days = data["continue_down_limit_days"]
        if pre_down_limit_days < 0:
            pre_down_limit_days = 0
        return pre_down_limit_days + 1

    # 获取某只股票统计的核心数据
    def get_one_stock_statistic_core_data(self, data):
        if data is None:
            return data
        close_amt = data["trade"]
        # 没有收盘价，停牌的时候，不进行数据的处理
        if close_amt <= 0:
            return
        date = data["date"]
        if isinstance(date, datetime.date):
            date = self.get_date_str(date)
        data["trade_date"] = date
        stock_code = data["code"]
        change_percent = data["changepercent"]
        open_amt = data["open"]
        low_amt = data["low"]
        high_amt = data["high"]
        trade_volume = data["volume"]
        market_cap_amt = 0
        market_cap_amt_key = "mktcap"
        if market_cap_amt_key in data.keys():
            market_cap_amt = data[market_cap_amt_key]
        data["market_cap_amt"] = market_cap_amt

        circulation_amt = 0
        circulation_amt_key = "nmc"
        if circulation_amt_key in data.keys():
            circulation_amt = data[circulation_amt_key]
        data["circulation_amt"] = circulation_amt

        sum_trade_volume = self.get_stock_today_sum_volume(stock_code, date)
        sum_trade_amt = self.get_stock_today_sum_amt(stock_code, date)
        sunso_stock_baise = self.get_one_sunso_stock_basic(stock_code, date)

        name_key = "name"
        if name_key not in data.keys():
            data[name_key] = sunso_stock_baise[name_key]
        name = data[name_key]
        data["industry"] = sunso_stock_baise["industry"]
        data["area"] = sunso_stock_baise["area"]
        data["open_amt"] = open_amt
        data["close_amt"] = close_amt
        data["low_amt"] = low_amt
        data["high_amt"] = high_amt
        data["avg_amt"] = self.cal_division_round_2(sum_trade_amt, sum_trade_volume*100)

        settlement_key = "settlement"
        if settlement_key in data.keys():
            pre_close_amt = data[settlement_key]
        else:
            pre_close_amt = Decimal(self.cal_division_round_2(close_amt, (1 + change_percent / 100)))
            # Decimal(round(close_amt / (1 + change_percent / 100), 2))
        data["pre_close_amt"] = pre_close_amt

        data["close_pre_close_diff_amt_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_close_amt)
        data["open_pre_close_diff_amt_ratio"] = self.cal_percent_round_2_not_zero(open_amt, pre_close_amt)
        data["low_pre_close_diff_amt_ratio"] = self.cal_percent_round_2_not_zero(low_amt, pre_close_amt)
        data["high_pre_close_diff_amt_ratio"] = self.cal_percent_round_2_not_zero(high_amt, pre_close_amt)
        low_high_diff_amt = high_amt - low_amt
        data["low_high_diff_amt_ratio"] = self.cal_percent_round_2(high_amt - low_amt, pre_close_amt)
        ten_time_price = Decimal(self.get_stock_ten_time_price_from_today_tick_trade_data(stock_code, date))
        data["open_ten_time_ratio"] = self.cal_percent_round_2(ten_time_price - open_amt, open_amt)
        data["ten_tine_close_ratio"] = self.cal_percent_round_2(close_amt - ten_time_price, ten_time_price)

        pre1_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 1)
        pre3_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 3)
        pre5_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 5)
        pre10_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 10)
        pre20_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 20)
        pre30_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 30)
        pre60_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 60)
        pre90_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 90)
        pre120_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 120)
        pre250_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 250)
        pre365_close_price = self.get_close_price_from_sunso_stock_day_trade_statistic_core_by_date_and_limit(stock_code, date, 365)

        data["pre1_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre1_close_price)
        data["pre3_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre3_close_price)
        data["pre5_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre5_close_price)
        data["pre10_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre10_close_price)
        data["pre20_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre20_close_price)
        data["pre30_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre30_close_price)
        data["pre60_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre60_close_price)
        data["pre90_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre90_close_price)
        data["pre120_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre120_close_price)
        data["pre250_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre250_close_price)
        data["pre365_close_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre365_close_price)

        up_limit_type = self.get_up_limit_type(stock_code, date, pre_close_amt, close_amt, low_high_diff_amt)
        down_limit_type = self.get_down_limit_type(stock_code, date, pre_close_amt, close_amt, low_high_diff_amt)
        data["up_limit_type"] = up_limit_type
        data["down_limit_type"] = down_limit_type
        limit_up_price = self.get_stock_limit_up_value_by_pre_close_amt(pre_close_amt)
        limit_down_price = self.get_stock_limit_down_value_by_pre_close_amt(pre_close_amt)
        data["first_limit_up_time"] = self.get_stock_first_limit_up_time(stock_code, date, limit_up_price)
        data["first_limit_down_time"] = self.get_stock_first_limit_down_time(stock_code, date, limit_down_price)
        data["continue_up_limit_days"] = self.get_continue_up_limit_days(stock_code, date, up_limit_type)
        data["continue_down_limit_days"] = self.get_continue_down_limit_days(stock_code, date, down_limit_type)
        continue_up_down_data = self.get_stock_continue_up_down_data(data)
        data["continue_up_down_days"] = str(continue_up_down_data["continue_up_down_days"])
        data["contiune_up_down_percent"] = str(round(continue_up_down_data["contiune_up_down_percent"], 2))

        turnoverratio_key = "turnoverratio"
        if turnoverratio_key in data.keys():
            turnover_rate = data[turnoverratio_key]
        else:
            turnover_rate = str(self.cal_percent_round_2(
                trade_volume, sunso_stock_baise["circulation_stock_volume"]*self.unit_hundred_million))
        data["turnover_rate"] = turnover_rate

        pre1_avg_turnover_rate = self.get_avg_turnover_rate_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre3_avg_turnover_rate = self.get_avg_turnover_rate_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre5_avg_turnover_rate = self.get_avg_turnover_rate_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)

        data["pre1_avg_turnover_rate_ratio"] = self.cal_division_round_2(turnover_rate, pre1_avg_turnover_rate)
        data["pre3_avg_turnover_rate_ratio"] = self.cal_division_round_2(turnover_rate, pre3_avg_turnover_rate)
        data["pre5_avg_turnover_rate_ratio"] = self.cal_division_round_2(turnover_rate, pre5_avg_turnover_rate)

        data["trade_volume"] = trade_volume

        amount_key = "amount"
        if amount_key in data.keys():
            trade_amt = data["amount"]
        else:
            trade_amt = sum_trade_amt
        data["trade_amt"] = trade_amt

        trade_count = self.get_all_count(stock_code, date)
        trade_per_avg_volume = Decimal(self.cal_division_round_2(trade_volume, trade_count))
            #Decimal(trade_volume / trade_count)
        data["trade_count"] = trade_count
        data["trade_per_avg_volume"] = trade_per_avg_volume
        pre_day_circulation_amt = self.get_circulation_amt_from_newly_quotes_data_hist_by_pre_one_date(data)
        if pre_day_circulation_amt < 1:
            pre_day_circulation_amt = circulation_amt
        trade_net_amt = circulation_amt - pre_day_circulation_amt
        data["trade_net_amt"] = trade_net_amt

        pre_avg1_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre_avg3_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre_avg5_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        pre_avg10_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10)
        pre_avg20_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20)
        pre_avg30_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30)
        pre_avg60_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60)
        pre_avg90_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90)
        pre_avg120_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120)
        pre_avg250_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250)
        pre_avg365_trade_price = self.get_avg_trade_price_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365)

        data["pre_avg1_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg1_trade_price)
        data["pre_avg3_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg3_trade_price)
        data["pre_avg5_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg5_trade_price)
        data["pre_avg10_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg10_trade_price)
        data["pre_avg20_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg20_trade_price)
        data["pre_avg30_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg30_trade_price)
        data["pre_avg60_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg60_trade_price)
        data["pre_avg90_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg90_trade_price)
        data["pre_avg120_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg120_trade_price)
        data["pre_avg250_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg250_trade_price)
        data["pre_avg365_trade_price_ratio"] = self.cal_percent_round_2_not_zero(close_amt, pre_avg365_trade_price)

        pre_avg1_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre_avg3_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre_avg5_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        pre_avg10_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10)
        pre_avg20_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20)
        pre_avg30_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30)
        pre_avg60_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60)
        pre_avg90_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90)
        pre_avg120_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120)
        pre_avg250_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250)
        pre_avg365_trade_amt = self.get_avg_trade_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365)

        data["pre_avg1_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg1_trade_amt)
        data["pre_avg3_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg3_trade_amt)
        data["pre_avg5_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg5_trade_amt)
        data["pre_avg10_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg10_trade_amt)
        data["pre_avg20_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg20_trade_amt)
        data["pre_avg30_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg30_trade_amt)
        data["pre_avg60_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg60_trade_amt)
        data["pre_avg90_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg90_trade_amt)
        data["pre_avg120_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg120_trade_amt)
        data["pre_avg250_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg250_trade_amt)
        data["pre_avg365_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(trade_amt, pre_avg365_trade_amt)

        pre_avg1_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1))
        pre_avg3_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3))
        pre_avg5_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5))
        pre_avg10_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10))
        pre_avg20_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20))
        pre_avg30_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30))
        pre_avg60_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60))
        pre_avg90_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90))
        pre_avg120_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120))
        pre_avg250_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250))
        pre_avg365_trade_net_amt = abs(self.get_avg_trade_net_amt_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365))
        abs_trade_net_amt = abs(trade_net_amt)

        data["pre_avg1_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg1_trade_net_amt)
        data["pre_avg3_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg3_trade_net_amt)
        data["pre_avg5_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg5_trade_net_amt)
        data["pre_avg10_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg10_trade_net_amt)
        data["pre_avg20_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg20_trade_net_amt)
        data["pre_avg30_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg30_trade_net_amt)
        data["pre_avg60_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg60_trade_net_amt)
        data["pre_avg90_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg90_trade_net_amt)
        data["pre_avg120_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg120_trade_net_amt)
        data["pre_avg250_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg250_trade_net_amt)
        data["pre_avg365_trade_net_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_trade_net_amt, pre_avg365_trade_net_amt)

        pre_avg1_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre_avg3_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre_avg5_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        pre_avg10_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10)
        pre_avg20_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20)
        pre_avg30_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30)
        pre_avg60_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60)
        pre_avg90_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90)
        pre_avg120_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120)
        pre_avg250_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250)
        pre_avg365_trade_volume = self.get_avg_trade_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365)

        data["pre_avg1_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg1_trade_volume)
        data["pre_avg3_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg3_trade_volume)
        data["pre_avg5_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg5_trade_volume)
        data["pre_avg10_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg10_trade_volume)
        data["pre_avg20_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg20_trade_volume)
        data["pre_avg30_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg30_trade_volume)
        data["pre_avg60_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg60_trade_volume)
        data["pre_avg90_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg90_trade_volume)
        data["pre_avg120_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg120_trade_volume)
        data["pre_avg250_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg250_trade_volume)
        data["pre_avg365_trade_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_volume, pre_avg365_trade_volume)

        pre_avg1_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre_avg3_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre_avg5_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        pre_avg10_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10)
        pre_avg20_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20)
        pre_avg30_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30)
        pre_avg60_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60)
        pre_avg90_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90)
        pre_avg120_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120)
        pre_avg250_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250)
        pre_avg365_trade_count = self.get_avg_trade_count_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365)

        data["pre_avg1_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg1_trade_count)
        data["pre_avg3_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg3_trade_count)
        data["pre_avg5_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg5_trade_count)
        data["pre_avg10_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg10_trade_count)
        data["pre_avg20_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg20_trade_count)
        data["pre_avg30_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg30_trade_count)
        data["pre_avg60_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg60_trade_count)
        data["pre_avg90_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg90_trade_count)
        data["pre_avg120_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg120_trade_count)
        data["pre_avg250_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg250_trade_count)
        data["pre_avg365_trade_count_ratio"] = self.cal_percent_round_2_not_zero(trade_count, pre_avg365_trade_count)

        pre_avg1_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre_avg3_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre_avg5_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        pre_avg10_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 10)
        pre_avg20_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 20)
        pre_avg30_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 30)
        pre_avg60_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 60)
        pre_avg90_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 90)
        pre_avg120_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 120)
        pre_avg250_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 250)
        pre_avg365_trade_per_avg_volume = self.get_avg_trade_per_avg_volume_from_sunso_stock_day_trade_statistic_core(stock_code, date, 365)

        data["pre_avg1_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume,  pre_avg1_trade_per_avg_volume)
        data["pre_avg3_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg3_trade_per_avg_volume)
        data["pre_avg5_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg5_trade_per_avg_volume)
        data["pre_avg10_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg10_trade_per_avg_volume)
        data["pre_avg20_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg20_trade_per_avg_volume)
        data["pre_avg30_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg30_trade_per_avg_volume)
        data["pre_avg60_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg60_trade_per_avg_volume)
        data["pre_avg90_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg90_trade_per_avg_volume)
        data["pre_avg120_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg120_trade_per_avg_volume)
        data["pre_avg250_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg250_trade_per_avg_volume)
        data["pre_avg365_trade_per_avg_volume_ratio"] = self.cal_percent_round_2_not_zero(trade_per_avg_volume, pre_avg365_trade_per_avg_volume)

        dragon_tiger_today = self.get_stock_dragon_tiger_today_data(stock_code, date)
        dragon_tiger_organ_today = self.get_stock_dragon_tiger_organ_today_data(stock_code, date)

        data["dragon_tiger_today_is"] = dragon_tiger_today["is_dragon_tiger"]
        data["dragon_tiger_today_reason"] = dragon_tiger_today["reason"]
        dragon_tiger_all_today_amt = dragon_tiger_today["amount"]
        data["dragon_tiger_all_today_amt"] = dragon_tiger_all_today_amt
        dragon_tiger_all_today_buy_amt = dragon_tiger_today["buy"]
        dragon_tiger_all_today_sell_amt = dragon_tiger_today["sell"]
        dragon_tiger_organ_today_buy_amt = dragon_tiger_organ_today["buy"]
        dragon_tiger_organ_today_sell_amt = dragon_tiger_organ_today["sell"]
        dragon_tiger_sale_today_buy_amt = dragon_tiger_all_today_buy_amt - dragon_tiger_organ_today_buy_amt
        dragon_tiger_sale_today_sell_amt = dragon_tiger_all_today_sell_amt - dragon_tiger_organ_today_sell_amt

        today_sum_amt = Decimal(self.cal_division_round_2(trade_amt, 10000))
        data["dragon_tiger_all_today_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_all_today_amt, today_sum_amt)
        data["dragon_tiger_all_today_buy_amt_ratio"] = dragon_tiger_today["buy_percent"] * 100
        data["dragon_tiger_all_today_sell_amt_ratio"] = dragon_tiger_today["sell_percent"] * 100
        data["dragon_tiger_organ_today_buy_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_organ_today_buy_amt, today_sum_amt)
        data["dragon_tiger_organ_today_sell_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_organ_today_sell_amt, today_sum_amt)
        data["dragon_tiger_sale_today_buy_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_sale_today_buy_amt, today_sum_amt)
        data["dragon_tiger_sale_today_sell_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_sale_today_sell_amt, today_sum_amt)

        dragon_tiger_total = self.get_stock_dragon_tiger_total_data(stock_code, date)
        dragon_tiger_organ_total = self.get_stock_dragon_tiger_organ_total_data(stock_code, date)

        data["dragon_tiger_total_is"] = dragon_tiger_total["is_dragon_tiger"]
        data["dragon_tiger_total_reason"] = dragon_tiger_total["reason"]
        dragon_tiger_all_total_amt = dragon_tiger_total["amount"]
        data["dragon_tiger_all_total_amt"] = dragon_tiger_all_total_amt
        dragon_tiger_all_total_buy_amt = dragon_tiger_total["buy"]
        dragon_tiger_all_total_sell_amt = dragon_tiger_total["sell"]
        dragon_tiger_organ_total_buy_amt = dragon_tiger_organ_total["buy"]
        dragon_tiger_organ_total_sell_amt = dragon_tiger_organ_total["sell"]
        dragon_tiger_sale_total_buy_amt = dragon_tiger_all_total_buy_amt - dragon_tiger_organ_total_buy_amt
        dragon_tiger_sale_total_sell_amt = dragon_tiger_all_total_sell_amt - dragon_tiger_organ_total_sell_amt

        total_sum_amt = (self.get_sum_amount_from_newly_quotes_data_hist_by_pre_two_date(data) + trade_amt) / 10000
        data["dragon_tiger_all_total_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_all_total_amt, total_sum_amt)
        data["dragon_tiger_all_total_buy_amt_ratio"] = dragon_tiger_total["buy_percent"] * 100
        data["dragon_tiger_all_total_sell_amt_ratio"] = dragon_tiger_total["sell_percent"] * 100

        data["dragon_tiger_organ_total_buy_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_organ_total_buy_amt, total_sum_amt)
        data["dragon_tiger_organ_total_sell_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_organ_total_sell_amt, total_sum_amt)
        data["dragon_tiger_sale_total_buy_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_sale_total_buy_amt, total_sum_amt)
        data["dragon_tiger_sale_total_sell_amt_ratio"] = self.cal_percent_round_2(dragon_tiger_sale_total_sell_amt, total_sum_amt)

        n_day_data = self.get_stock_dragon_tiger_n_day_data(stock_code, date, 5)
        organ_n_day_data = self.get_stock_dragon_tiger_organ_n_day_data(stock_code, date, 5)

        data["dragon_tiger_all_5day_count"] = n_day_data["all_count"]
        dragon_tiger_all_5day_buy_amt = n_day_data["buy_amt"]
        dragon_tiger_all_5day_sell_amt = n_day_data["sell_amt"]
        data["dragon_tiger_all_5day_bs_amt_percent"] = self.cal_percent_round_2(dragon_tiger_all_5day_buy_amt, dragon_tiger_all_5day_sell_amt)
        dragon_tiger_all_5day_buy_count = n_day_data["buy_count"]
        dragon_tiger_all_5day_sell_count = n_day_data["sell_count"]
        data["dragon_tiger_all_5day_bs_count_percent"] = self.cal_percent_round_2(dragon_tiger_all_5day_buy_count, dragon_tiger_all_5day_sell_count)
        data["dragon_tiger_all_5day_bs_diff_amt"] = n_day_data["diff_amt"]

        dragon_tiger_organ_5day_buy_amt = organ_n_day_data["buy_amt"]
        dragon_tiger_organ_5day_sell_amt = organ_n_day_data["sell_amt"]
        data["dragon_tiger_organ_5day_bs_amt_percent"] = self.cal_percent_round_2(dragon_tiger_organ_5day_buy_amt, dragon_tiger_organ_5day_sell_amt)
        dragon_tiger_organ_5day_buy_count = organ_n_day_data["buy_count"]
        dragon_tiger_organ_5day_sell_count = organ_n_day_data["sell_count"]
        data["dragon_tiger_organ_5day_bs_count_percent"] = self.cal_percent_round_2(dragon_tiger_organ_5day_buy_count, dragon_tiger_organ_5day_sell_count)
        data["dragon_tiger_organ_5day_bs_diff_amt"] = organ_n_day_data["diff_amt"]
        data["dragon_tiger_sale_5day_name"] = self.get_stock_dragon_tiger_sale_name_n_day_data(name, date, 5)

        small_sum_trade_amt = self.get_min_amt(stock_code, date)
        medium_sum_trade_amt = self.get_mid_amt(stock_code, date)
        large_sum_trade_amt = self.get_max_amt(stock_code, date)
        super_sum_trade_amt = self.get_super_amt(stock_code, date)
        large_above_sum_trade_amt = large_sum_trade_amt + super_sum_trade_amt
        sum_trade_amt = small_sum_trade_amt + medium_sum_trade_amt + large_sum_trade_amt + super_sum_trade_amt

        data["small_sum_trade_amt_ratio"] = self.cal_percent_round_2(small_sum_trade_amt, sum_trade_amt)
        data["medium_sum_trade_amt_ratio"] = self.cal_percent_round_2(medium_sum_trade_amt, sum_trade_amt)
        data["large_sum_trade_amt_ratio"] = self.cal_percent_round_2(large_sum_trade_amt, sum_trade_amt)
        data["super_sum_trade_amt_ratio"] = self.cal_percent_round_2(super_sum_trade_amt, sum_trade_amt)
        data["large_above_sum_trade_amt_ratio"] = self.cal_percent_round_2(large_above_sum_trade_amt, sum_trade_amt)

        inside_dish_sum_amt = self.get_inside_dish_amt(stock_code, date)
        outside_dish_sum_amt = self.get_outside_dish_amt(stock_code, date)
        midside_dish_sum_amt = self.get_midside_dish_amt(stock_code, date)
        data["inside_dish_sum_amt_ratio"] = self.cal_percent_round_2(inside_dish_sum_amt, sum_trade_amt)
        data["outside_dish_sum_amt_ratio"] = self.cal_percent_round_2(outside_dish_sum_amt, sum_trade_amt)
        data["midside_dish_sum_amt_ratio"] = self.cal_percent_round_2(midside_dish_sum_amt, sum_trade_amt)

        small_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.min_volume, None)
        small_avg_buy_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.min_volume, self.outside_dish)
        small_avg_sell_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.min_volume, self.inside_dish)
        large_above_avg_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, None)
        large_above_avg_buy_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, self.outside_dish)
        large_above_avg_sell_trade_price = self.get_all_day_avg_trade_price(stock_code, date, self.large_above, self.inside_dish)
        data["small_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_avg_trade_price, close_amt)
        data["small_avg_buy_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_avg_buy_trade_price, close_amt)
        data["small_avg_sell_trade_price_ratio"] = self.cal_percent_round_2_not_zero(small_avg_sell_trade_price, close_amt)
        data["large_above_avg_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_avg_trade_price, close_amt)
        data["large_above_avg_buy_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_avg_buy_trade_price, close_amt)
        data["large_above_avg_sell_trade_price_ratio"] = self.cal_percent_round_2_not_zero(large_above_avg_sell_trade_price, close_amt)

        small_inside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.min_volume, self.inside_dish)
        small_outside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.min_volume, self.outside_dish)
        medium_inside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.mid_volume, self.inside_dish)
        medium_outside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.mid_volume, self.outside_dish)
        large_inside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.max_volume, self.inside_dish)
        large_outside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.max_volume, self.outside_dish)
        super_inside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.super_volume, self.inside_dish)
        super_outside_sum_trade_amt = self.get_all_day_trade_amt(stock_code, date, self.super_volume, self.outside_dish)
        data["small_inside_sum_trade_amt_ratio"] = self.cal_percent_round_2(small_inside_sum_trade_amt, small_sum_trade_amt)
        data["small_outside_sum_trade_amt_ratio"] = self.cal_percent_round_2(small_outside_sum_trade_amt, small_sum_trade_amt)
        data["medium_inside_sum_trade_amt_ratio"] = self.cal_percent_round_2(medium_inside_sum_trade_amt, medium_sum_trade_amt)
        data["medium_outside_sum_trade_amt_ratio"] = self.cal_percent_round_2(medium_outside_sum_trade_amt, medium_sum_trade_amt)
        data["large_inside_sum_trade_amt_ratio"] = self.cal_percent_round_2(large_inside_sum_trade_amt, large_sum_trade_amt)
        data["large_outside_sum_trade_amt_ratio"] = self.cal_percent_round_2(large_outside_sum_trade_amt, large_sum_trade_amt)
        data["super_inside_sum_trade_amt_ratio"] = self.cal_percent_round_2(super_inside_sum_trade_amt, super_sum_trade_amt)
        data["super_outside_sum_trade_amt_ratio"] = self.cal_percent_round_2(super_outside_sum_trade_amt, super_sum_trade_amt)

        large_above_buy_trade_amt = large_outside_sum_trade_amt + super_outside_sum_trade_amt
        large_above_sell_trade_amt = large_inside_sum_trade_amt + super_inside_sum_trade_amt
        data["small_buy_trade_amt_ratio"] = self.cal_percent_round_2(small_outside_sum_trade_amt, sum_trade_amt)
        data["small_sell_trade_amt_ratio"] = self.cal_percent_round_2(small_inside_sum_trade_amt, sum_trade_amt)
        large_above_buy_trade_amt_ratio = Decimal(str(self.cal_percent_round_2(large_above_buy_trade_amt, sum_trade_amt)))
        data["large_above_buy_trade_amt_ratio"] = large_above_buy_trade_amt_ratio
        pre1_avg_large_above_buy_trade_amt_ratio = self.get_avg_large_above_buy_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date ,1)
        pre3_avg_large_above_buy_trade_amt_ratio = self.get_avg_large_above_buy_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre5_avg_large_above_buy_trade_amt_ratio = self.get_avg_large_above_buy_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        data["pre1_avg_large_above_buy_trade_amt_ratio"] = self.cal_division_round_2(large_above_buy_trade_amt_ratio, pre1_avg_large_above_buy_trade_amt_ratio)
        data["pre3_avg_large_above_buy_trade_amt_ratio"] = self.cal_division_round_2(large_above_buy_trade_amt_ratio, pre3_avg_large_above_buy_trade_amt_ratio)
        data["pre5_avg_large_above_buy_trade_amt_ratio"] = self.cal_division_round_2(large_above_buy_trade_amt_ratio, pre5_avg_large_above_buy_trade_amt_ratio)

        large_above_sell_trade_amt_ratio = Decimal(str(self.cal_percent_round_2(large_above_sell_trade_amt, sum_trade_amt)))
        data["large_above_sell_trade_amt_ratio"] = large_above_sell_trade_amt_ratio
        pre1_avg_large_above_sell_trade_amt_ratio = self.get_avg_large_above_sell_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date, 1)
        pre3_avg_large_above_sell_trade_amt_ratio = self.get_avg_large_above_sell_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date, 3)
        pre5_avg_large_above_sell_trade_amt_ratio = self.get_avg_large_above_sell_trade_amt_ratio_from_sunso_stock_day_trade_statistic_core(stock_code, date, 5)
        data["pre1_avg_large_above_sell_trade_amt_ratio"] = self.cal_division_round_2(large_above_sell_trade_amt_ratio, pre1_avg_large_above_sell_trade_amt_ratio)
        data["pre3_avg_large_above_sell_trade_amt_ratio"] = self.cal_division_round_2(large_above_sell_trade_amt_ratio, pre3_avg_large_above_sell_trade_amt_ratio)
        data["pre5_avg_large_above_sell_trade_amt_ratio"] = self.cal_division_round_2(large_above_sell_trade_amt_ratio, pre5_avg_large_above_sell_trade_amt_ratio)

        data["large_above_bs_trade_amt_ratio"] = self.cal_division_round_2(large_above_buy_trade_amt, large_above_sell_trade_amt)

        large_above_bs_diff_trade_amt = large_above_buy_trade_amt - large_above_sell_trade_amt
        pre_2_days_sum_large_above_bs_diff_trade_amt = self.get_pre_n_days_sum_large_above_bs_diff_trade_amt(stock_code, date, 2)
        pre_4_days_sum_large_above_bs_diff_trade_amt = self.get_pre_n_days_sum_large_above_bs_diff_trade_amt(stock_code, date, 4)
        large_above_day3_bs_diff_trade_amt = large_above_bs_diff_trade_amt + pre_2_days_sum_large_above_bs_diff_trade_amt
        large_above_day5_bs_diff_trade_amt = large_above_bs_diff_trade_amt + pre_4_days_sum_large_above_bs_diff_trade_amt
        pre_trade_statistic_core_data = self.get_pre_date_data_from_sunso_stock_day_trade_statistic_core(stock_code, date)
        pre_large_above_bs_diff_trade_amt = abs(pre_trade_statistic_core_data["large_above_day1_bs_diff_trade_amt"])
        pre_large_above_day3_bs_diff_trade_amt = abs(pre_trade_statistic_core_data["large_above_day3_bs_diff_trade_amt"])
        pre_large_above_day5_bs_diff_trade_amt = abs(pre_trade_statistic_core_data["large_above_day5_bs_diff_trade_amt"])
        abs_large_above_bs_diff_trade_amt = abs(large_above_bs_diff_trade_amt)
        abs_large_above_day3_bs_diff_trade_amt = abs(large_above_day3_bs_diff_trade_amt)
        abs_large_above_day5_bs_diff_trade_amt = abs(large_above_day5_bs_diff_trade_amt)

        data["large_above_day1_bs_diff_trade_amt"] = large_above_bs_diff_trade_amt
        data["large_above_day3_bs_diff_trade_amt"] = large_above_day3_bs_diff_trade_amt
        data["large_above_day5_bs_diff_trade_amt"] = large_above_day5_bs_diff_trade_amt
        data["large_above_day1_bs_diff_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_large_above_bs_diff_trade_amt, pre_large_above_bs_diff_trade_amt)
        data["large_above_day3_bs_diff_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_large_above_day3_bs_diff_trade_amt, pre_large_above_day3_bs_diff_trade_amt)
        data["large_above_day5_bs_diff_trade_amt_ratio"] = self.cal_percent_round_2_not_zero(abs_large_above_day5_bs_diff_trade_amt, pre_large_above_day5_bs_diff_trade_amt)

        return data


    def get_now_ymd(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def data_to_db_append(self, data, table_name):
        print(data)
        self.data_to_db(data, table_name, "append")

    def data_to_db(self, data, table_name, append_type):
        if data is None:
            print("data_to_db input data parameter is empty")
            return
        data.to_sql(table_name, TushareBase.db_engine, if_exists=append_type)

    def delete_sql(self, sql):
        TushareBase.db_execute.dml(sql)

    def insert_sql(self, sql):
        TushareBase.db_execute.dml(sql)

    def update_sql(self, sql):
        TushareBase.db_execute.dml(sql)

    def select_sql(self, sql):
        # print(sql)
        data_list = TushareBase.db_execute.select(sql)
        if len(data_list) < 1:
            return None
        self.convert_dict_list_unicode_to_str(data_list)
        return data_list

    def select_one_sql(self, sql):
        data_list = self.select_sql(sql)
        if data_list is None:
            return data_list
        return data_list[0]

    def count_sql(self, sql):
        data = TushareBase.db_execute.select(sql)
        if len(data) < 1:
            return None
        count = data[0]["c"]
        if isinstance(count, unicode):
            count = self.encode(count)
        # self.log_info("count result-->" + str(count))
        return count

    def count_sql_default_zero(self, sql):
        value = self.count_sql(sql)
        if value is None:
            value = 0
        return value

    def is_exist_data_sql(self, sql):
        count_value = self.count_sql(sql)
        if count_value > 0:
            return True

        return False

    def sleep_five_second(self):
        time.sleep(5)

    def sleep_one_second(self):
        time.sleep(1)

    def sleep_second(self, second):
        time.sleep(second)

    def get_latest_work_day(self):
        return "2018-11-09"

    def get_before_two_month(self):
        before_two_month = datetime.datetime.today() + datetime.timedelta(days=-60)
        return before_two_month.strftime("%Y-%m-%d")

    def compare_two_date_str(self, first_date, two_date):
        if first_date is None:
            return False
        if two_date is None:
            return False
        if datetime.datetime.strptime(first_date, "%Y-%m-%d") >= datetime.datetime.strptime(two_date, "%Y-%m-%d"):
            return True
        return False

    def log_info(self, message):
        print("message-->" + message)

    def is_none(self, data):
        if data is None:
            return True
        return False

    # 计算百分比，并进行四舍五入保留2为小数
    def cal_percent_round_2(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100

        return round((first_value/second_value)*100, 2)

    # 计算百分比，并进行四舍五入保留2为小数
    def cal_percent_round_2_not_zero(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100

        return round(((first_value - second_value)/second_value)*100, 2)

    # 两个数相除并保留两个小数点
    def cal_division_round_2(self, first_value, second_value):
        if first_value == 0:
            return 0
        if second_value == 0:
            return 100
        return round((first_value / second_value), 2)

    def get_next_date_str(self, date):
        if date is None:
            return date
        next_date = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)
        return next_date.strftime("%Y-%m-%d")

    def get_pre_date_str(self, date):
        if date is None:
            return date
        next_date = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=-1)
        return next_date.strftime("%Y-%m-%d")

    def get_date_str_list(self, start_date_str, end_date_str):
        date_list = []
        start_date = datetime.datetime.strptime(start_date_str, self.yyyy_mm_dd_date_format)
        end_date = datetime.datetime.strptime(end_date_str, self.yyyy_mm_dd_date_format)
        while start_date <= end_date:
            date_list.append(start_date.strftime(self.yyyy_mm_dd_date_format))
            start_date = start_date + datetime.timedelta(1)
        return date_list

    def get_date_str(self, date):
        if date is None:
            return date
        if not isinstance(date, datetime.date):
            return date
        return date.strftime("%Y-%m-%d")


test = TushareBase()
# value = test.cal_percent_round_2(766, 877)
# test.get_one_stock_basic("603997")
# value = test.get_date_str_list("2018-09-28", "2018-10-13")
# value = test.get_before_two_month()
# value = test.get_next_date_str("2018-09-30")
# print(value)
# value = test.compare_two_date_str("2018-09-27", "2018-09-28")
# print(value)
# test.get_inside_dish_volume("002134")
# test.get_inside_dish_amt("002134")
# test.get_min_volume("002134")
# test.get_max_amt("002134")
# test.get_mid_amt("002134")
# test.get_stock_limit_up_value("603997")
# test.get_stock_limit_down_value("603997")
# test.get_stock_first_limit_up_time("002931")
# test.get_stock_first_limit_down_time("002931")
# test.get_sunso_stock_newly_quotes_data()
# test.get_avg_trade_volume_from_tushare_quotes("600532", 5)
# test.get_avg_trade_amt_from_sunso_quotes("600532", 5)
# test.get_stock_basics_to_db()
# test.get_stock_basics_to_hist_db()
# test.setproperty("users")
# test.getproperty()

# data = json.loads('{"timeToMarket":"20180909"}')
# time_to_market = test.get_time_to_market_ymd(None)
# print("timeToMarket-->" + time_to_market)
# test.data_to_db_append(None, 'user')

# test.count_sql("select count(*) as c from t_tushare_stock_basic")