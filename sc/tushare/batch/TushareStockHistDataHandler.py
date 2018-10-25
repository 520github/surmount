#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import datetime
import traceback
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from TushareStockHistQuotesData import TushareStockHistQuotesData
from TushareStockTodayTickTradeData import TushareStockTodayTickTradeData

class TushareStockHistDataHandler(object):
    tushare_stock_hist_quotes_data = None
    tushare_stock_today_tick_trade_data = None
    stock_code = "600518"
    start_date = "2017-04-21" # "2018-08-03"
    end_date = None

    def __init__(self):
        self.tushare_stock_hist_quotes_data = TushareStockHistQuotesData()
        self.tushare_stock_today_tick_trade_data = TushareStockTodayTickTradeData()
        print("TushareStockHistDataHandler init ")

    def handle_tushare_one_stock_hist_quotes_data(self, stock_code, start_date=None, end_date=None):
        self.tushare_stock_hist_quotes_data.delete_tushare_one_stock_hist_quotes_data(stock_code)
        self.tushare_stock_hist_quotes_data.get_one_stock_hist_quotes_data_to_db(stock_code, start_date, end_date)

    def handle_tushare_one_stock_hist_tick_trade_data(self, stock_code):
        data_list = self.tushare_stock_hist_quotes_data.get_one_stock_list_not_in_sunso_stock_day_trade_statistic_data(stock_code)
        if data_list is None or len(data_list) < 1:
            print("stock_code " + stock_code + " not found hist_tick_trade handle to day_trade_statistic_data")
            time.sleep(1)
            return

        for data in data_list:
            stock_code = data["code"]
            date = data["date"]
            if not self.tushare_stock_today_tick_trade_data.is_exist_today_tick_trade_data(stock_code, date):
                self.tushare_stock_today_tick_trade_data.get_one_stock_date_tick_trade_data_to_db(stock_code, date)
            self.tushare_stock_today_tick_trade_data.insert_to_sunso_stock_day_trade_statistic_data(data)
            self.tushare_stock_today_tick_trade_data.delete_today_tick_trade_data(stock_code, date)

    def run_tushare_one_stock_hist_data_handle(self):
        while True:
            try:
                start_time = time.time()
                print("       ")
                print("start run_tushare_one_stock_hist_data_handle run  " + self.get_now_date_time_all_str())
                print("       ")
                self.handle_tushare_one_stock_hist_quotes_data(self.stock_code, self.start_date, self.end_date)
                self.handle_tushare_one_stock_hist_tick_trade_data(self.stock_code)
                consume_time = str(time.time() - start_time)
                print("      ")
                print(
                            "end run_tushare_one_stock_hist_data_handle run " + self.get_now_date_time_all_str() + ", counsume time:" + consume_time)
                print("      ")
                break
            except Exception, e:
                print("exception run_tushare_one_stock_hist_data_handle run  " + self.get_now_date_time_all_str())
                print e
                print(traceback.format_exc())
                time.sleep(10)

    def get_now_date_time_all_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    hist_data_handler = TushareStockHistDataHandler()
    hist_data_handler.run_tushare_one_stock_hist_data_handle()