#!/usr/bin/python
# -*- coding: UTF-8 -*-

from StockPlateBase import StockPlateBase


class SqlTest(StockPlateBase, object):
    sql_template = "plate_type_down_up_down_sql.sql"
    t_sunso_stock_day_trade_statistic_core_data = "t_sunso_stock_day_trade_statistic_core_data"

    def __init__(self):
        super(SqlTest, self).__init__()

    def test_date_list(self):
        self.sql_template = "plate_type_short_hight_callback_sql.sql"
        self.sql_template = "plate_type_down_continue_two_sql.sql"

        self.sql_template = "plate_type_mid_term_two_snake_go_in_down_sql.sql"
        self.sql_template = "plate_type_mid_term_two_shade_after_sun_sql.sql"
        self.sql_template = "plate_type_short_term_sunflower_to_sun_sql.sql"







        self.sql_template = "plate_type_short_term_three_sun_sql.sql"

        self.sql_template = "plate_type_short_term_four_shade_after_sun_sql.sql"

        self.sql_template = "plate_type_short_term_four_stable_after_sun_sql.sql"





        #

        # self.sql_template = "plate_type_short_term_shrinkage_callback_sql.sql"







        self.sql_template = "plate_type_short_term_continue_down_after_sun_sql.sql"

        # self.sql_template = "plate_type_mid_term_abandon_baby_sql.sql"



        #self.sql_template = "plate_type_short_term_two_shade_after_sun_sql.sql"

        self.sql_template = "plate_type_mid_term_continue_down_shrinkage_botton_sql.sql"

        self.sql_template = "plate_type_mid_term_left_abandon_baby_sql.sql"

        self.sql_template = "plate_type_mid_term_right_abandon_baby_sql.sql"

        self.sql_template = "plate_type_mid_term_newly_5_10_20_30_quick_down.sql"

        self.sql_template = "plate_type_mid_term_newly_5_10_20_quick_down.sql"

        # self.sql_template = "plate_type_short_term_quick_up_after_three_adjust_sql.sql"

        # self.sql_template = "plate_type_short_term_quick_up_after_n_day_adjust_sql.sql"

        self.sql_template = "plate_type_mid_term_three_avg_ten_day_down_sql.sql"

        # self.sql_template = "plate_type_mid_term_two_avg_ten_day_up_sql.sql"
        self.sql_template = "plate_type_mid_term_three_sun_sql.sql"
        self.sql_template = "plate_type_short_term_five_shade_sun_change_sql.sql"
        self.sql_template = "plate_type_short_term_up_limit_after_three_up_sql.sql"
        self.sql_template = "plate_type_mid_term_one_up_after_two_down_sql.sql"
        self.sql_template = "plate_type_short_term_four_sun_one_shade_sql.sql"
        self.sql_template = "plate_type_short_term_limit_up_after_down_sql.sql"

        sql = "select distinct trade_date from " + self.t_sunso_stock_day_trade_statistic_core_data + " " \
              "where 1 > 0 and trade_date<'2018-12-28' " \
              "order by trade_date asc "
        data_list = self.select_list_sql(sql)
        if data_list is None:
            return
        for data in data_list:
            trade_date = self.get_date_str(data["trade_date"])
            print("trade_date-->" + trade_date)
            self.test_date_one(trade_date)

    def test_date_one(self, trade_date):
        data = {"trade_date": trade_date}
        sql = self.get_sql_by_template(self.sql_template, data)
        data_list = self.select_list_sql(sql)
        if data_list is None:
            return

        for data in data_list:
            code = data["code"]
            name = data["name"]

            print("trade_date:" + trade_date+", code:" + code + ", name:" + name)


if __name__ == "__main__":
    test = SqlTest()
    test.test_date_list()