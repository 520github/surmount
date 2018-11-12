#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportPlateBase import ExportPlateBase


class ExportPlateTurnoverRateChangeMoreData(ExportPlateBase, object):

    def __init__(self):
        # self.keywords = "export_stock_confirm_point_data"
        self.keywords = "export_stock_price_analysis_data"
        super(ExportPlateTurnoverRateChangeMoreData, self).__init__()
        self.plate_name = "换手率变大"
        self.plate_start_date = "2018-11-07"
        print("ExportPlateTurnoverRateChangeMoreData init ")


if __name__ == "__main__":
    turnover_rate = ExportPlateTurnoverRateChangeMoreData()
    turnover_rate.export_stock_list_to_excel()