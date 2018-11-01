#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockPlateBase import StockPlateBase


class StockPlateDayData(StockPlateBase, object):

    def __init__(self):
        super(StockPlateDayData, self).__init__()

    def get_stock_plate_data_list(self):
        sql = "select * from t_sunso_stock_plate where status='normal' order by sort desc "
        return self.select_list_sql(sql)

    def update_plate_total_up_down_ratio(self, plate_data):
        plate_data["total_up_down_ratio"] = self.get_plate_total_up_down_ratio(plate_data)
        sql = self.get_sql_by_template("update_plate_total_up_down_ratio.sql", plate_data)
        self.update_sql(sql)

    def get_plate_total_up_down_ratio(self, plate_data):
        return self.get_plate_index_value("plate_index_total_up_down_ratio_sql.sql", plate_data)

    def init_stock_plate_day_data(self, plate_data):
        plate_data["avg_ratio"] = self.get_plate_avg_ratio(plate_data)
        plate_data["tap_ratio"] = self.get_plate_tap_ratio(plate_data)
        plate_data["mid_ratio"] = self.get_plate_mid_ratio(plate_data)
        plate_data["up_limit_count"] = self.get_plate_up_limit_count(plate_data)
        plate_data["down_limit_count"] = self.get_plate_down_limit_count(plate_data)
        plate_data["up_count"] = self.get_plate_up_count(plate_data)
        plate_data["down_count"] = self.get_plate_down_count(plate_data)
        plate_data["net_amt"] = self.get_plate_net_amt(plate_data)
        sql = self.get_sql_by_template("insert_t_sunso_stock_plate_day_data.sql", plate_data)
        try:
            self.insert_sql(sql)
        except Exception, e:
            print e

    def get_plate_avg_ratio(self, plate_data):
        return self.get_plate_index_value("plate_index_avg_ratio_sql.sql", plate_data)

    def get_plate_tap_ratio(self, plate_data):
        return self.get_plate_index_value("plate_index_tap_ratio_sql.sql", plate_data)

    def get_plate_mid_ratio(self, plate_data):
        return self.get_plate_index_value("plate_index_mid_ratio_sql.sql", plate_data)

    def get_plate_up_limit_count(self, plate_data):
        return self.get_plate_index_value("plate_index_up_limit_count_sql.sql", plate_data)

    def get_plate_down_limit_count(self, plate_data):
        return self.get_plate_index_value("plate_index_down_limit_count_sql.sql", plate_data)

    def get_plate_up_count(self, plate_data):
        return self.get_plate_index_value("plate_index_up_count_sql.sql", plate_data)

    def get_plate_down_count(self, plate_data):
        return self.get_plate_index_value("plate_index_down_count_sql.sql", plate_data)

    def get_plate_net_amt(self, plate_data):
        return self.get_plate_index_value("plate_index_net_amt_sql.sql", plate_data)