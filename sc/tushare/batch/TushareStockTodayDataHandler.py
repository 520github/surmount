#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import datetime
import traceback
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from TushareStockNewlyQuotesData import TushareStockNewlyQuotesData
from TushareStockTodayTickTradeData import TushareStockTodayTickTradeData

class TushareStockTodayDataHandler(object):

    tushare_stock_newly_quotes_data = None
    tushare_stock_today_tick_trade_data = None
    latest_work_day = None
    title = "run_tushare_stock_today_data_handle"

    def __init__(self):
        self.tushare_stock_newly_quotes_data = TushareStockNewlyQuotesData()
        self.tushare_stock_today_tick_trade_data = TushareStockTodayTickTradeData()
        self.latest_work_day = self.tushare_stock_newly_quotes_data.get_latest_work_day()
        print(" TushareStockTodayDataHandler init " + self.latest_work_day)

    def handle_tushare_stock_today_quotes_data(self):
        self.tushare_stock_newly_quotes_data.delete_stock_newly_quotes_data_before_today()
        if self.tushare_stock_newly_quotes_data.is_exist_today_newly_quotes_data():
            print("date " + self.latest_work_day + " tushare_stock_today_quotes_data is exist ")
            return
        self.tushare_stock_newly_quotes_data.get_all_stock_newly_quotes_data_to_db()

    def handle_tushare_stock_today_tick_trade_data(self):
        data_list = self.get_handle_stock_data_list()
        if data_list is None or len(data_list) < 1:
            print("date " + self.latest_work_day + " not found newly_quotes_data handle to day_trade_statistic_data")
            time.sleep(60)
            return

        for data in data_list:
            stock_code = data["code"]
            date = data["date"].strftime("%Y-%m-%d")
            if not self.tushare_stock_today_tick_trade_data.is_exist_today_tick_trade_data(stock_code, date):
                # self.tushare_stock_today_tick_trade_data.get_one_stock_today_tick_trade_data_replace_to_db(stock_code)
                self.tushare_stock_today_tick_trade_data.get_one_stock_date_tick_trade_data_to_db(stock_code, date)
            # self.tushare_stock_today_tick_trade_data.insert_to_sunso_stock_day_trade_statistic_data(data)
            self.tushare_stock_today_tick_trade_data.insert_into_about_sunso_stock_day_trade_statistic_data(data)
            self.tushare_stock_today_tick_trade_data.delete_today_tick_trade_data(stock_code, date)

    def get_handle_stock_data_list(self):
        return self.tushare_stock_today_tick_trade_data.get_stocks_not_in_sunso_stock_day_trade_statistic_data()

    def run_tushare_stock_today_data_handle(self):
        while True:
            try:
                start_time = time.time()
                print("       ")
                print("start " + self.title + " run  " + self.get_now_date_time_all_str())
                print("       ")
                self.handle_tushare_stock_today_quotes_data()
                self.handle_tushare_stock_today_tick_trade_data()
                consume_time = str(time.time() - start_time)
                print("      ")
                print("end " + self.title + " run " + self.get_now_date_time_all_str() + ", counsume time:" + consume_time)
                print("      ")
            except Exception, e:
                print("exception " + self.title + " run  " + self.get_now_date_time_all_str())
                print e
                print(traceback.format_exc())
                time.sleep(30)

    def get_now_date_time_all_str(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    today_data_handler = TushareStockTodayDataHandler()
    today_data_handler.run_tushare_stock_today_data_handle()
