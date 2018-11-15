#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation


class TushareStockDragonTigerDayTotalData(BaseFoundation, object):

    trade_date = ""

    def __init__(self):
        super(TushareStockDragonTigerDayTotalData, self).__init__()
        self.table_name = "t_sunso_stock_dragon_tiger_day_total_data"
        print("TushareStockDragonTigerDayTotalData init...")

    def load_dragon_tiger_day_total_data(self):
        date_list = self.get_date_list()
        if date_list is None:
            return
        for date in date_list:
            self.trade_date = date["date"]
            self.load_dragon_tiger_day_total_data_by_one_date()

    def load_dragon_tiger_day_total_data_by_one_date(self):
        template_key = "dragon_tiger_day_total_data.sql"
        sql = self.get_sql_by_template(template_key, self.get_template_data())
        # print(sql)
        self.insert_sql(sql)

    def get_date_list(self):
        sql = "select distinct date from t_tushare_stock_dragon_tiger_sale_total_data " \
              "where date not in (select distinct trade_date " \
              "from " + self.table_name + ") "
        return self.select_list_sql(sql)

    def delete_dragon_tiger_day_total_data(self):
        sql = "delete from " + self.table_name + " " \
              "where trade_date='" + self.trade_date + "'"
        self.delete_sql(sql)

    def get_template_data(self):
        data = {"trade_date": self.trade_date}
        return data


if __name__ == "__main__":
    dragon_tiger = TushareStockDragonTigerDayTotalData()
    dragon_tiger.load_dragon_tiger_day_total_data()