#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from DbEngineHandler import DbEngineHandler
from DateHandler import DateHandler
from TemplateHandler import TemplateHandler


class BaseFoundation(DbHandler, DbEngineHandler, object):

    table_name = None

    def __init__(self):
        super(BaseFoundation, self).__init__()
        DbEngineHandler.__init__(self)
        print("BaseFoundation init")

    def get_append_data(self):
        return None

    def delete_table_data_before_append(self):
        print("delete table data do nothing")

    def append_data_to_table(self):
        data = self.get_append_data()
        if data is not None:
            self.delete_table_data_before_append()
        self.data_to_db_append(data, self.table_name)

    def get_now_ymd_str(self):
        return DateHandler.get_now_ymd_str()

    def get_delete_sql_by_year_and_quarter(self, year, quarter):
        sql = "delete from " + self.table_name + " " \
              "where year=" + str(year) + " and quarter=" + str(quarter)
        return sql

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        return path + "/sql/"