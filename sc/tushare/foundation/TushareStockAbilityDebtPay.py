#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
import tushare as ts


class TushareStockAbilityDebtPay(BaseFoundationYearAndQuarter, object):

    def __init__(self):
        super(TushareStockAbilityDebtPay, self).__init__()
        self.table_name = "t_tushare_stock_ability_debt_pay"
        print("TushareStockAbilityDebtPay init...")

    def get_append_data(self):
        data = ts.get_debtpaying_data(self.begin_year, self.quarter)
        self.append_year_and_quater_to_data_and_reset_index(data)
        return data


if __name__ == "__main__":
    ad = TushareStockAbilityDebtPay()
    ad.get_data()