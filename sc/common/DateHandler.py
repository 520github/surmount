#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime


class DateHandler(object):

    @staticmethod
    def get_now_ymd_str():
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def compare_greater_two_date_str(first_date, two_date):
        if first_date is None:
            return False
        if two_date is None:
            return False
        if datetime.datetime.strptime(first_date, "%Y-%m-%d") > datetime.datetime.strptime(two_date, "%Y-%m-%d"):
            return True
        return False

    @staticmethod
    def get_date_str(date):
        if date is None:
            return date
        if not isinstance(date, datetime.date):
            return date
        return date.strftime("%Y-%m-%d")