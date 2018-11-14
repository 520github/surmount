#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt
import xlrd
from xlutils.copy import copy
from SortHandler import SortHandler
from FileHandler import FileHandler


class ExcelHandler(object):

    def __init__(self):
        print("ExcelHandler init")

    @staticmethod
    def export_data_to_excel_copy(dict_data_list, file_name, sheet_name=None):
        if FileHandler.is_exist_file(file_name):
            workbook = xlrd.open_workbook(file_name)
            new_workbook = copy(workbook)
            ExcelHandler.__create_sheet_and_write_data__(new_workbook, dict_data_list, file_name, sheet_name)
        else:
            ExcelHandler.export_data_to_new_excel(dict_data_list, file_name, sheet_name)

    @staticmethod
    def export_data_to_new_excel(dict_data_list, file_name, sheet_name=None):
        workbook = xlwt.Workbook()
        ExcelHandler.__create_sheet_and_write_data__(workbook, dict_data_list, file_name, sheet_name)

    @staticmethod
    def __create_sheet_and_write_data__(workbook, dict_data_list, file_name, sheet_name):
        sheet = ExcelHandler.__create_sheet__(workbook, sheet_name)
        ExcelHandler.__write_data_to_excel__(sheet, dict_data_list)
        workbook.save(r"%s" % file_name)
        return True

    @staticmethod
    def __create_sheet__(workbook, sheet_name):
        if sheet_name is None:
            sheet_name = "sheet1"
        sheet_name = u'%s' % sheet_name
        return workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

    @staticmethod
    def __write_data_to_excel__(sheet, dict_data_list):
        if dict_data_list is None:
            return False
        if len(dict_data_list) < 1:
            return False
        keys = SortHandler.get_sort_keys_by_dict_data_list(dict_data_list)
        data_list = SortHandler.get_dict_data_list_by_sort_key(dict_data_list)
        for i in range(0, len(keys)):
            col_key = u'%s' % keys[i]
            sheet.write(0, i, col_key)

        for row in range(1, len(data_list) + 1):
            for col in range(0, len(keys)):
                col_value = u'%s' % data_list[row - 1][col]
                sheet.write(row, col, col_value)
        return True

# data_list = [{"name":"力挺","sex":"男","age":10},{"name":"无情","sex":"女","age":11}]
# file_name = "/Users/sunso520/Downloads/name_姓名.xls"
# ExcelHandler.export_data_to_excel(data_list, file_name)

