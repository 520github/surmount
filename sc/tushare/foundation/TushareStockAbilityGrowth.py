#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockAbilityGrowth(BaseFoundationYearAndQuarter, object):
    def __init__(self):
        super(TushareStockAbilityGrowth, self).__init__()
        self.table_name = "t_tushare_stock_ability_growth"
        print("TushareStockAbilityGrowth init...")

    def get_append_data(self):
        data = ts.get_growth_data(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data_and_reset_index(data)
        return data


if __name__ == "__main__":
    ag = TushareStockAbilityGrowth()
    ag.get_data()