#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取股票的历史行情数据

import tushare as ts
from TushareBase import TushareBase


class TushareStockHistQuotesData(TushareBase, object):

    def __init__(self):
        super(TushareStockHistQuotesData, self).__init__()
        self.table_name = "t_tushare_stock_hist_quotes_data"
        print("hist quotes data")

    def get_one_stock_hist_quotes_data(self, stock_code, start_date=None, end_date=None):
        data = ts.get_hist_data(stock_code, start=start_date, end=end_date, pause=self.pause)
        if data is None:
            if start_date is None:
                start_date = ""
            if end_date is None:
                end_date = ""
            print("get stock " + stock_code + " data is empty by date between " + start_date + " and " + end_date)
            return data

        data["code"] = stock_code
        return data

    # 获取小于已存在最小交易日的交易行情数据
    def get_one_stock_hist_quotes_data_to_db_before_exist_min_trade_date(self, stock_code, start_date=None):
        end_date = self.get_stock_quotes_data_min_date(stock_code)
        if self.compare_two_date_str(start_date, end_date):
            return
        self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), self.table_name)

    # 获取单个股份的所有历史行情数据
    def get_one_stock_hist_quotes_data_to_db(self, stock_code, start_date=None, end_date=None):
        self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), self.table_name)

    # 获取所有股票的历史行情数据, 开始时间为该股票已存在行情的最大日期+1
    def get_all_stock_quotes_data_to_db(self):
        stocks = self.get_stock_basics()
        for stock_code, row in stocks.iterrows():
            start_date = self.get_stock_quotes_data_max_date(stock_code)
            if self.compare_two_date_str(start_date, self.get_latest_work_day()):
                continue
            end_date = None
            self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), self.table_name)
            self.sleep_one_second()

    # 获取所有股票指定开始和结束时间的历史行情数据,
    def get_all_stock_date_quotes_data_to_db(self, start_date, end_date):
        stocks = self.get_stock_basics()
        for stock_code, row in stocks.iterrows():
            self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), "t_tushare_stock_hist_quotes_data")

    # 获取某个股票已存在行情数据的最大日期
    def get_stock_quotes_data_max_date(self, stock_code):
        sql = "select max(date) as c from " + self.table_name + " where code='" + stock_code + "'"
        max_date = self.count_sql(sql)
        return self.get_next_date_str(max_date)

    # 获取某个股票已存在行情数据的最小日期
    def get_stock_quotes_data_min_date(self, stock_code):
        sql = "select min(date) as c from " + self.table_name + " where code='" + stock_code + "'"
        min_date = self.count_sql(sql)
        return self.get_pre_date_str(min_date)

    # 获取缺少的股票行情数据
    def get_loss_stock_date_quotes_data_to_db(self, start_date, end_date):
        sql = "select code from t_tushare_stock_basic where code not in (select code from t_tushare_stock_hist_quotes_data) "
        data_list = self.select_sql(sql)
        print("data list size:" + str(len(data_list)))
        for data in data_list:
            stock_code = data["code"].encode('utf-8')
            self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), "t_tushare_stock_hist_quotes_data")

    # 根据指定日期涨停板的股票，根据指定时间段，获取其股票行情数据
    def get_limit_up_stock_date_quotes_data_to_db(self, limit_up_stocke_date, start_date, end_date):
        data_list = self.get_limit_up_stock(limit_up_stocke_date)
        for data in data_list:
            stock_code = data["code"]
            self.data_to_db_append(self.get_one_stock_hist_quotes_data(stock_code, start_date, end_date), self.table_name)

    # 查询小于某个交易日期的指定数量的股票行情数据
    def get_stock_hist_quotes_data_list_by_less_trade_date_limit(self, stock_code, trade_date, limit):
        sql = "select * from " + self.table_name + " " \
              "where code='" + stock_code + "' and date < '" + trade_date + "' limit " + str(limit)
        data_list = self.select_sql(sql)
        self.convert_dict_list_unicode_to_str(data_list)
        return data_list

    def save_data_list_to_sunso_stock_all_quotes_data(self, data_list):
        for data in data_list:
            self.save_one_data_to_sunso_stock_all_quotes_data(data)

    def save_one_data_to_sunso_stock_all_quotes_data(self, data):
        stock_code = data["code"]
        date = data["date"]
        inside_dish_volume = self.get_inside_dish_volume_date(stock_code, date)
        outside_dish_volume = self.get_outside_dish_volume_date(stock_code, date)
        oi_dish_diff_volume = str(outside_dish_volume - inside_dish_volume)
        oi_dish_volume_percent = str(self.cal_percent_round_2(outside_dish_volume, inside_dish_volume))
        inside_dish_amt = self.get_inside_dish_amt_date(stock_code, date)
        outside_dish_amt = self.get_outside_dish_amt_date(stock_code, date)
        oi_dish_diff_amt = str(outside_dish_amt - inside_dish_amt)
        oi_dish_amt_percent = str(self.cal_percent_round_2(outside_dish_amt, inside_dish_amt))
        min_trade_volume = str(self.get_min_volume_date(stock_code, date))
        mid_trade_volume = str(self.get_mid_volume_date(stock_code, date))
        max_trade_volume = str(self.get_max_volume_date(stock_code, date))
        min_trade_amt = str(self.get_min_amt_date(stock_code, date))
        mid_trade_amt = str(self.get_mid_amt_date(stock_code, date))
        max_trade_amt = str(self.get_max_amt_date(stock_code, date))
        stock_basic = self.get_one_stock_basic(stock_code)
        sql = "insert into " + self.t_sunso_stock_all_quotes_data + "(" + self.get_sunso_stock_quotes_data_column() + ""\
              ") values('" + stock_code + "'," \
            "'" + stock_basic["name"] + "'," \
            "" + str(data["open"]) + "," \
            "" + str(data["close"]) + "," \
            "" + str(data["low"]) + "," \
            "" + str(data["high"]) + "," \
            "-1,-1,-1," \
            "" + str(data["p_change"]) + "," \
            "" + str(data["price_change"]) + "," \
            "-1," \
            "" + str(data["volume"]) + "," \
            "-1," \
            "" + str(data["v_ma5"]) + "," \
            "" + str(data["v_ma10"]) + "," \
            "" + str(data["v_ma20"]) +  "," \
            "" + str(data["ma5"]) + "," \
            "" + str(data["ma10"]) + "," \
            "" + str(data["ma20"]) + "," \
            "" + str(inside_dish_volume) + "," \
            "" + str(outside_dish_volume) + "," \
            "" + oi_dish_diff_volume + "," \
            "" + oi_dish_volume_percent + "," \
            "" + str(inside_dish_amt) + "," \
            "" + str(outside_dish_amt) + "," \
            "" + oi_dish_diff_amt + "," \
            "" + oi_dish_amt_percent + "," \
            "" + min_trade_volume + "," \
            "" + mid_trade_volume + "," \
            "" + max_trade_volume + "," \
            "" + min_trade_amt + "," \
            "" + mid_trade_amt + "," \
            "" + max_trade_amt + "," \
            "'','',-1,-1,-1,-1," \
            "'" + date + "')"
        print(sql)
        self.insert_sql(sql)

    def delete_tushare_one_stock_hist_quotes_data(self, stock_code):
        sql = "delete from " + self.table_name + " where code='" + stock_code + "'"
        self.delete_sql(sql)

    def get_one_stock_list_not_in_sunso_stock_day_trade_statistic_data(self, stock_code):
        sql = "select " + self.get_stock_hist_quotes_data_serach_column() + "" \
              " from " + self.table_name + " " \
              "where concat(code,date) not in (select concat(code,trade_date) from " \
               "" + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where code='" + stock_code + "')  " \
              " and code='" + stock_code + "' order by date asc "
        return self.select_sql(sql)

    def get_date_stock_list_not_in_sunso_stock_day_trade_statistic_data(self, date):
        sql = "select * " \
              " from " + self.t_sunso_stock_basic + " " \
              "where concat(code,trade_date) not in (select concat(code,trade_date) from " \
              "" + self.t_sunso_stock_day_trade_statistic_data + " " \
              "where trade_date='" + date + "')  " \
              " and trade_date='" + date + "' " \
              " and code='600518' " \
              "order by trade_date asc "
        return self.select_sql(sql)

    def get_one_stock_hist_quotes_data_by_date(self, stock_code, date):
        sql = "select " + self.get_stock_hist_quotes_data_serach_column() + "" \
              " from " + self.table_name + " " \
              " where code='" + stock_code + "' and date='" + date + "'"
        return self.select_one_sql(sql)

    def is_exist_stock_hist_quotes_data_by_date(self, stock_code, date):
        sql = "select count(*) as c from " + self.table_name + " where code='" + stock_code + "' and date='" + date + "'"
        count_value = self.count_sql_default_zero(sql)
        if count_value > 0:
            return True
        return False

    def get_stock_hist_quotes_data_serach_column(self):
        return "code,date,open,high,close as trade,low,volume,p_change as changepercent,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20"


newly = TushareStockHistQuotesData()
# newly.get_one_stock_hist_quotes_data("603895")
# data_list = newly.get_stock_hist_quotes_data_list_by_less_trade_date_limit("603895", "2018-10-12", 30)
# newly.save_data_list_to_sunso_stock_all_quotes_data(data_list)
# newly.get_one_stock_hist_quotes_data_to_db_before_exist_min_trade_date("603895", "2018-08-14")
# newly.get_all_stock_quotes_data_to_db()
# newly.get_one_stock_hist_quotes_data_to_db("600518")
# newly.get_all_stock_date_quotes_data_to_db("2018-09-28","2018-10-07")
# newly.get_loss_stock_date_quotes_data_to_db("2018-09-28", "2018-10-07")
# 】newly.get_limit_up_stock_date_quotes_data_to_db("2018-09-28", "2018-09-20", "2018-09-27")
