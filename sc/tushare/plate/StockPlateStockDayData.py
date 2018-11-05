#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockPlateBase import StockPlateBase


class StockPlateStockDayData(StockPlateBase, object):
    def __init__(self):
        super(StockPlateStockDayData, self).__init__()

    def init_stock_plate_stock_data(self, plate_data):
        key = plate_data["sql_template_key"]
        # now_date = self.get_now_ymd_str()
        plate_data["join_date"] = plate_data["trade_date"]
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
        if data_list is None:
            return
        for data in data_list:
            plate_data["code"] = data["code"]
            total_up_down_ratio = self.get_plate_stock_total_up_down_ratio(plate_data)
            plate_data["total_up_down_ratio"] = total_up_down_ratio
            total_count = self.get_plate_stock_total_count(plate_data)
            plate_data["total_count"] = total_count
            plate_data["avg_up_down_ratio"] = self.cal_division_round_2(total_up_down_ratio, total_count)

            large_above_total_bs_trade_amt = self.get_plate_stock_total_bs_trade_amt(plate_data)
            plate_data["large_above_total_bs_trade_amt"] = large_above_total_bs_trade_amt
            trade_amt = self.get_plate_stock_trade_amt(plate_data)
            plate_data["large_above_total_bs_trade_amt_ratio"] = self.cal_percent_round_2(large_above_total_bs_trade_amt, trade_amt)

            plate_data["first_up_down_ratio"] = self.get_plate_stock_pre_up_down_ratio(plate_data, "up_down_ratio", "asc")
            plate_data["first_pre3_up_down_ratio"] = self.get_plate_stock_pre_up_down_ratio(plate_data, "pre3_up_down_ratio", "asc")
            plate_data["first_pre5_up_down_ratio"] = self.get_plate_stock_pre_up_down_ratio(plate_data, "pre5_up_down_ratio", "asc")
            first_close_amt = self.get_plate_stock_pre_up_down_ratio(plate_data, "close_amt", "asc")
            plate_data["first_close_amt"] = first_close_amt

            plate_data["last_pre3_up_down_ratio"] = self.get_plate_stock_pre_up_down_ratio(plate_data, "pre3_up_down_ratio", "desc")
            plate_data["last_pre5_up_down_ratio"] = self.get_plate_stock_pre_up_down_ratio(plate_data, "pre5_up_down_ratio", "desc")
            last_close_amt = self.get_plate_stock_pre_up_down_ratio(plate_data, "close_amt", "desc")
            plate_data["last_close_amt"] = last_close_amt

            last_circulation_amt = self.get_plate_stock_pre_up_down_ratio(plate_data, "circulation_amt", "desc")
            plate_data["last_circulation_amt"] = last_circulation_amt
            plate_data["large_above_total_bs_trade_last_circulatio_ratio"] = self.cal_percent_round_2(large_above_total_bs_trade_amt/10000, last_circulation_amt)

            plate_data["last_first_close_amt_ratio"] = self.cal_percent_round_2_not_zero(last_close_amt, first_close_amt)

            sql = self.get_sql_by_template("update_stock_plate_stock.sql", plate_data)
            self.update_sql(sql)

    def get_stock_plate_stock_by_plate(self, plate_data):
        sql = self.get_sql_by_template("get_stock_plate_stock_by_plate.sql", plate_data)
        return self.select_list_sql(sql)

    def get_plate_stock_total_up_down_ratio(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_total_up_down_ratio_sql.sql", plate_data)

    def get_plate_stock_total_count(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_total_count_sql.sql", plate_data)

    def get_plate_stock_trade_amt(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_trade_amt_sql.sql", plate_data)

    def get_plate_stock_total_bs_trade_amt(self, plate_data):
        return self.get_plate_index_value("plate_stock_index_total_bs_trade_amt_sql.sql", plate_data)

    def get_plate_stock_pre_up_down_ratio(self, plate_data, column_name, sort):
        plate_data["pre_column_name"] = column_name
        plate_data["sort"] = sort
        return self.get_plate_index_value("plate_stock_index_pre_up_down_ratio_sql.sql", plate_data)