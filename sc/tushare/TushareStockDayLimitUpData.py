#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 处理每日涨停板相关数据

from TushareBase import TushareBase


class TushareStockDayLimitUpData(TushareBase, object):

    def __init__(self):
        super(TushareStockDayLimitUpData, self).__init__()
        self.table_name = "t_sunso_stock_day_up_limit_data"
        self.log_info("stock day limit up data")

    def save_stock_day_limit_up_from_newly(self):
        sql = "insert into t_sunso_stock_day_up_limit_data(code,name,open_amt,close_amt,low_amt,high_amt," \
              "pre_close_amt,change_percent,trade_volume,trade_amt,turnover_rate,per,pb,market_cap_amt," \
              "circulation_amt,up_limit_date) " \
              "select code,name,open,trade,low,high,settlement,changepercent," \
              "volume,amount,turnoverratio,per,pb,mktcap,nmc,date " \
              "from t_tushare_stock_newly_quotes_data " \
              "where changepercent > " + str(self.limit_up_value);
        self.insert_sql(sql)

    # 处理涨停板相关股票的数据
    def handle_limit_up_stock_data(self):
        data_list = self.get_limit_up_stock_from_newly()
        for data in data_list:
            stock_code = data["code"]
            date = data["date"]
            if self.is_enough_trade_date_from_sunso_stock_all_quotes_data(stock_code, 30):
                self.insert_limit_up_stock_data_from_sunso_all_quotes_data(stock_code, date)
                continue

            min_trade_date = self.get_min_trade_date_from_sunso_stock_all_quotes_data(stock_code)
            count = self.count_stock_from_sunso_stock_all_quotes_data(stock_code)


        return

    def insert_limit_up_stock_data_from_sunso_all_quotes_data(self, stock_code, date):
        sql = "insert into " + self.table_name + "(" + self.get_sunso_stock_quotes_data_column() + ",up_limit_date) " \
              "select " + self.get_sunso_stock_quotes_data_column() + "," + date + " where code='" + stock_code + "' " \
              "order by date desc limit 30"
        self.insert_sql(sql)


# limit = TushareStockDayLimitUpData()
# limit.save_stock_day_limit_up_from_newly()