#!/usr/bin/python
# -*- coding: UTF-8 -*-


from TrackBace import TrackBace


class IndustryTrackBase(TrackBace, object):

    def __init__(self):
        super(IndustryTrackBase, self).__init__()
        self.classify_type = "industry"
        print("IndustryTrackBase init......")

    def init_classify_track_basic(self):
        template_key = "industry_insert_stock_classify_track_basic.sql"
        data = {"trade_date": self.trade_date}
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def update_classify_track_basic(self, classify_track_basic_data):
        data = {"trade_date": self.trade_date, "industry": classify_track_basic_data["classify_name"]}
        classify_track_basic_data["trade_date"] = self.trade_date
        classify_track_basic_data["stock_num"] = self.get_industry_stock_num_value_by_date(data)
        trade_date_totals_stock_amt = self.get_industry_totals_stock_amt_value_by_date(data)

        data["trade_date"] = classify_track_basic_data["track_date"]
        track_date_totals_stock_amt = self.get_industry_totals_stock_amt_value_by_date(data)

        classify_track_basic_data["from_track_date_up_down_ratio"] = self.cal_percent_round_2_not_zero(trade_date_totals_stock_amt, track_date_totals_stock_amt)
        template_key = "industry_update_stock_classify_track_basic.sql"
        sql = self.get_sql_by_template(template_key, classify_track_basic_data)
        self.update_sql(sql)

    def init_classify_track_config(self):
        template_key = "industry_insert_stock_classify_track_config.sql"
        data = {"trade_date": self.trade_date}
        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def init_one_classify_track_day_data(self, data):
        template_key = "industry_insert_stock_classify_track_day_data.sql"
        data["trade_date"] = self.trade_date
        industry_data = {"industry": data["classify_name"], "track_date": data["track_date"], "trade_date": data["track_date"]}

        track_date_totals_stock_amt = self.get_industry_totals_stock_amt_value_by_date(industry_data)
        industry_data["trade_date"] = self.trade_date
        trade_date_totals_stock_amt = self.get_industry_totals_stock_amt_value_by_date(industry_data)
        data["from_track_date_up_down_ratio"] = self.cal_percent_round_2_not_zero(
            trade_date_totals_stock_amt, track_date_totals_stock_amt)

        data["track_sum_day"] = self.get_industry_count_value_by_between_date(industry_data)
        data["trade_volume"] = self.get_industry_trade_volume_value_by_date(industry_data)
        data["sum_close_amt_ratio"] = round(self.get_industry_sum_close_amt_ratio_value_by_date(industry_data), 2)
        data["avg_close_amt_ratio"] = round(self.get_industry_avg_close_amt_ratio_value_by_date(industry_data), 2)
        data["stock_num"] = self.get_industry_stock_num_value_by_date(industry_data)

        sql = self.get_sql_by_template(template_key, data)
        self.insert_sql(sql)

    def get_classify_stock_list(self, classify_track_basic_data):
        data = {"industry": classify_track_basic_data["classify_name"], "trade_date":self.trade_date}
        template_key = "get_stock_list_by_industry.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.select_list_sql(sql)

    def get_industry_trade_volume_value_by_date(self, data):
        return self.get_industry_column_value_by_date(data, "trade_volume")

    def get_industry_sum_close_amt_ratio_value_by_date(self, data):
        return self.get_industry_column_value_by_date(data, "sum_close_price_ratio")

    def get_industry_avg_close_amt_ratio_value_by_date(self, data):
        return round(self.get_industry_column_value_by_date(data, "avg_close_price_ratio"),2)

    def get_industry_stock_num_value_by_date(self, data):
        return self.get_industry_column_value_by_date(data, "stock_num")

    def get_industry_totals_stock_amt_value_by_date(self, data):
        return self.get_industry_column_value_by_date(data, "totals_stock_amt")

    def get_industry_column_value_by_date(self, data, column):
        data["column"] = column
        template_key = "industry_column_value_by_one_date.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql(sql)

    def get_industry_count_value_by_between_date(self, data):
        return self.get_industry_column_value_by_between_date(data, "count(*)")

    def get_industry_column_value_by_between_date(self, data, column):
        data["column"] = column
        template_key = "industry_column_value_by_between_date.sql"
        sql = self.get_sql_by_template(template_key, data)
        return self.count_sql(sql)


if __name__ == "__main__":
    industry = IndustryTrackBase()
    industry.init_classify_track_list_portal()