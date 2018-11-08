#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBase import ExportBase
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from FileHandler import FileHandler


class ExportSuperLargeBuyAmtData(ExportBase, object):
    keywords = "export_super_large_buy_amt_data"
    stock_list = ["002668", "600122"]
    is_alone_file = False

    def __init__(self):
        super(ExportSuperLargeBuyAmtData, self).__init__()
        self.sql_template_key = self.keywords + ".sql"
        print("ExportSuperLargeBuyAmtData")

    def export_stock_list_to_excel(self):
        if not self.is_alone_file:
            all_excel_file = self.get_excel_file("")
            if FileHandler.is_exist_file(all_excel_file):
                FileHandler.remove_file(all_excel_file)

        for code in self.stock_list:
            self.sql_data = {"code": code}
            self.excel_file_path_name = self.get_excel_file(code)
            self.sheet_name = code
            self.export_db_data_to_excel_portal()

    def get_excel_file(self, code):
        if not self.is_alone_file:
            code = "all"
        return self.get_excel_file_path_name(self.keywords, code)


super_large = ExportSuperLargeBuyAmtData()
super_large.export_stock_list_to_excel()