#!/usr/bin/python
# -*- coding: UTF-8 -*-

from TushareStockDragonTigerTotalData import TushareStockDragonTigerTotalData
from TushareStockDragonTigerTodayData import TushareStockDragonTigerTodayData
from TushareStockDragonTigerSaleTotalData import TushareStockDragonTigerSaleTotalData
from TushareStockDragonTigerOrganTotalData import TushareStockDragonTigerOrganTotalData
from TushareStockDragonTigerOrganTodayData import TushareStockDragonTigerOrganTodayData


class TushareStockDragonTigerTest(object):
    trade_date = "2018-12-05"
    day = 5

    def test(self):
        stock_top = TushareStockDragonTigerTotalData()
        ds = stock_top.get_tushare_stock_dragon_tiger_total_data(self.day)
        print("dragon_tiger_total--1>" + str(len(ds)))

        top = TushareStockDragonTigerTodayData()
        ds = top.get_stock_dragon_tiger_today_data(self.trade_date)
        print("tiger_today_data--2>" + str(len(ds)))

        organ_top = TushareStockDragonTigerSaleTotalData()
        ds = organ_top.get_stock_dragon_tiger_sale_total_data(self.day)
        print("tiger_sale_total--3>" + str(len(ds)))

        organ_seat = TushareStockDragonTigerOrganTotalData()
        ds = organ_seat.get_tushare_stock_dragon_tiger_organ_total_data(self.day)
        print("dragon_tiger_organ_total_data--4>" + str(len(ds)))

        organ = TushareStockDragonTigerOrganTodayData()
        ds = organ.get_dragon_tiger_organ_today_data()
        print("dragon_tiger_organ_today--5>" + str(len(ds)))


if __name__ == "__main__":
    test = TushareStockDragonTigerTest()
    test.test()