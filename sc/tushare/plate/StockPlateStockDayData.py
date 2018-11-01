#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockPlateBase import StockPlateBase


class StockPlateStockDayData(StockPlateBase, object):
    def __init__(self):
        super(StockPlateStockDayData, self).__init__()

    def init_stock_plate_stock_data(self, plate_data):
        key = plate_data["sql_template_key"]
        now_date = self.get_now_ymd_str()
        plate_data["join_date"] = now_date
        sql = self.get_sql_by_template(key, plate_data)
        try:
            self.insert_sql(sql)
        except Exception, e:
            print e

    def init_stock_plate_stock_day_data(self, plate_data):
        sql = self.get_sql_by_template("insert_t_sunso_stock_plate_stock_day_data.sql", plate_data)
        try:
            self.insert_sql(sql)
        except Exception, e:
            print e

    def update_stock_plate_stock(self, plate_data):
        data_list = self.get_stock_plate_stock_by_plate(plate_data)
        for data in data_list:
            plate_data["code"] = data["code"]
            plate_data["total_up_down_ratio"] = self.get_plate_stock_total_up_down_ratio(plate_data)
            plate_data["total_count"] = self.get_plate_stock_total_count(plate_data)
            sql = self.get_sql_by_template("update_stock_plate_stock.sql", plate_data)
            self.update_sql(sql)

    def get_stock_plate_stock_by_plate(self, plate_data):
        sql = self.get_sql_by_template("get_stock_plate_stock_by_plate.sql", plate_data)
        return self.select_list_sql(sql)

    def get_plate_stock_total_up_down_ratio(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_total_up_down_ratio_sql.sql", plate_data)

    def get_plate_stock_total_count(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_total_count_sql.sql", plate_data)
