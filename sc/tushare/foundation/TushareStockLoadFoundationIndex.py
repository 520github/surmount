#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation
from TushareStockAbilityProfit import TushareStockAbilityProfit
from BaseFoundationYearAndQuarter import BaseFoundationYearAndQuarter
from TushareStockPerformanceReport import TushareStockPerformanceReport
from TushareStockAbilityOperation import TushareStockAbilityOperation
from TushareStockAbilityGrowth import TushareStockAbilityGrowth
from TushareStockAbilityDebtPay import TushareStockAbilityDebtPay
from TushareStockAbilityCashFlow import TushareStockAbilityCashFlow


class TushareStockLoadFoundationIndex(BaseFoundation, object):

    is_delete_before_insert = True
    year = "(2018)"
    quarter = "(1,2,3)"

    def __init__(self):
        self.table_name = "t_sunso_stock_foundation_index"
        super(TushareStockLoadFoundationIndex, self).__init__()
        BaseFoundationYearAndQuarter.begin_year = 2018
        BaseFoundationYearAndQuarter.end_year = 2018
        BaseFoundationYearAndQuarter.quarters = [1, 2, 3]
        print("TushareStockLoadFoundationIndex init...")

    def init_foundation_about_data(self):
        # pr = TushareStockPerformanceReport()
        # pr.get_data()

        ap = TushareStockAbilityProfit()
        ap.get_data()

        ao = TushareStockAbilityOperation()
        ao.get_data()

        ag = TushareStockAbilityGrowth()
        ag.get_data()

        ad = TushareStockAbilityDebtPay()
        ad.get_data()

        acf = TushareStockAbilityCashFlow()
        acf.get_data()

    def load_foundation_index(self):
        # self.init_foundation_about_data()

        if self.is_delete_before_insert:
            self.delete_foundation_index()

        template_key = "load_foundation_index.sql"
        sql = self.get_sql_by_template(template_key, self.get_template_data())
        print(sql)
        self.insert_sql(sql)

    def delete_foundation_index(self):
        sql = "delete from " + self.table_name + " " \
              "where year in " + self.year + " and quarter in " + self.quarter
        self.delete_sql(sql)

    def get_template_data(self):
        data = {"year": self.year, "quarter": self.quarter}
        print(data)
        return data


if __name__ == "__main__":
    index = TushareStockLoadFoundationIndex()
    index.load_foundation_index()
    # index.init_foundation_about_data()