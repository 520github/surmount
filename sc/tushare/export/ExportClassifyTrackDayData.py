#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportClassifyTrackDayData(ExportBaseSqlData, object):
    def __init__(self):
        self.keywords = "export_classify_track_day_data"
        super(ExportClassifyTrackDayData, self).__init__()
        print("ExportClassifyTrackDayData init ")

    def get_export_sql_data_list(self):
        sql = "select t.*,concat(classify_name,track_date) as ukey from t_sunso_stock_classify_track_basic t " \
              " where 1>0 "
        self.data_list = self.select_data_list(sql)

    def get_sql_data_custom(self, data):
        self.sql_data = {"classify_type": data["classify_type"],
                         "classify_name": data["classify_name"],
                         "track_date": data["track_date"]
                         }


if __name__ == "__main__":
    ctdd = ExportClassifyTrackDayData()
    ctdd.export_sql_data_list_to_excel("ukey")