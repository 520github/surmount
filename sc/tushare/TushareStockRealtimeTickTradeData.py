#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 获取当前实时的分笔买卖盘的数据情况

#import TushareBase
import tushare as ts
from TushareBase import TushareBase


class TushareStockRealtimeTickTradeData(TushareBase, object):

    def __init__(self):
        super(TushareStockRealtimeTickTradeData, self).__init__()
        self.table_name = "t_tushare_stock_realtime_tick_trade_data"
        print("realtime quotes data")

    def get_realtime_quotes(self, stock_code):
        return ts.get_realtime_quotes(stock_code)

    # 获取某个股票当前实时的分笔数据
    def get_realtime_quotes_to_db(self, stock_code):
        self.delete_one_stock_realtime_quotes_by_date(stock_code)
        self.data_to_db_append(self.get_realtime_quotes(stock_code), self.table_name)

    # 获取所有股票当前实时的分笔数据
    def get_all_realtime_quotes_to_db(self):
        df = self.get_stock_basics()
        for index, row in df.iterrows():
            print("stockeCode-->" + index)
            self.get_realtime_quotes_to_db(index)

    # 获取多个股票的当前实时的分布数据
    def get_mulit_stock_realtime_quotes_to_db(self, mulit_stock_codes):
        for stock_code in mulit_stock_codes:
            self.get_realtime_quotes_to_db(stock_code)

    def delete_one_stock_realtime_quotes_by_date(self, stock_code):
        sql = "delete from " + self.table_name + " where code='" + stock_code + "'"
        self.delete_sql(sql)


# realtime = TushareStockRealtimeTickTradeData()
# realtime.get_all_realtime_quotes_to_db()
# realtime.delete_one_stock_realtime_quotes_by_date("000001")
# realtime.get_realtime_quotes_to_db("000001")