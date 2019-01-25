#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportStockNShadeNDayBigTurnover(ExportBaseSqlData, object):

    trade_date = "2019-01-23"
    days = [5, 10, 20]
    shades = {
        "two": "export_stock_two_shade_and_n_day_big_turnover",
        "three": "export_stock_three_shade_and_n_day_big_turnover",
        "four": "export_stock_four_shade_and_n_day_big_turnover",
        "five": "export_stock_five_shade_and_n_day_big_turnover",
        "six": "export_stock_six_shade_and_n_day_big_turnover"
    }

    def __init__(self):
        self.keywords = "export_stock_n_shade_and_n_day_big_turnover_" + self.trade_date
        super(ExportStockNShadeNDayBigTurnover, self).__init__()
        print("ExportStockNShadeNDayBigTurnover init ")

    def get_export_sql_data_list(self):
        data = []
        for shade in self.shades.keys():
            template = self.shades[shade]
            for limit in self.days:
                data.append(self.get_data(limit, shade, template))
        self.data_list = data

    def get_data(self, limit, shade, template):
        self.sql_template_key = template + ".sql"
        key = shade + "_" + str(limit)
        return {"trade_date": self.trade_date, "limit": limit, "key": key}

    def get_sql_data_custom(self, data):
        print(data["key"])
        self.sql_data = data


if __name__ == "__main__":
    one = ExportStockNShadeNDayBigTurnover()
    # one.export_sql_data_to_excel()
    one.export_sql_data_list_to_excel("key")