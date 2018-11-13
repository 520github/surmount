#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from ConfigReader import ConfigReader


class DbEngineHandler(object):

    db_engine = None

    def __init__(self):
        self.configReader = ConfigReader().get_conf("main")
        DbEngineHandler.db_engine = create_engine(self.configReader.mysql_url)
        print("DbEngineHandler init")

    @staticmethod
    def data_to_db_append(data, table_name):
        print(data)
        DbEngineHandler.data_to_db(data, table_name, "append")

    @staticmethod
    def data_to_db(data, table_name, append_type):
        if data is None:
            print("data_to_db input data parameter is empty")
            return
        data.to_sql(table_name, DbEngineHandler.db_engine, if_exists=append_type)