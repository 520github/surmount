#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pystache as tp


class TemplateHandler(object):

    def __init__(self):
        print("TemplateHandler init")

    @staticmethod
    def get_template_content_by_key(key, path, data):
        t = open(TemplateHandler.get_template_file_path(key, path), "r")
        content = tp.render(t.read(), data)
        return content

    @staticmethod
    def get_template_file_path(name, path):
        return path + name   #"../sql/"