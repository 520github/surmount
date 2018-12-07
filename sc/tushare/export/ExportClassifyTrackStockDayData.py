#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportClassifyTrackStockDayData(ExportBaseSqlData, object):
    classify_type = "industry"
    classify_name = "日用化工"
    track_date = "2018-11-02"
    reback_day = 5
    track_sum_day = 5

    def __init__(self):
        self.keywords = "export_classify_track_stock_day_data"
        super(ExportClassifyTrackStockDayData, self).__init__()
        print("ExportClassifyTrackStockDayData init ")

    def get_export_sql_data_list(self):
        sql = "select distinct classify_type,classify_name,track_date,code " \
              "from t_sunso_stock_classify_track_stock_day_data t " \
              " where 1>0 " \
              "and classify_type='" + self.classify_type + "' " \
              "and classify_name='" + self.classify_name + "' " \
              "and track_date='" + self.track_date + "' " \
              "and track_sum_day = " + str(self.track_sum_day) + " " \
              "order by from_track_date_up_down_ratio desc "
        self.data_list = self.select_data_list(sql)

    def get_sql_data_custom(self, data):
        self.sql_data = {"classify_type": data["classify_type"],
                         "classify_name": data["classify_name"],
                         "track_date": data["track_date"],
                         "code": data["code"],
                         "reback_day": self.reback_day
                         }


if __name__ == "__main__":
    ctsd = ExportClassifyTrackStockDayData()
    ctsd.export_sql_data_list_to_excel("code")