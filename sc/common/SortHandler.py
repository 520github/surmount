#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SortHandler(object):

    def __init__(self):
        print("SortHandler init...")

    @staticmethod
    def get_dict_data_list_by_sort_key(dict_data_list):
        if SortHandler.is_empty_dict_data_list(dict_data_list):
            return None
        new_dict_data_list = []
        for dict_data_one in dict_data_list:
            new_dict_data_list.append(SortHandler.sort_dict_by_key(dict_data_one))
        return new_dict_data_list

    @staticmethod
    def sort_dict_by_key(dict_data_one):
        if dict_data_one is None:
            return dict_data_one
        # keys = dict_data.keys()
        # keys.sort()
        # return map(dict_data.get, keys)
        items = dict_data_one.items()
        items.sort()
        return [value for key, value in items]

    @staticmethod
    def get_sort_keys_by_dict_data_list(dict_data_list):
        if SortHandler.is_empty_dict_data_list(dict_data_list):
            return None
        dict_data_one = dict_data_list[0]
        keys = dict_data_one.keys()
        keys.sort()
        return keys

    @staticmethod
    def is_empty_dict_data_list(dict_data_list):
        if dict_data_list is None or len(dict_data_list) < 1:
            return True
        return False



if __name__ == "__main__":
    dict_data = [{"dd":"dd","aa":"aa"},{"dd":"dd","aa":"aa"}]
    print(dict_data)
    result_data = SortHandler.sort_dict_list_by_key(dict_data)
    print(result_data)