#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../alarm'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../plate'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../foundation'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../statistic'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../batch'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../export'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../industry'))

from TushareStockDataHandler import TushareStockDataHandler
from TushareStockTodayHistDataHandler import TushareStockTodayHistDataHandler
from TushareStockLoadFoundationIndex import TushareStockLoadFoundationIndex
from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
from StatisticRangeAvgData import StatisticRangeAvgData
from AlarmLowPriceRise import AlarmLowPriceRise
from AlarmTurnoverRateChangeBigMore import AlarmTurnoverRateChangeBigMore
from AlarmTodayFirstUpAfterDownAndYesterdayUpLimit import AlarmTodayFirstUpAfterDownAndYesterdayUpLimit
from StockPlateHandler import StockPlateHandler
from ExportAlarmSameDayBeforeLowAfterHigh import ExportAlarmSameDayBeforeLowAfterHigh
from ExportPlateStockList import ExportPlateStockList
from TushareStockDragonTigerDayTotalData import TushareStockDragonTigerDayTotalData
from DayIndustryStatisticCoreData import DayIndustryStatisticCoreData


class TusharePortal(object):
    trade_date = "2018-11-29"

    def __init__(self):
        print("TusharePortal init")

    # 获取当天相关的数据源
    def step1_get_today_data(self):
        # 需要修改当前日期
        handler = TushareStockDataHandler()
        # handler.clear_today_basic_data()
        handler.init_today_basic_data()

    # 处理当天数据
    def step2_load_today_data(self):
        today_hist_data_handler = TushareStockTodayHistDataHandler()
        print("date1-->" + today_hist_data_handler.date)
        today_hist_data_handler.date = self.trade_date
        print("date2-->" + today_hist_data_handler.date)
        today_hist_data_handler.run_tushare_stock_today_data_handle()

    # 统计相关幅度的平均数据
    def step3_statistic_range_avg_data(self):
        range = StatisticRangeAvgData()
        range.load_statistic_data()

    # 处理当日龙虎榜数据
    def step33_dragon_tiger_day_total_data(self):
        dragon_tiger = TushareStockDragonTigerDayTotalData()
        dragon_tiger.load_dragon_tiger_day_total_data()

    # 处理行业相关数据
    def step333_day_industry_statistic_data(self):
        dis = DayIndustryStatisticCoreData()
        dis.handle_list_day_industry()

    # 执行相关预警操作
    def step4_alarm_data(self):
        alpr = AlarmLowPriceRise()
        alpr.trade_date = self.trade_date
        alpr.alarm_stock_list()

        atrc= AlarmTurnoverRateChangeBigMore()
        atrc.trade_date = self.trade_date
        atrc.alarm_stock_list()

        ty = AlarmTodayFirstUpAfterDownAndYesterdayUpLimit()
        ty.trade_date = self.trade_date
        ty.alarm_stock_list()

    # 处理板块相关数据
    def step5_plate_data(self):
        plate_handler = StockPlateHandler()
        plate_handler.trade_date = self.trade_date
        plate_handler.run_stock_plate()

    # 执行股票基础指标相关数据，一般每个季度跑一次就可以,不需要每次都执行
    def step6_load_foundation_index_data(self):

        index = TushareStockLoadFoundationIndex()
        index.year = "(2018)"
        index.quarter = "(4)"

        BaseFoundationYearAndQuarter.begin_year = 2018
        BaseFoundationYearAndQuarter.end_year = 2018
        BaseFoundationYearAndQuarter.quarters = [4]

        index.load_foundation_index()

    def step7_export_data(self):
        blah = ExportAlarmSameDayBeforeLowAfterHigh()
        blah.trade_date = self.trade_date
        blah.export_sql_data_to_excel()

        high = ExportPlateStockList()
        high.export_sql_data_list_to_excel("plate_name")


if __name__ == "__main__":
    portal = TusharePortal()
    # portal.step1_get_today_data()
    # portal.step2_load_today_data()
    # portal.step3_statistic_range_avg_data()
    # portal.step33_dragon_tiger_day_total_data()
    # portal.step333_day_industry_statistic_data()
    # portal.step4_alarm_data()
    # portal.step5_plate_data()
    # portal.step6_load_foundation_index_data()
    portal.step7_export_data()
