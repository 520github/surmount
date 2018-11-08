#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class FileHandler(object):

    def __init__(self):
        print("FileHandler init")

    @staticmethod
    def is_exist_file(file_path_name):
        return os.path.isfile(file_path_name)

    @staticmethod
    def remove_file(file_path_name):
        os.remove(file_path_name)