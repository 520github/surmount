#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseIndustry import BaseIndustry


class DayIndustryStatisticCoreData(BaseIndustry, object):
    trade_date = "2018-11-26"
    table_name = "t_sunso_stock_day_industry_statistic_core_data"
    t_sunso_stock_day_trade_statistic_core_data = "t_sunso_stock_day_trade_statistic_core_data"

    def __init__(self):
        super(DayIndustryStatisticCoreData, self).__init__()
        print("DayIndustryStatisticCoreData init")

    def handle_list_day_industry(self):
        sql = "select distinct trade_date from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where trade_date not in (select distinct trade_date from " + self.table_name + ") " \
              "order by trade_date asc "
        date_list = self.select_list_sql(sql)
        if date_list is None:
            return

        for date in date_list:
            self.trade_date = self.get_date_str(date["trade_date"])
            print("handle data date-->" + str(self.trade_date))
            self.handle_one_day_industry()

    def handle_one_day_industry(self):
        self.step1_insert()
        self.step2_update_day_industry_list()

    def step1_insert(self):
        template_key = "insert_day_industry_statistic_core_data.sql"
        data = {"trade_date": self.trade_date}
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def step2_update_day_industry_list(self):
        data_list = self.get_day_industry_list()
        for data in data_list:
            self.step3_update_day_industry_one(data)

    def step3_update_day_industry_one(self, data):
        sum_up_limit_count = self.get_up_limit_count(data)
        sum_down_limit_count = self.get_down_limit_count(data)

        data["sum_up_limit_count"] = sum_up_limit_count
        data["sum_down_limit_count"] = sum_down_limit_count
        data["up_down_limit_count_ratio"] = self.cal_division_round_2(sum_up_limit_count, sum_down_limit_count)

        sum_up_count = self.get_up_count(data)
        sum_down_count = self.get_down_count(data)
        data["sum_up_count"] = sum_up_count
        data["sum_down_count"] = sum_down_count
        data["up_down_count_ratio"] = self.cal_division_round_2(sum_up_count, sum_down_count)

        up_top_names = self.repair_data(self.get_up_top3_name(data), 3)
        data["up_top1_name"] = up_top_names[0]
        data["up_top2_name"] = up_top_names[1]
        data["up_top3_name"] = up_top_names[2]

        down_top_names = self.repair_data(self.get_down_top3_name(data), 3)
        data["down_top1_name"] = down_top_names[0]
        data["down_top2_name"] = down_top_names[1]
        data["down_top3_name"] = down_top_names[2]

        data["up_avg_close_price_ratio"] = round(self.get_up_avg(data), 2)
        data["down_avg_close_price_ratio"] = round(self.get_down_avg(data), 2)

        limits = [1, 3, 5, 10, 20, 30, 60, 90, 120] #, 180, 250, 360
        for limit in limits:
            self.add_pre_day_column_value(data, limit)

        template_key = "update_day_industry_statistic_core_data.sql"
        update_sql = self.get_sql_by_template(template_key, data)
        self.update_sql(update_sql)

    def add_pre_day_column_value(self, data, limit):
        pre_limit = "pre" + str(limit)
        pre_totals_stock_amt_ratio = "%s_totals_stock_amt_ratio" % pre_limit
        pre_circulation_stock_amt_ratio = "%s_circulation_stock_amt_ratio" % pre_limit
        pre_totals_stock_volume_ratio = "%s_totals_stock_volume_ratio" % pre_limit
        pre_circulation_stock_volume_ratio = "%s_circulation_stock_volume_ratio" % pre_limit
        pre_sum_close_price_ratio = "%s_sum_close_price_ratio" % pre_limit
        pre_avg_close_price_ratio = "%s_avg_close_price_ratio" % pre_limit
        pre_avg_trade_amt = "%s_avg_trade_amt" % pre_limit
        pre_avg_trade_volume = "%s_avg_trade_volume" % pre_limit
        pre3_avg_trade_count = "%s_avg_trade_count" % pre_limit

        pre_totals_stock_amt = self.get_pre_one_day_totals_stock_amt(data, limit)
        pre_circulation_stock_amt = self.get_pre_one_day_circulation_stock_amt(data, limit)
        pre_totals_stock_volume = self.get_pre_one_day_totals_stock_volume(data, limit)
        pre_circulation_stock_volume = self.get_pre_one_day_circulation_stock_volume(data, limit)
        totals_stock_amt = data["totals_stock_amt"]
        circulation_stock_amt = data["circulation_stock_amt"]
        totals_stock_volume = data["totals_stock_volume"]
        circulation_stock_volume = data["circulation_stock_volume"]

        data[pre_totals_stock_amt_ratio] = self.cal_percent_round_2_not_zero(totals_stock_amt, pre_totals_stock_amt)
        data[pre_circulation_stock_amt_ratio] = self.cal_percent_round_2_not_zero(circulation_stock_amt, pre_circulation_stock_amt)
        data[pre_totals_stock_volume_ratio] = self.cal_percent_round_2_not_zero(totals_stock_volume, pre_totals_stock_volume)
        data[pre_circulation_stock_volume_ratio] = self.cal_percent_round_2_not_zero(circulation_stock_volume, pre_circulation_stock_volume)

        data[pre_sum_close_price_ratio] = self.get_pre_day_sum_close_price_ratio(data, limit)
        data[pre_avg_close_price_ratio] = self.get_pre_day_avg_close_price_ratio(data, limit)
        data[pre_avg_trade_amt] = self.get_pre_day_avg_trade_amt(data, limit)
        data[pre_avg_trade_volume] = self.get_pre_day_avg_trade_volume(data, limit)
        data[pre3_avg_trade_count] = self.get_pre_day_avg_trade_count(data, limit)
        return data

    def repair_data(self, data, length):
        if data is None:
            data = []
            for i in range(length):
                data.append("")
            return data

        data = data.split(",")

        data_length = len(data)
        if data_length >= length:
            return data

        for i in range(data_length, length):
            data.append("")
        return data

    def get_day_industry_list(self):
        sql = "select * from " + self.table_name + " " \
              "where trade_date='" + self.trade_date + "'"
        return self.select_list_sql(sql)


if __name__ == "__main__":
    dis = DayIndustryStatisticCoreData()
    dis.handle_list_day_industry()
    # dis.handle_one_day_industry()