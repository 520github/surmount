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


class TushareStockHistDateDataHandler(object):
    tushare_stock_hist_quotes_data = None
    tushare_stock_today_tick_trade_data = None
    date = "2018-10-19" # "2017-04-21"
    end_date = None

    def __init__(self):
        self.tushare_stock_hist_quotes_data = TushareStockHistQuotesData()
        self.tushare_stock_today_tick_trade_data = TushareStockTodayTickTradeData()
        print("TushareStockHistDateDataHandler init ")

    def handle_tushare_date_stock_hist_tick_trade_data(self, date):
        # 从t_sunso_stock_basic表中获取某一日期，需要执行的股票列表
        data_list = self.tushare_stock_hist_quotes_data.get_date_stock_list_not_in_sunso_stock_day_trade_statistic_data(date)
        if data_list is None or len(data_list) < 1:
            print("date " + date + " not found hist_tick_trade handle to day_trade_statistic_data")
            time.sleep(1)
            return

        for data in data_list:
            stock_code = data["code"]
            date = data["trade_date"].strftime("%Y-%m-%d")
            if not self.tushare_stock_hist_quotes_data.is_exist_stock_hist_quotes_data_by_date(stock_code, date):
                self.tushare_stock_hist_quotes_data.get_one_stock_hist_quotes_data_to_db(stock_code, date, date)

            hist_quotes_data = self.tushare_stock_hist_quotes_data.get_one_stock_hist_quotes_data_by_date(stock_code, date)

            if not self.tushare_stock_today_tick_trade_data.is_exist_today_tick_trade_data(stock_code, date):
                self.tushare_stock_today_tick_trade_data.get_one_stock_date_tick_trade_data_to_db(stock_code, date)
            self.tushare_stock_today_tick_trade_data.insert_to_sunso_stock_day_trade_statistic_data(hist_quotes_data)
            self.tushare_stock_today_tick_trade_data.delete_today_tick_trade_data(stock_code, date)

    def run_tushare_date_stock_hist_data_handle(self):
        while True:
            try:
                start_time = time.time()
                print("       ")
                print("start run_tushare_date_stock_hist_data_handle run  " + self.get_now_date_time_all_str())
                print("       ")
                self.handle_tushare_date_stock_hist_tick_trade_data(self.date)
                consume_time = str(time.time() - start_time)
                print("      ")
                print(
                            "end run_tushare_date_stock_hist_data_handle run " + self.get_now_date_time_all_str() + ", counsume time:" + consume_time)
                print("      ")
                break
            except Exception, e:
                print("exception run_tushare_date_stock_hist_data_handle run  " + self.get_now_date_time_all_str())
                print e
                print(traceback.format_exc())
                time.sleep(10)

    def get_now_date_time_all_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    hist_data_handler = TushareStockHistDateDataHandler()
    hist_data_handler.run_tushare_date_stock_hist_data_handle()