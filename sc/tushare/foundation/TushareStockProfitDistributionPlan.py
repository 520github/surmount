#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation
import tushare as ts


class TushareStockProfitDistributionPlan(BaseFoundation, object):
    begin_year = 2018
    end_year = 2018
    top = 4000

    def __init__(self):
        super(TushareStockProfitDistributionPlan, self).__init__()
        self.table_name = "t_tushare_stock_profit_distribution_plan"
        print("TushareStockProfitDistributionPlan init...")

    def get_append_data(self):
        data = ts.profit_data(self.begin_year, self.top)
        data["date"] = self.get_now_ymd_str()
        return data

    def delete_table_data_before_append(self):
        sql = "delete from " + self.table_name + " where year=" + str(self.begin_year)
        self.delete_sql(sql)

    def get_profit_distribution_plan(self):
        while self.begin_year <= self.end_year:
            print("begin_year-->" + str(self.begin_year))
            self.__get_profit_distribution_plan_by_year__()

    def __get_profit_distribution_plan_by_year__(self):
        self.append_data_to_table()
        self.begin_year = self.begin_year + 1


if __name__ == "__main__":
    pdp = TushareStockProfitDistributionPlan()
    pdp.get_profit_distribution_plan()