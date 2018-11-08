#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from ExcelHandler import ExcelHandler
from TemplateHandler import TemplateHandler


class ExportBase(DbHandler, ExcelHandler, object):
    sql_template_key = None
    sql_data = None
    excel_file_path_name = None
    sheet_name = None

    def __init__(self):
        super(ExportBase, self).__init__()
        print("ExportBase init ")

    def export_db_data_to_excel_portal(self):
        self.export_db_data_to_excel(self.sql_template_key, self.sql_data, self.excel_file_path_name)

    def export_db_data_to_excel(self, sql_template_key, sql_data, excel_file_path_name):
        sql = self.get_sql_by_template(sql_template_key, sql_data)
        data_list = self.select_data_list(sql)
        self.export_data_to_excel_copy(data_list, excel_file_path_name, self.sheet_name)

    def select_data_list(self, sql):
        return self.select_list_sql(sql)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        return sql

    def get_tempalte_path(self):
        return "./sql/"

    def get_excel_file_path_name(self, keywords, code):
        return self.get_excel_file_path() + keywords + "_" + code + ".xls"

    def get_excel_file_path(self):
        return "/Users/sunso520/Downloads/"
