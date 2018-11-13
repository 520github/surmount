#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation
import tushare as ts


class TushareStockPerformanceForecast(BaseFoundation, object):
    begin_year = 2017
    end_year = 2018
    quarters = [1, 2, 3, 4]
    quarter = 1

    def __init__(self):
        super(TushareStockPerformanceForecast, self).__init__()
        self.table_name = "t_tushare_stock_performance_forecast"
        print("TushareStockPerformanceForecast init...")

    def get_append_data(self):
        data = ts.forecast_data(self.begin_year, self.quarter)
        data["year"] = self.begin_year
        data["quarter"] = self.quarter
        data["date"] = self.get_now_ymd_str()
        return data

    def delete_table_data_before_append(self):
        sql = "delete from " + self.table_name + " " \
              "where year=" + str(self.begin_year) + " and quarter=" + str(self.quarter)
        self.delete_sql(sql)

    def get_performance_forecast(self):
        while self.begin_year <= self.end_year:
            self.__get_performance_forecast_by_year()

    def __get_performance_forecast_by_year(self):
        for q in self.quarters:
            self.quarter = q
            self.__get_performance_forecast_by_year_and_quarter()
        self.begin_year = self.begin_year + 1

    def __get_performance_forecast_by_year_and_quarter(self):
        self.append_data_to_table()


if __name__ == "__main__":
    pf = TushareStockPerformanceForecast()
    pf.get_performance_forecast()