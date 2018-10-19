#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://www.cnblogs.com/zhuque/p/8365217.html
# http://www.mamicode.com/info-detail-2171395.html

import ConfigParser
import os


class Dictionary(dict):
    def __getattr__(self, item):
        return self.get(item, "没有找到对应的值for"+item)


class ConfigReader(object):

    def __init__(self):
        current_dir = os.path.dirname(__file__)
        top_dir = os.path.dirname(current_dir)
        file_name = top_dir + "/conf/conf.ini"
        self.config = ConfigParser.ConfigParser()
        self.config.read(file_name)
        print("init configReader-->" + file_name)

        for section in self.config.sections():
            setattr(self, section, Dictionary())
            for key, value in self.config.items(section):
                setattr(getattr(self, section), key, value)

    def get_conf(self, section):
        if section in self.config.sections():
            pass
        else:
            print("找不到")
        return getattr(self, section);
        # num = len(self.config.sections())
        # print("num-->" + str(num))
        # key_value = ""
        # i = 0
        # while i < num:
        #     section = self.config.sections()[i]
        #     if key_name in self.config.options(section):
        #         key_value = self.config.get(section, key_name)
        #         break
        #     else:
        #         i = i + 1
        #
        # return key_value


test = ConfigReader()
# url = test.get_conf("url")
url = test.get_conf("main").url
print("url-->" + url)