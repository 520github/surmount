#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockAbilityOperation(BaseFoundationYearAndQuarter, object):

    def __init__(self):
        super(TushareStockAbilityOperation, self).__init__()
        self.table_name = "t_tushare_stock_ability_operation"
        print("TushareStockAbilityOperation init...")

    def get_append_data(self):
        data = ts.get_operation_data(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data_and_reset_index(data)
        return data


if __name__ == "__main__":
    ao = TushareStockAbilityOperation()
    ao.get_data()