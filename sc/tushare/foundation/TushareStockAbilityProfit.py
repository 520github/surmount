#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockAbilityProfit(BaseFoundationYearAndQuarter, object):
    def __init__(self):
        super(TushareStockAbilityProfit, self).__init__()
        self.table_name = "t_tushare_stock_abitity_profit"
        print("TushareStockAbilityProfit init...")

    def get_append_data(self):
        data = ts.get_profit_data(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data(data)
        return data


if __name__ == "__main__":
    ap = TushareStockAbilityProfit()
    ap.get_data()