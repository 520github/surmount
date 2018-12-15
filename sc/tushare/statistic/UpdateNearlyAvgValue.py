#!/usr/bin/python
# -*- coding: UTF-8 -*-
from StatisticBase import StatisticBase


class UpdateNearlyAvgValue(StatisticBase, object):

    t_sunso_stock_day_trade_statistic_range_avg_data = "t_sunso_stock_day_trade_statistic_range_avg_data"

    def __init__(self):
        super(UpdateNearlyAvgValue, self).__init__()
        print("UpdateNearlyAvgValue init")

    def update_nearly_by_list_date(self):
        date_list = self.get_date_list()
        for date in date_list:
            self.update_nearly_by_one_date(self.get_date_str(date["trade_date"]))

    def update_nearly_by_one_date(self, trade_date):
        print("trade_date-->" + trade_date)
        for column in self.update_nearly_column_list:
            limit = column.split("_")[0].split("nearly")[1]
            self.update_nearly_by_one_date_and_column(trade_date, column, limit)

    def update_nearly_by_one_date_and_column(self, trade_date, column, limit):
        data = {"trade_date": trade_date, "column": column, "limit": limit}
        template_key = "update_nearly_avg_value.sql"
        sql = self.get_sql_by_template(template_key, data)
        self.update_sql(sql)

    def update_continue_above_avg_day_by_list_date(self):
        date_list = self.get_date_list()
        for date in date_list:
            trade_date = self.get_date_str(date["trade_date"])
            print("trade_date-->" + trade_date)
            self.update_continue_above_avg_day_by_one_date(trade_date)

    def update_continue_above_avg_day_by_one_date(self, trade_date):
        sql = "select * from " + self.t_sunso_stock_day_trade_statistic_range_avg_data + " " \
              "where 1 >0 " \
              "and trade_date='" + trade_date + "' and continue_above_nearly5_avg_day < 0 " \
              # "and code='300532' "
        data_list = self.select_data_list(sql)
        for data in data_list:
            self.update_continue_above_avg_day_by_stock(data)

    def update_continue_above_avg_day_by_stock(self, data):
        template_key = "update_continue_above_avg_day.sql"
        data = self.get_continue_above_avg_day_data(data)
        sql = self.get_sql_by_template(template_key, data)
        self.update_sql(sql)

    def get_date_list(self):
        sql = "select distinct trade_date from " \
              "" + self.t_sunso_stock_day_trade_statistic_core_data + " " \
"where 1 > 0 and trade_date between '2018-10-31' and '2018-12-13' " \
              " order by trade_date asc "
        date_list = self.select_data_list(sql)
        return date_list


if __name__ == "__main__":
    up = UpdateNearlyAvgValue()
    # up.update_nearly_by_list_date()
    up.update_continue_above_avg_day_by_list_date()