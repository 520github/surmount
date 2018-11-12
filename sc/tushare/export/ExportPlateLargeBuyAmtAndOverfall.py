#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportPlateBase import ExportPlateBase


class ExportPlateLargeBuyAmtAndOverfall(ExportPlateBase, object):

    def __init__(self):
        self.keywords = "export_stock_confirm_point_data"
        self.keywords = "export_stock_price_analysis_data"
        super(ExportPlateLargeBuyAmtAndOverfall, self).__init__()
        self.plate_name = "大额资金净流入和短期内跌幅较大"
        self.plate_start_date = "2018-10-26"
        print("ExportPlateLargeBuyAmtAndOverfall init ")


if __name__ == "__main__":
    overfall = ExportPlateLargeBuyAmtAndOverfall()
    overfall.export_stock_list_to_excel()