#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from TemplateHandler import TemplateHandler
from DateHandler import DateHandler

class StockConceptBase(DbHandler, object):

    def __init__(self):
        super(StockConceptBase, self).__init__()
        print("StockConceptBase init")

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        return "./sql/"