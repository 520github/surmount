#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform


class CommonHandler(object):

    @staticmethod
    def is_window_platform():
        sysstr = platform.system()
        print(sysstr)
        if sysstr == "window":
            return True
        return False


if __name__ == "__main__":
    result = CommonHandler.is_window_platform()
    print(result)