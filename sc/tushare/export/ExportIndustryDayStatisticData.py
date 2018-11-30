#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportIndustryDayStatisticData(ExportBaseSqlData, object):
    custom_industry = ""

    def __init__(self):
        # self.keywords = "export_stock_high_transfer_data"
        self.keywords = "export_plate_stock_list_data"
        super(ExportIndustryDayStatisticData, self).__init__()
        print("ExportIndustryDayStatisticData init ")

    def get_export_sql_data_list(self):
        sql = "select * from t_sunso_stock_plate where status='normal' "
        self.data_list = self.select_data_list(sql)

    def get_sql_data_custom(self, data):
        self.sql_data = {"plate_name": data["plate_name"],
                         "plate_start_date": data["plate_start_date"]}