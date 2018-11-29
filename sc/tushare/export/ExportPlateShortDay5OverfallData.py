#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportPlateBase import ExportPlateBase


class ExportPlateShortDay5OverfallData(ExportPlateBase, object):

    def __init__(self):
        self.keywords = "export_stock_confirm_point_data"
        # self.keywords = "export_stock_price_analysis_data"
        super(ExportPlateShortDay5OverfallData, self).__init__()
        self.plate_name = "短期5天超跌"
        self.plate_start_date = "2018-10-31"
        print("ExportPlateShortDay5OverfallData init ")


if __name__ == "__main__":
    turnover_rate = ExportPlateShortDay5OverfallData()
    turnover_rate.export_stock_list_to_excel()