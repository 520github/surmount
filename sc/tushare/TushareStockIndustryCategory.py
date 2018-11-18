#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取股票的行业分类数据

from TushareBase import TushareBase
import tushare as ts


class TushareStockIndustryCategory(TushareBase, object):

    def __init__(self):
        super(TushareStockIndustryCategory, self).__init__()
        print("industry category")

    def get_all_stock_industry_category_data(self):
        return ts.get_industry_classified()

    def get_all_stock_industry_category_data_to_db(self):
        self.data_to_db_append(self.get_all_stock_industry_category_data(), "t_tushare_stock_industry_category")


# industry = TushareStockIndustryCategory()
# industry.get_all_stock_industry_category_data_to_db()