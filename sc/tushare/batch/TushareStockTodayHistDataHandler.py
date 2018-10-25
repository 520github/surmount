#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from TushareStockTodayDataHandler import TushareStockTodayDataHandler


class TushareStockTodayHistDataHandler(TushareStockTodayDataHandler, object):
    date = "2018-10-24"

    def __init__(self):
        super(TushareStockTodayHistDataHandler,self).__init__()
        self.title = "run_tushare_stock_today_hist_data_handle"
        if TushareStockTodayHistDataHandler.date is None:
            TushareStockTodayHistDataHandler.date = self.tushare_stock_newly_quotes_data.get_latest_work_day()
        print(" TushareStockTodayHistDataHandler init " + self.latest_work_day)

    def handle_tushare_stock_today_quotes_data(self):
        print("not thing doing")

    def get_handle_stock_data_list(self):
        return self.tushare_stock_today_tick_trade_data.get_newly_quotes_hist_stocks_not_in_sunso_stock_day_trade_statistic_data(
            TushareStockTodayHistDataHandler.date)


if __name__ == '__main__':
    today_hist_data_handler = TushareStockTodayHistDataHandler()
    today_hist_data_handler.run_tushare_stock_today_data_handle()
