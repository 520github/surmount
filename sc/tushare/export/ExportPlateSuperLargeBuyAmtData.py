#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportPlateBase import ExportPlateBase


class ExportSuperLargeBuyAmtData(ExportPlateBase, object):

    def __init__(self):
        self.keywords = "export_stock_confirm_point_data"
        # self.keywords = "export_stock_price_analysis_data"
        super(ExportSuperLargeBuyAmtData, self).__init__()
        self.plate_name = "超级大额资金净流入"
        self.plate_start_date = "2018-10-26"
        print("ExportSuperLargeBuyAmtData init ")


if __name__ == "__main__":
    super_large = ExportSuperLargeBuyAmtData()
    super_large.export_stock_list_to_excel()