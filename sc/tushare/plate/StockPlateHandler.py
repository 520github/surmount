#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockPlateDayData import StockPlateDayData
from StockPlateStockDayData import StockPlateStockDayData


class StockPlateHandler(object):

    stock_plate_day_data = None
    stock_plate_stock_day_data = None
    trade_date = "2018-11-01"

    def __init__(self):
        StockPlateHandler.stock_plate_day_data = StockPlateDayData()
        StockPlateHandler.stock_plate_stock_day_data = StockPlateStockDayData()

    def handle_one_stock_plate(self, plate_data):
        self.stock_plate_stock_day_data.init_stock_plate_stock_data(plate_data)
        self.stock_plate_stock_day_data.init_stock_plate_stock_day_data(plate_data)
        self.stock_plate_stock_day_data.update_stock_plate_stock(plate_data)

        self.stock_plate_day_data.init_stock_plate_day_data(plate_data)
        self.stock_plate_day_data.update_stock_plate(plate_data)

    def run_stock_plate(self):
        data_list = self.stock_plate_day_data.get_stock_plate_data_list()
        if data_list is None:
            return
        for plate_data in data_list:
            plate_data["trade_date"] = self.trade_date
            self.handle_one_stock_plate(plate_data)


if __name__ == '__main__':
    plate_handler = StockPlateHandler()
    plate_handler.run_stock_plate()
