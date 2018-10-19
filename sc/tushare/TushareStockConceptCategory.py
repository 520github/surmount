#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取股票的概念分类数据

from TushareBase import TushareBase
import tushare as ts


class TushareStockConceptCategory(TushareBase, object):

    def __init__(self):
        super(TushareStockConceptCategory, self).__init__()
        self.table_name = "t_tushare_stock_concept_category"
        print("concept category")

    def get_all_stock_concept_category_data(self):
        return ts.get_concept_classified()

    def get_all_stock_concept_category_data_to_db(self):
        sql = "delete from " + self.table_name
        self.delete_sql(sql)
        self.data_to_db_append(self.get_all_stock_concept_category_data(), self.table_name)


industry = TushareStockConceptCategory()
industry.get_all_stock_concept_category_data_to_db()