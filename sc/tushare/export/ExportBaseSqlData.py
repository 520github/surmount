#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
from ExportBase import ExportBase
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from FileHandler import FileHandler


class ExportBaseSqlData(ExportBase, object):
    data_list = None

    def __init__(self):
        super(ExportBaseSqlData, self).__init__()
        print("ExportBaseSqlData init ")

    def export_sql_data_to_excel(self):
        self.delete_excel_file()
        self.get_sql_data("")
        self.export_db_data_to_excel_portal()

    def export_sql_data_list_to_excel(self, key):
        self.get_export_sql_data_list()
        if self.data_list is None:
            return
        self.delete_excel_file()
        for data in self.data_list:
            self.get_sql_data_custom(data)
            key_value = data[key]
            self.excel_file_path_name = self.get_excel_file(key_value)
            self.sheet_name = key_value
            self.export_db_data_to_excel_portal()

    def get_export_sql_data_list(self):
        print("no thing doing")

    def get_sql_data_custom(self, data):
        print("no thing doing")

