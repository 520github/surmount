#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockPerformanceReport(BaseFoundationYearAndQuarter, object):

    def __init__(self):
        super(TushareStockPerformanceReport, self).__init__()
        self.table_name = "t_tushare_stock_performance_report"
        self.begin_year = 2018
        self.end_year = 2018
        self.quarters = [4]
        print("TushareStockPerformanceReport init...")

    def get_append_data(self):
        data = ts.get_report_data(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data_and_reset_index(data)
        return data


if __name__ == "__main__":
    pr = TushareStockPerformanceReport()
    pr.get_data()