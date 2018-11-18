#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import time
import datetime
import traceback
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from TushareStockBasic import TushareStockBasic
from TushareStockNewlyQuotesData import TushareStockNewlyQuotesData
from TushareStockHistQuotesData import TushareStockHistQuotesData
from TushareStockTodayTickTradeData import TushareStockTodayTickTradeData
from TushareStockDragonTigerTotalData import TushareStockDragonTigerTotalData
from TushareStockDragonTigerTodayData import TushareStockDragonTigerTodayData
from TushareStockDragonTigerOrganTotalData import TushareStockDragonTigerOrganTotalData
from TushareStockDragonTigerOrganTodayData import TushareStockDragonTigerOrganTodayData
from TushareStockDragonTigerSaleTotalData import TushareStockDragonTigerSaleTotalData



class TushareStockDataHandler(object):
    tushare_stock_basic = None
    tushare_stock_newly_quotes_data = None
    tushare_stock_hist_quotes_data = None
    tushare_stock_today_tick_trade_data = None

    tushare_stock_dragon_tiger_total_data = None
    tushare_stock_dragon_tiger_today_data = None
    tushare_stock_dragon_tiger_organ_total_data = None
    tushare_stock_dragon_tiger_organ_today_data = None
    tushare_stock_dragon_tiger_sale_total_data = None

    days5_data = 5
    latest_work_day = None

    def __init__(self):
        TushareStockDataHandler.tushare_stock_basic = TushareStockBasic()
        TushareStockDataHandler.tushare_stock_newly_quotes_data = TushareStockNewlyQuotesData()
        TushareStockDataHandler.tushare_stock_hist_quotes_data = TushareStockHistQuotesData()
        TushareStockDataHandler.tushare_stock_today_tick_trade_data = TushareStockTodayTickTradeData()

        TushareStockDataHandler.tushare_stock_dragon_tiger_total_data = TushareStockDragonTigerTotalData()
        TushareStockDataHandler.tushare_stock_dragon_tiger_today_data = TushareStockDragonTigerTodayData()
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_total_data = TushareStockDragonTigerOrganTotalData()
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_today_data = TushareStockDragonTigerOrganTodayData()
        TushareStockDataHandler.tushare_stock_dragon_tiger_sale_total_data = TushareStockDragonTigerSaleTotalData()

        TushareStockDataHandler.latest_work_day = TushareStockDataHandler.tushare_stock_basic.get_latest_work_day()

        print("TushareStockDataHandler init")

    def init_today_basic_data(self):
        self.init_today_quotes_data()
        self.init_today_stock_basic()
        self.init_dragon_tiger_data()
        print("init_today_basic_data is ok...........................")

    def init_today_quotes_data(self):
        TushareStockDataHandler.tushare_stock_newly_quotes_data.delete_stock_newly_quotes_data_before_today()
        if TushareStockDataHandler.tushare_stock_newly_quotes_data.is_exist_today_newly_quotes_data():
            print("date " + self.latest_work_day + " tushare_stock_today_quotes_data is exist ")
            return
        # 同时先删除当前表和历史表数据，再写入当前表和历史表
        TushareStockDataHandler.tushare_stock_newly_quotes_data.get_all_stock_newly_quotes_data_to_db()

    def init_today_stock_basic(self):
        TushareStockDataHandler.tushare_stock_basic.insert_sunso_stock_basic_from_tushare_stock_basic()

    def init_dragon_tiger_data(self):
        TushareStockDataHandler.tushare_stock_dragon_tiger_total_data.get_tushare_stock_dragon_tiger_total_data_to_db(
            self.days5_data)
        TushareStockDataHandler.tushare_stock_dragon_tiger_today_data.get_stock_dragon_tiger_today_data_to_db(
            self.latest_work_day)
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_total_data.get_tushare_stock_dragon_tiger_organ_total_data_to_db(
            self.days5_data)
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_today_data.get_dragon_tiger_organ_today_data_to_db()
        TushareStockDataHandler.tushare_stock_dragon_tiger_sale_total_data.get_stock_dragon_tiger_sale_total_data_to_db(
            self.days5_data)

    def clear_today_basic_data(self):
        TushareStockDataHandler.tushare_stock_newly_quotes_data.delete_stock_newly_quotes_data()
        TushareStockDataHandler.tushare_stock_basic.delete_sunso_stock_basic()
        TushareStockDataHandler.tushare_stock_dragon_tiger_total_data.delete_stock_dragon_tiger_total_data_by_days_and_date(
            self.days5_data)
        TushareStockDataHandler.tushare_stock_dragon_tiger_today_data.delete_dragon_tiger_today_data_by_date(
            self.latest_work_day)
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_total_data.delete_stock_dragon_tiger_organ_total_data_by_date_and_days(
            self.days5_data)
        TushareStockDataHandler.tushare_stock_dragon_tiger_organ_today_data.delete_dragon_tiger_organ_today_data_by_date(
            self.latest_work_day)
        TushareStockDataHandler.tushare_stock_dragon_tiger_sale_total_data.delete_stock_dragon_tiger_sale_total_data_by_date_and_days(
            self.days5_data)


if __name__ == "__main__":
    handler = TushareStockDataHandler()
    # handler.clear_today_basic_data()
    handler.init_today_basic_data()