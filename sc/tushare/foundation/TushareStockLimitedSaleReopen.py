#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation
import tushare as ts


class TushareStockLimitedSaleReopen(BaseFoundation, object):
    begin_year = 2019
    end_year = 2019
    begin_month = 1
    end_month = 12
    month = begin_month

    def __init__(self):
        super(TushareStockLimitedSaleReopen, self).__init__()
        self.table_name = "t_tushare_stock_limited_sale_reopen"
        print("TushareStockLimitedSaleReopen init...")

    def get_append_data(self):
        data = ts.xsg_data(year=self.begin_year, month=self.month)
        data["year"] = self.begin_year
        data["month"] = self.month
        data["handle_date"] = self.get_now_ymd_str()
        return data

    def delete_table_data_before_append(self):
        sql = "delete from " + self.table_name + " " \
              "where year=" + str(self.begin_year) + " and month=" + str(self.month)
        self.delete_sql(sql)

    def get_data(self):
        while self.begin_year <= self.end_year:
            self.__get_data_by_year__()

    def __get_data_by_year__(self):
        self.month = self.begin_month
        while self.month <= self.end_month:
            self.__get_data_by_year_and_month__()
            self.month = self.month + 1
        self.begin_year = self.begin_year + 1

    def __get_data_by_year_and_month__(self):
        self.append_data_to_table()


if __name__ == "__main__":
    lsr = TushareStockLimitedSaleReopen()
    lsr.get_data()