#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
from ExportBase import ExportBase
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from FileHandler import FileHandler


class ExportBaseSqlData(ExportBase, object):

    def __init__(self):
        super(ExportBaseSqlData, self).__init__()
        print("ExportBaseSqlData init ")

    def export_sql_data_to_excel(self):
        self.get_sql_data("")
        self.excel_file_path_name = self.get_excel_file("all")
        if not self.is_alone_file:
            if FileHandler.is_exist_file(self.excel_file_path_name):
                FileHandler.remove_file(self.excel_file_path_name)

        self.export_db_data_to_excel_portal()
