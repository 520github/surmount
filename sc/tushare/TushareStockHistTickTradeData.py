#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取当日已成交的分笔交易数据

from TushareBase import TushareBase
import tushare as ts


class TushareStockHistTickTradeData(TushareBase, object):
    def __init__(self):
        super(TushareStockHistTickTradeData, self).__init__()
        self.table_name = "t_tushare_stock_hist_tick_trade_data"
        print("stock today tick trade data")

    def get_one_stock_hist_tick_trade_data(self, stock_code=None, date=None):
        if date is None:
            date = self.get_latest_work_day()

        data = ts.get_tick_data(stock_code, date, src="nt") #
        if data is None:
            return data

        data["date"] = date
        data["code"] = stock_code
        data.insert(2, "pchange", 0)
        return data

    def get_one_stock_hist_tick_trade_data_to_db(self, stock_code=None, date=None):
        self.data_to_db_append(self.get_one_stock_hist_tick_trade_data(stock_code, date), self.table_name)

    def get_all_stock_hist_tick_trade_data_to_db(self):
        df = self.get_stock_basics()
        for stock_code, row in df.iterrows():
            max_trade_date = self.get_stock_max_trade_date(stock_code)
            lastet_work_date = self.get_latest_work_day()
            date_list = self.get_date_str_list(max_trade_date, lastet_work_date)
            for date in date_list:
                self.get_one_stock_hist_tick_trade_data_to_db(stock_code, date)
                self.sleep_second(0.5)

    def get_stock_max_trade_date(self, stock_code):
        sql = "select max(date) as c from " + self.table_name + " where code='" + stock_code + "'"
        max_trade_date = self.count_sql(sql)
        if max_trade_date is None:
            max_trade_date = self.get_before_two_month()
        return max_trade_date


# print(ts.trade_cal())


hist_tick = TushareStockHistTickTradeData()
# hist_tick.get_all_stock_hist_tick_trade_data_to_db()
hist_tick.get_one_stock_hist_tick_trade_data_to_db("600518", "2018-10-16")