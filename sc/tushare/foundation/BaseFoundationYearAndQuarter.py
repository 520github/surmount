#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BaseFoundation import BaseFoundation


class BaseFoundationYearAndQuarter(BaseFoundation, object):
    begin_year = 2017
    end_year = 2017
    quarters = [1]
    quarter = 1

    def __init__(self):
        super(BaseFoundationYearAndQuarter, self).__init__()
        print("BaseFoundationYearAndQuarter init...")

    def delete_table_data_before_append(self):
        sql = self.get_delete_sql_by_year_and_quarter(self.begin_year, self.quarter)
        self.delete_sql(sql)

    def append_year_and_quater_to_data(self, data):
        if data is None:
            return data
        data["year"] = self.begin_year
        data["quarter"] = self.quarter
        data["date"] = self.get_now_ymd_str()

    def append_year_and_quater_to_data_and_reset_index(self, data):
        self.append_year_and_quater_to_data(data)
        data.set_index(["code"], inplace=True)

    def get_data(self):
        while self.begin_year <= self.end_year:
            self.__get_data_by_year()

    def __get_data_by_year(self):
        for q in self.quarters:
            self.quarter = q
            self.__get_data_by_year_and_quarter()
        self.begin_year = self.begin_year + 1

    def __get_data_by_year_and_quarter(self):
        self.append_data_to_table()