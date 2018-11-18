#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockFundHolding(BaseFoundationYearAndQuarter, object):
    def __init__(self):
        super(TushareStockFundHolding, self).__init__()
        self.table_name = "t_tushare_stock_fund_holding"
        self.begin_year = 2018
        self.end_year = 2018
        self.quarters = [3]
        print("TushareStockFundHolding init...")

    def get_append_data(self):
        data = ts.fund_holdings(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data_and_reset_index(data, "handle_date")
        return data


if __name__ == "__main__":
    ag = TushareStockFundHolding()
    ag.get_data()