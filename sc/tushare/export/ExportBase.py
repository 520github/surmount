#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../common'))
from DbHandler import DbHandler
from ExcelHandler import ExcelHandler
from TemplateHandler import TemplateHandler
from FileHandler import FileHandler


class ExportBase(DbHandler, ExcelHandler, object):
    sql_template_key = None
    sql_data = None
    excel_file_path_name = None
    sheet_name = None
    is_alone_file = False
    keywords = None

    def __init__(self):
        super(ExportBase, self).__init__()
        self.sql_template_key = self.keywords + ".sql"
        print("ExportBase init ")

    def export_stock_list_to_excel(self):
        self.delete_excel_file()
        stock_list = self.get_stock_list()
        if stock_list is None or len(stock_list) < 1:
            return

        for code in stock_list:
            self.get_sql_data(code)
            self.excel_file_path_name = self.get_excel_file(code)
            self.sheet_name = code
            self.export_db_data_to_excel_portal()

    def delete_excel_file(self):
        if not self.is_alone_file:
            self.excel_file_path_name = self.get_excel_file("all")
            if FileHandler.is_exist_file(self.excel_file_path_name):
                FileHandler.remove_file(self.excel_file_path_name)

    def get_excel_file(self, code):
        if not self.is_alone_file:
            code = "all"
        return self.get_excel_file_path_name(self.keywords, code)

    def get_stock_list(self):
        return None

    def get_sql_data(self, code):
        self.sql_data = {"code": code}

    def get_stock_list_by_sql(self, sql):
        data_list = self.select_data_list(sql)
        return self.get_stocks_by_data_list(data_list)

    def get_stocks_by_data_list(self, data_list):
        if data_list is None or len(data_list) < 1:
            return None
        stock_list = []
        for data in data_list:
            stock_list.append(data["code"])
        return stock_list

    def get_stocks_in_str_by_data_list(self, data_list):
        if data_list is None or len(data_list) < 1:
            return None
        stocks = "("
        for data in data_list:
            stocks = stocks + "'" + data["ac_code"] + "',"
        stocks = stocks + "'')"
        return stocks

    def export_db_data_to_excel_portal(self):
        return self.export_db_data_to_excel(self.sql_template_key, self.sql_data, self.excel_file_path_name)

    def export_db_data_to_excel(self, sql_template_key, sql_data, excel_file_path_name):
        sql = self.get_sql_by_template(sql_template_key, sql_data)
        data_list = self.select_data_list(sql)
        self.export_data_to_excel_copy(data_list, excel_file_path_name, self.sheet_name)
        return data_list

    def select_data_list(self, sql):
        return self.select_list_sql(sql)

    def get_sql_by_template(self, template_key, data):
        sql = TemplateHandler.get_template_content_by_key(template_key, self.get_tempalte_path(), data)
        # print(sql)
        return sql

    def get_tempalte_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        return path + "/sql/"

    def get_excel_file_path_name(self, keywords, code):
        return self.get_excel_file_path() + keywords + "_" + code + ".xls"

    def get_excel_file_path(self):
        #return "/Users/sunso520/Downloads/"
        return "G:\\surmount\\export\\"
