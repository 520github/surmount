#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from TushareStockHistQuotesData import TushareStockHistQuotesData
from TushareStockTodayTickTradeData import TushareStockTodayTickTradeData
from TushareStockNewlyQuotesData import TushareStockNewlyQuotesData


class TushareStockHistQuotesToNewlyQuotesHandler(object):
    tushare_stock_hist_quotes_data = None
    tushare_stock_today_tick_trade_data = None
    tushare_stock_newly_quotes_data = None

    def __init__(self):
        self.tushare_stock_hist_quotes_data = TushareStockHistQuotesData()
        self.tushare_stock_today_tick_trade_data = TushareStockTodayTickTradeData()
        self.tushare_stock_newly_quotes_data = TushareStockNewlyQuotesData()
        print("TushareStockHistQuotesToNewlyQuotesHandler init")

    def handle_hist_quotes_to_newly_quotes(self, date):
        # 从t_sunso_stock_basic表中获取某一日期，需要执行的股票列表
        data_list = self.tushare_stock_hist_quotes_data.get_date_stock_list_not_in_sunso_stock_day_trade_statistic_data(
            date)
        if data_list is None or len(data_list) < 1:
            print("date " + date + " not found hist_quotes_data handle to TushareStockHistQuotesToNewlyQuotes")
            time.sleep(1)
            return

        for data in data_list:
            stock_code = data["code"]
            date = data["trade_date"].strftime("%Y-%m-%d")
            print("code:" + stock_code + ", trade_date:" + date)
            if not self.tushare_stock_hist_quotes_data.is_exist_stock_hist_quotes_data_by_date(stock_code, date):
                self.tushare_stock_hist_quotes_data.get_one_stock_hist_quotes_data_to_db(stock_code, date, date)

            hist_quotes_data = self.tushare_stock_hist_quotes_data.get_one_stock_hist_quotes_data_by_date(
                stock_code, date)
            if hist_quotes_data is None:
                continue
            if not self.tushare_stock_today_tick_trade_data.is_exist_today_tick_trade_data(stock_code, date):
                self.tushare_stock_today_tick_trade_data.get_one_stock_date_tick_trade_data_to_db(stock_code, date)
            self.tushare_stock_newly_quotes_data.insert_into_newly_quotes_data_from_hist_quotes_data(hist_quotes_data)

        print("handle newly_quotes_data_hist by trade_date:" + date)
        self.tushare_stock_newly_quotes_data.delete_stock_newly_quotes_data_hist(date)
        self.tushare_stock_newly_quotes_data.insert_to_stock_newly_quotes_data_hist()
