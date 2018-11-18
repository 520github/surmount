#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 股票基本信息数据

from TushareBase import TushareBase
import tushare as ts


class TushareStockBasic(TushareBase, object):

    def __init__(self):
        super(TushareStockBasic, self).__init__()
        self.table_name = self.t_tushare_stock_basic
        print("TushareStockBasic init")

    def insert_sunso_stock_basic_from_tushare_stock_basic(self):
        # self.delete_tushare_stock_basic()
        if not self.is_exist_sunso_stock_basic_by_date():
            self.get_stock_basics_to_db()
            self.insert_sunso_stock_basic()
            self.update_sunso_stock_basic()

    def delete_tushare_stock_basic(self):
        sql = "delete from " + self.table_name + " where date='" + self.get_latest_work_day() + "'"
        self.delete_sql(sql)

    def insert_sunso_stock_basic(self):
        sql = "insert into " + self.t_sunso_stock_basic + "(code,name,industry,area,pe,pb,earnings_per_share," \
              "net_asset_per_share,circulation_stock_volume,totals_stock_volume,totals_stock_amt,total_assets," \
              "liquid_assets,fixed_assets,reserved_amt,reserved_amt_per_share,un_allot_profit," \
              "un_allot_profit_per_share,income_yy_percent,profit_yy_percent,gross_interest_rate,net_profit_rate," \
              "shareholders,time_to_market,trade_date) " \
              "select code,name,industry,area,pe,pb,esp,bvps,outstanding,totals,0,totalAssets,liquidAssets,fixedAssets," \
              "reserved,reservedPerShare,undp,perundp,rev,profit,gpr,npr,holders,timeToMarket,"  \
              "'" + self.get_latest_work_day() + "' from " + self.table_name
        self.insert_sql(sql)

    def update_sunso_stock_basic(self):
        sql = "update " + self.t_sunso_stock_basic + " t1 set totals_stock_amt = " \
              "(select mktcap from " + self.t_tushare_stock_newly_quotes_data + " t2 " \
              "where t1.code = t2.code and t2.date='" + self.get_latest_work_day() + "' limit 1)"
        self.update_sql(sql)

    def is_exist_sunso_stock_basic_by_date(self):
        sql = "select count(*) as c from " + self.t_sunso_stock_basic + " " \
              "where trade_date='" + self.get_latest_work_day() + "'"
        count_value = self.count_sql_default_zero(sql)
        if count_value > 3000:
            return True
        return False

    def delete_sunso_stock_basic(self):
        sql = "delete from " + self.t_sunso_stock_basic + " where trade_date='" + self.get_latest_work_day() + "'"
        self.delete_sql(sql)

# basic = TushareStockBasic()
# basic.insert_sunso_stock_basic_from_tushare_stock_basic()
# basic.update_sunso_stock_basic()
