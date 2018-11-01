#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class DateHandler(object):

    @staticmethod
    def get_now_ymd_str():
        return time.strftime("%Y-%m-%d", time.localtime())
