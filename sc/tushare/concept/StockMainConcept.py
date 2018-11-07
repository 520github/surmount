#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockConceptBase import StockConceptBase


class StockMainConcept(StockConceptBase, object):
    join_date = "2018-11-05"

    def __init__(self):
        super(StockMainConcept, self).__init__()
        print("StockMainConcept init")

    def init_stock_main_concept(self):
        data = {"join_date": self.join_date}
        sql = self.get_sql_by_template("insert_t_sunso_stock_concept_classified_venture.sql", data)
        self.insert_sql(sql)

        sql = self.get_sql_by_template("insert_t_sunso_stock_concept_classified_unicorn.sql", data)
        self.insert_sql(sql)


main_concept = StockMainConcept()
main_concept.init_stock_main_concept()