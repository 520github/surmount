#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportIndustryDayStatisticData(ExportBaseSqlData, object):
    custom_industry = "('旅游服务','批发业','汽车配件','电气设备','仓储物流','水力发电','园区开发','化学制药','染料涂料')"

    def __init__(self):
        self.keywords = "export_industry_day_statistic_data"
        super(ExportIndustryDayStatisticData, self).__init__()
        print("ExportIndustryDayStatisticData init ")

    def get_export_sql_data_list(self):
        sql = "select distinct industry from t_sunso_stock_day_industry_statistic_core_data" \
              " where industry in " + self.custom_industry
        self.data_list = self.select_data_list(sql)

    def get_sql_data_custom(self, data):
        self.sql_data = {"industry": data["industry"]}


if __name__ == "__main__":
    id = ExportIndustryDayStatisticData()
    id.export_sql_data_list_to_excel("industry")