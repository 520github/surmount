#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ExportBaseSqlData import ExportBaseSqlData


class ExportAlarmSameDayBeforeHighAfterLow(ExportBaseSqlData, object):

    trade_date = "2018-11-19"

    def __init__(self):
        self.keywords = "export_alarm_same_day_before_high_after_low"
        super(ExportAlarmSameDayBeforeHighAfterLow, self).__init__()
        print("ExportAlarmSameDayBeforeHighAfterLow init ")

    def export_sql_data_to_excel(self):
        self.delete_excel_file()
        self.get_sql_data("")
        data_list = self.export_db_data_to_excel_portal()
        self.export_netx_date_data(data_list)

    def get_sql_data(self, code):
        self.sql_data = {"trade_date": self.trade_date}

    def get_next_date(self):
        sql = "select distinct trade_date as c " \
              "from t_sunso_stock_day_trade_statistic_core_data " \
              "where trade_date>'" + self.trade_date + "' " \
              "order by trade_date asc limit 1"
        return self.count_sql(sql)

    def export_netx_date_data(self, data_list):
        if data_list is None or len(data_list) < 1:
            return
        next_date = self.get_next_date()
        if next_date is None:
            return
        stocks = self.get_stocks_in_str_by_data_list(data_list)
        self.sql_data = {"trade_date": next_date, "codes": stocks}
        self.sql_template_key = "export_alarm_same_day_before_low_after_high_next_day.sql"
        self.sheet_name = "next_date"
        self.export_db_data_to_excel_portal()


if __name__ == "__main__":
    blah = ExportAlarmSameDayBeforeHighAfterLow()
    blah.export_sql_data_to_excel()